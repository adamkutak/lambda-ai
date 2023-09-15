import os
import sqlite3
from lambdaai.apis import APIFunction
from lambdaai.environment import APIEnvironment, APIFile
from lambdaai.utils import close_enough_float


class TestHarness:
    def __init__(
        self,
        api_function: APIFunction,
        api_file: APIFile,
    ):
        if not api_function.test_cases:
            self.standard_test = False
            self.build_auto_tester
        else:
            self.standard_test = True
        self.api_function = api_function
        self.test_server = APIEnvironment(api_file)

    def build_auto_tester(self):
        # generate input + output
        # generate sql calls to add test rows
        # generate sql calls to verify rows
        pass

    def perform_test(self):
        deploy_result, message = self.test_server.deploy()
        if deploy_result > 0:
            return 1, message

        test_db = None
        for test_case in self.api_function.test_cases:
            if self.api_function.attached_db:
                test_db = self.api_function.attached_db.create_testing_copy()
            error_message = None
            e, response = self.test_server.query(
                self.api_function.path, test_case["input"]
            )

            if e:
                error_message = f"error on test case: {str(test_case)}, error: {e}"
            elif response.status_code >= 400:
                error_message = (
                    f"error on test case: {str(test_case)}, error: {response.text}"
                )
            elif response.json() != test_case["output"] and not close_enough_float(
                response.json(), test_case["output"]
            ):
                error_message = f"error on test case: {str(test_case['input'])}, expected output is: {str(test_case['output'])}. Actual output is {str(response.json())}"

            if test_db:
                os.remove(self.api_function.attached_db.test_db_path)

            if error_message:
                self.test_server.undeploy()
                return 1, error_message

        self.test_server.undeploy()
        return 0, "success"
