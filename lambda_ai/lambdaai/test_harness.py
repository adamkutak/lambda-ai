import os
from .apis import APIFunction
from .environment import APIEnvironment, APIFile
from .gpt_management import openAIchat
from .unused_prompts import (
    AUTO_TESTER_DATABASE_EXT,
    AUTO_TESTER_ON_ERROR,
    AUTO_TESTER_ONESHOT_ARGS,
    AUTO_TESTER_ONESHOT_PROMPT,
    AUTO_TESTER_BUILD_PROMPT,
)
from .gpt_function_calls import (
    FUNCTION_CALLING_TEST_CREATION,
    FUNCTION_CALLING_TEST_CREATION_DB_EXT,
    FunctionCallTest,
    FunctionCallTestWithDB,
)
from .utils import close_enough_float, execute_sql

AUTO_BUILD_TEST_CASE_COUNT = 3
MAX_AUTO_BUILD_ATTEMPTS = 5


class TestHarness:
    def __init__(
        self,
        api_function: APIFunction,
        api_file: APIFile,
    ):
        self.api_function = api_function
        self.test_server = APIEnvironment(api_file, for_testing=True)

    def perform_test(self):
        deploy_result, message = self.test_server.deploy()
        if deploy_result > 0:
            return 1, message

        test_db = (
            self.api_function.attached_db if self.api_function.attached_db else None
        )
        for test_case in self.api_function.test_cases:
            if test_db:
                test_db.create_testing_copy()
                pre_sql_queries = test_case.get("pre_sql", [])
                for query in pre_sql_queries:
                    execute_sql(test_db.test_db_path, query)
            error_message = None
            e, response = self.test_server.query(
                self.api_function.path, test_case["input"]
            )
            if e:
                error_message = (
                    f"error on test case: {str(test_case['input'])}, error: {e}"
                )
            elif response.status_code >= 400:
                error_message = f"error on test case: {str(test_case['input'])}, error: {response.text}"
            elif response.json() != test_case["output"] and not close_enough_float(
                response.json(), test_case["output"]
            ):
                error_message = f"error on test case: {str(test_case['input'])}, expected output is: {str(test_case['output'])}. Actual output is {str(response.json())}"

            if test_db and not error_message:
                post_sql_tests = test_case.get("post_sql", [])
                for test in post_sql_tests:
                    if not error_message:
                        result_val = execute_sql(test_db.test_db_path, test["sql"])
                        if result_val[0][0] != test["assert_value"]:
                            pre_sql_queries_str = "\n".join(pre_sql_queries)
                            error_message = (
                                f"Error: while testing with input {str(test_case['input'])},"
                                f"with test assert SQL on the database: {test['sql']},\n"
                                f"expected return value {test['assert_value']}, got {result_val[0][0]} instead."
                                "Additional Info: the following pre-test setup was ran on the database:\n"
                                f"{pre_sql_queries_str}\n\n"
                            )
                os.remove(test_db.test_db_path)

            if error_message:
                self.test_server.undeploy()
                return 1, error_message

        self.test_server.undeploy()
        return 0, "success"

    def build_auto_tester(
        api_function: APIFunction, test_count=AUTO_BUILD_TEST_CASE_COUNT
    ):
        ai_chat = openAIchat(
            model="gpt-3.5-turbo-0613",
            system_message="Only use the functions you have been provided with.",
            functions=[
                FUNCTION_CALLING_TEST_CREATION_DB_EXT
                if api_function.attached_db
                else FUNCTION_CALLING_TEST_CREATION
            ],
        )

        ext_str = ""
        attached_db = api_function.attached_db if api_function.attached_db else None
        if attached_db:
            ext_str = AUTO_TESTER_DATABASE_EXT.format(
                database_info=attached_db.view_db_details()
            )
            function_kind = FunctionCallTestWithDB
        else:
            ai_chat.add_function_one_shot_prompt(
                "add_test", AUTO_TESTER_ONESHOT_PROMPT, AUTO_TESTER_ONESHOT_ARGS
            )
            function_kind = FunctionCallTest
        prompt = AUTO_TESTER_BUILD_PROMPT.format(
            name=api_function.name,
            inputs=api_function.inputs,
            outputs=api_function.outputs,
            functionality=api_function.functionality,
            ext_str=ext_str,
        )
        for _ in range(test_count):
            ai_response = ai_chat.send_chat(message=prompt, function_call="add_test")
            print(ai_response)
            result_code = 1
            build_attempts = 0
            while result_code > 0 and build_attempts < MAX_AUTO_BUILD_ATTEMPTS:
                result_code, data = openAIchat.validate_json_function_call(
                    ai_response, "add_test", function_kind
                )
                if result_code == 0:
                    generated_test_case = data
                    result_code, data = TestHarness.verify_autogenerated_test(data)

                if result_code > 0:
                    ai_response = ai_chat.send_chat(
                        message=AUTO_TESTER_ON_ERROR.format(error=data),
                        function_call="add_test",
                    )
                    build_attempts += 1
                    print(data)

            if result_code > 0:
                return result_code, data

            api_function.test_cases.append(generated_test_case)
            prompt = "That is a valid test case. Give me another test case using the add_test function"

        return 0, "success"

    def verify_autogenerated_test(data):
        return 0, "success"  # TODO: fill this function in
