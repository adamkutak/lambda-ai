from .environment import APIFile
from .prompts import (
    CHAIN_OF_THOUGHT_REASONING,
    CHAIN_OF_THOUGHT_REASONING_WITH_DB,
    CREATE_ENDPOINT,
    CREATE_ENDPOINT_WITH_DB,
    ERROR_ANALYSIS,
    ON_CREATE_ERROR,
    ONE_SHOT_PROMPT_FUNCTION_ARGS,
    ONE_SHOT_PROMPT_WITH_DB_FUNCTION_ARGS,
    ONE_SHOT_PROMPT_WITH_DB_FUNCTION_ARGS_2,
)
from .gpt_function_calls import (
    FUNCTION_CALLING_ENDPOINT_CREATION,
    EndpointCreation,
)
from .utils import generate_fastapi_definition
from .gpt_management import openAIchat
from .db import DB

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
        use_line_by_line: bool = True,
        use_error_analysis: bool = False,
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
        self.use_line_by_line = use_line_by_line
        self.use_error_analysis = use_error_analysis

    def create_api_function(self) -> str:
        from .test_harness import TestHarness

        if not self.test_cases:
            result_code, message = self.test_harness = TestHarness.build_auto_tester(
                api_function=self
            )
            if result_code > 0:
                print(f"Failed to autogenerate test cases: {message}")

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
            model="gpt-4",
            system_message="Only use the functions you have been provided with.",  # noqa
            functions=[FUNCTION_CALLING_ENDPOINT_CREATION],
        )

        if self.attached_db:
            ai_chat.add_function_one_shot_prompt(
                "create_api",
                None,
                ONE_SHOT_PROMPT_WITH_DB_FUNCTION_ARGS,
            )
            ai_chat.add_function_one_shot_prompt(
                "create_api",
                None,
                ONE_SHOT_PROMPT_WITH_DB_FUNCTION_ARGS_2,
            )
            prompt = CREATE_ENDPOINT_WITH_DB.format(
                name=self.name,
                path=self.path,
                inputs=str(self.inputs),
                outputs=str(self.outputs),
                functionality=self.functionality,
                function_def=function_def,
                table_list=self.attached_db.view_db_details(),
                line_by_line=self.breakdown_description()
                if self.use_line_by_line
                else "",
            )
        else:
            ai_chat.add_function_one_shot_prompt(
                "create_api", None, ONE_SHOT_PROMPT_FUNCTION_ARGS
            )
            prompt = CREATE_ENDPOINT.format(
                name=self.name,
                path=self.path,
                inputs=str(self.inputs),
                outputs=str(self.outputs),
                functionality=self.functionality,
                function_def=function_def,
                line_by_line=self.breakdown_description()
                if self.use_line_by_line
                else "",
            )

        print(prompt)
        ai_response = ai_chat.send_chat(
            message=prompt,
            function_call="create_api",
        )

        # process, validate, and test.
        from .test_harness import TestHarness

        result_code = 1
        while result_code > 0 and self.build_attempts[-1] < MAX_TEST_ATTEMPTS:
            result_code, data = self.process_and_validate_response(ai_response)
            print(f"process/validation is {result_code}: {data}")
            if result_code == 0:
                test_harness = TestHarness(api_function=self, api_file=data)
                result_code, data = test_harness.perform_test()
                print(f"testing is {result_code}: {data}")

            if result_code > 0:
                if self.use_error_analysis and result_code < 2:
                    analysis = f"The following analysis might be useful to you:\n{self.analyse_error(data)}"
                else:
                    analysis = ""
                print(analysis)
                ai_response = ai_chat.send_chat(
                    message=ON_CREATE_ERROR.format(error=data, analysis=analysis),
                    function_call="create_api",
                )
                self.build_attempts[-1] += 1

        if result_code > 0:
            return result_code, data

        return result_code, data

    def process_and_validate_response(self, ai_response) -> (int, str):
        validate_json, data = openAIchat.validate_json_function_call(
            ai_response,
            "create_api",
            EndpointCreation,
        )
        if validate_json > 0:
            return 2, data

        imports = data["imports"]
        function = data["endpoint"]
        test_function = function
        if self.attached_db:
            if self.force_use_db and "execute_sql" not in function:
                return (
                    2,
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

    def breakdown_description(self) -> str:
        ai_chat = openAIchat(
            model="gpt-4",
            system_message="Only return the line by line of how to construct the function.",
        )

        if self.attached_db:
            prompt = CHAIN_OF_THOUGHT_REASONING_WITH_DB.format(
                inputs=str(self.inputs),
                outputs=str(self.outputs),
                functionality=self.functionality,
                table_list=self.attached_db.view_db_details(),
            )
        else:
            prompt = CHAIN_OF_THOUGHT_REASONING.format(
                inputs=str(self.inputs),
                outputs=str(self.outputs),
                functionality=self.functionality,
            )

        ai_response = ai_chat.send_chat(
            message=prompt,
        )

        return ai_response

    def analyse_error(self, error: str) -> str:
        ai_chat = openAIchat(
            model="gpt-4",
            system_message="Only return a description of why you believe there is an error in the function.",
        )

        prompt = ERROR_ANALYSIS.format(
            function_code=self.api_function_created["function_code"], error=error
        )
        ai_response = ai_chat.send_chat(
            message=prompt,
        )

        return ai_response
