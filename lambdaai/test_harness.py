from lambdaai.environment import APIEnvironment
from lambdaai.utils import close_enough_float


class TestHarness:
    def __init__(
        self,
        api_function,
        api_file,
    ):
        if not api_function.test_cases:
            self.standard_test = False
            self.build_auto_tester
        else:
            self.standard_test = True
        self.api_function = api_function
        self.test_server = APIEnvironment(api_file)

    def build_auto_tester(self):
        pass

    def perform_test(self):
        if self.api_function.attached_db:
            self.api_function.attached_db.create_shared_in_memory_copy()

        deploy_result, message = self.test_server.deploy()
        if deploy_result > 0:
            return 1, message

        for test_case in self.api_function.test_cases:
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

            if error_message:
                self.test_server.undeploy()
                return 1, error_message

        self.test_server.undeploy()

        return 0, "success"
