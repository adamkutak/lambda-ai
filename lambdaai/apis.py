from typing import Dict
from lambdaai.prompts import (
    CREATE_ENDPOINT,
    ON_CREATE_ERROR,
    FUNCTION_CALLING_ENDPOINT_CREATION,
    ONE_SHOT_PROMPT_USER,
    ONE_SHOT_PROMPT_FUNCTION_ARGS,
    CREATE_ENDPOINT_WITH_DB,
)
import subprocess
import requests
import atexit
from lambdaai.utils import close_enough_float, generate_fastapi_definition, get_imports
from lambdaai.gpt_management import openAIchat
from lambdaai.db import DB

TEST_FOLDER = "generated_tests"

FASTAPI_CODE = """
app = FastAPI()
"""

IMPORT_CODE = [
    "from fastapi import FastAPI",
    "from typing import Dict, Any",
]


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "8000"

MAX_TEST_ATTEMPTS = 5
MAX_BUILD_ATTEMPTS = 3

SQL_EXEC_FUNCTION = """def execute_sql(db_path: str, sql: str):
    connection = sqlite3.connect(db_path)
    crsr = connection.cursor()
    result = crsr.execute(sql)
    if "SELECT" in sql:
        result = result.fetchall()
    connection.commit()
    connection.close()
    return result
"""


class APIFunction:
    def __init__(
        self,
        name: str,
        path: str,
        inputs: dict,
        outputs: dict,
        functionality: str,
        test_cases: list[dict],
        is_async: bool = None,
        attached_db: DB = None,
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

        result_code, message = self.validate_and_test_api_function(ai_response)
        print("----2-----")
        print(result_code)
        print(message)
        while result_code > 0 and self.build_attempts[-1] < MAX_TEST_ATTEMPTS:
            ai_response = ai_chat.send_chat(
                message=ON_CREATE_ERROR.format(
                    error=message, test_cases=self.test_cases
                ),
                function_call="create_api",
            )
            self.build_attempts[-1] += 1
            result_code, message = self.validate_and_test_api_function(ai_response)
            print("----2-----")
            print(result_code)
            print(message)

        if result_code == 0:
            function_call_args = openAIchat.get_function_call_args(
                ai_response,
                "create_api",
            )
            if self.attached_db:
                function = self.attached_db.insert_db_path_into_function_exec_calls(
                    function_call_args["endpoint"]
                )
            else:
                function = function_call_args["endpoint"]
            self.api_function_created["name"] = self.name
            self.api_function_created["path"] = self.path
            self.api_function_created["function_code"] = function
            self.api_function_created["imports"] = function_call_args["imports"]

        return result_code, message

    def validate_and_test_api_function(self, ai_response) -> (int, str):
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
        if self.attached_db:
            function = self.attached_db.insert_db_path_into_function_exec_calls(
                function
            )
        print(function)

        test_file_name = f"test_{self.name}"
        attach_db = self.attached_db is not None
        test_api_file = APIFile(test_file_name, attach_db=attach_db)
        test_api_file.add_function(
            {
                "name": self.name,
                "path": self.path,
                "function_code": function,
                "imports": imports,
            }
        )
        format_result, message = test_api_file.format_file()
        if format_result > 0:
            return 1, message

        check_python_result, message = test_api_file.check_python()
        if check_python_result > 0:
            return 1, message

        api_server = APIEnvironment(test_api_file)

        deploy_result, message = api_server.deploy()
        if deploy_result > 0:
            return 1, message

        for test_case in self.test_cases:
            error_message = None
            e, response = api_server.query(self.path, test_case["input"])

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
                api_server.undeploy()
                return 1, error_message

        api_server.undeploy()

        return 0, "success"


class APIFile:
    def __init__(self, name: str, file_path: str = None, attach_db: bool = False):
        self.name = name
        self.functions = {}
        self.imports = set(IMPORT_CODE)
        if file_path:
            self.file_path = file_path + "/" + self.name + ".py"
        else:
            self.file_path = TEST_FOLDER + "/" + self.name + ".py"

        if attach_db:
            self.add_function(
                {
                    "name": "execute_sql",
                    "path": "fake_sql_path/",
                    "function_code": SQL_EXEC_FUNCTION,
                    "imports": "import sqlite3",
                }
            )

    def add_function(self, api_function: Dict[str, str]) -> str:
        assert api_function["name"] not in self.functions
        assert api_function["path"] not in [
            func["path"] for func in self.functions.values()
        ]

        self.functions[api_function["name"]] = {
            "path": api_function["path"],
            "function_code": api_function["function_code"],
        }

        new_imports = []
        for new_import in api_function["imports"].split("\n"):
            if new_import.startswith("import") or new_import.startswith("from"):
                new_imports.append(new_import)
        self.imports.update(new_imports)

        self.create_file()

        return "success"

    def create_file(self):
        file_string = self.build_file()

        with open(self.file_path, "w") as file:
            file.write(file_string)

        return "success"

    def format_file(self):
        try:
            subprocess.run(
                ["black", self.file_path],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            black_subprocess_error = e.stderr.decode("utf-8")
            return 1, f"{black_subprocess_error}. Python is likely invalid."
        return 0, "success"

    def check_python(self):
        try:
            subprocess.run(
                ["python", self.file_path],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            python_subprocess_error = e.stderr.decode("utf-8")
            return 1, f"{python_subprocess_error}"

        return 0, "success"

    def build_file(self):
        imports = "\n".join(self.imports)
        file_string = "\n".join(
            [
                imports,
                "\n",
                FASTAPI_CODE,
                "\n",
            ]
        )

        for function in self.functions.values():
            file_string += function["function_code"]
            file_string += "\n"

        return file_string


class APIEnvironment:
    def __init__(self, api_file: APIFile, host: str = None, port: str = None):
        self.api_file = api_file
        self.host = host or DEFAULT_HOST
        self.port = port or DEFAULT_PORT
        self.file_uvicorn = api_file.file_path.replace("/", ".").replace(".py", "")
        self.requirements_file = self.create_requirements_file()

    def deploy(self):
        if self.requirements_file:
            install_code, message = self.install_requirements()
            if install_code > 0:
                return message

        try:
            self.server_process = subprocess.Popen(
                [
                    "uvicorn",
                    "--host",
                    self.host,
                    "--port",
                    self.port,
                    f"{self.file_uvicorn}:app",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            atexit.register(self.server_process.terminate)

            self.await_live()

        except Exception as e:
            return 1, f"error starting api deployment: {e}"
        return 0, "success"

    def undeploy(self):
        self.server_process.terminate()

    def query(self, path, input):
        try:
            response = requests.get(
                f"http://{self.host}:{self.port}{path}",
                params=input,
            )
        except Exception as e:
            return e, response
        else:
            return None, response

    def create_requirements_file(self):
        requirements_file_path = self.api_file.file_path.replace(
            ".py", "_requirements.txt"
        )
        modules = get_imports(self.api_file.imports)
        if modules:
            modules_string = "\n".join(modules)
            with open(requirements_file_path, "w") as file:
                file.write(modules_string)
            return "success"
        else:
            return None

    def install_requirements(self):
        if self.requirements_file:
            try:
                subprocess.run(
                    ["pip", "install", self.requirements_file],
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError as e:
                pip_install_error = e.stderr.decode("utf-8")
                return 1, f"{pip_install_error}"

        return 0, "success"

    def await_live(self):
        live = False
        while not live:
            try:
                requests.get(
                    f"http://{self.host}:{self.port}",
                )
                live = True
            except Exception:
                pass
