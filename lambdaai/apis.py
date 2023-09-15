from lambdaai.environment import APIFile
from lambdaai.prompts import (
    CREATE_ENDPOINT,
    ON_CREATE_ERROR,
    FUNCTION_CALLING_ENDPOINT_CREATION,
    ONE_SHOT_PROMPT_USER,
    ONE_SHOT_PROMPT_FUNCTION_ARGS,
    CREATE_ENDPOINT_WITH_DB,
)
from lambdaai.utils import generate_fastapi_definition
from lambdaai.gpt_management import openAIchat
from lambdaai.db import DB


MAX_TEST_ATTEMPTS = 5
MAX_BUILD_ATTEMPTS = 3


class APIFunction:
    def __init__(
        self,
        name: str,
        path: str,
        inputs: dict,
        outputs: dict,
        functionality: str,
        test_cases: list[dict] = [],
        is_async: bool = None,
        attached_db: DB = None,
        force_use_db: bool = False,
    ):
        self.name = name
        self.path = path
        self.inputs = inputs
        self.outputs = outputs
        self.functionality = functionality
        self.test_cases = test_cases
        self.is_async = is_async
        self.build_attempts = []
        self.api_function_created = {}
        self.attached_db = attached_db
        self.force_use_db = force_use_db

    def create_api_function(self) -> str:
        result_code = 1
        while result_code > 0 and len(self.build_attempts) < MAX_BUILD_ATTEMPTS:
            result_code, message = self.maybe_create_api_function()
            print("-----1-----")
            print(result_code)
            print(message)

        return result_code, message

    def maybe_create_api_function(self) -> (int, str):
        self.build_attempts.append(0)

        function_def = generate_fastapi_definition(
            self.name,
            self.path,
            self.inputs,
            self.outputs,
            self.is_async,
        )

        ai_chat = openAIchat(
            model="gpt-3.5-turbo-0613",
            system_message="Only use the functions you have been provided with.",  # noqa
            functions=[FUNCTION_CALLING_ENDPOINT_CREATION],
        )

        if self.attached_db:
            prompt = CREATE_ENDPOINT_WITH_DB.format(
                name=self.name,
                path=self.path,
                inputs=str(self.inputs),
                outputs=str(self.outputs),
                functionality=self.functionality,
                function_def=function_def,
                table_list=self.attached_db.view_db_details(),
            )
        else:
            ai_chat.add_one_shot_prompt(
                ONE_SHOT_PROMPT_USER, ONE_SHOT_PROMPT_FUNCTION_ARGS
            )
            prompt = CREATE_ENDPOINT.format(
                name=self.name,
                path=self.path,
                inputs=str(self.inputs),
                outputs=str(self.outputs),
                functionality=self.functionality,
                function_def=function_def,
            )
        ai_response = ai_chat.send_chat(
            message=prompt,
            function_call="create_api",
        )

        # process, validate, and test.
        from lambdaai.test_harness import TestHarness

        result_code = 1
        while result_code > 0 and self.build_attempts[-1] < MAX_TEST_ATTEMPTS:
            print(ai_response)
            result_code, data = self.process_and_validate_response(ai_response)
            print(f"process/validation is {result_code}: {data}")
            if result_code == 0:
                test_harness = TestHarness(self, data)
                result_code, data = test_harness.perform_test()
                print(f"testing is {result_code}: {data}")

            if result_code > 0:
                ai_response = ai_chat.send_chat(
                    message=ON_CREATE_ERROR.format(
                        error=data, test_cases=self.test_cases
                    ),
                    function_call="create_api",
                )
                self.build_attempts[-1] += 1

        if result_code > 0:
            return result_code, data

        return result_code, data

    def process_and_validate_response(self, ai_response) -> (int, str):
        validate_json, message = openAIchat.validate_json_function_call(
            ai_response,
            "create_api",
            ["endpoint", "imports"],
        )
        if validate_json > 0:
            return 1, message

        function_call_args = openAIchat.get_function_call_args(
            ai_response,
            "create_api",
        )
        imports = function_call_args["imports"]
        function = function_call_args["endpoint"]
        test_function = function
        if self.attached_db:
            if self.force_use_db and "execute_sql" not in function:
                return (
                    1,
                    "Error: you must make use of the database in this function, the info for which you have been given already.",
                )
            function = self.attached_db.insert_db_path_into_function_exec_calls(
                function
            )
            test_function = self.attached_db.insert_db_path_into_function_exec_calls(
                test_function, for_test=True
            )
        print(function)

        self.api_function_created = {
            "name": self.name,
            "path": self.path,
            "function_code": function,
            "imports": imports,
        }

        function_test = self.api_function_created.copy()
        function_test["function_code"] = test_function

        format_file_name = "format_file_test"
        format_file = APIFile(format_file_name, attach_db=self.attached_db is not None)
        format_file.add_function(function_test)

        format_result, message = format_file.black_format_file()
        if format_result > 0:
            return 1, message

        check_python_result, message = format_file.check_python()
        if check_python_result > 0:
            return 1, message

        self.format_file = format_file
        return 0, format_file
