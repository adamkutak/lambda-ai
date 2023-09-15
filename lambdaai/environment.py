import subprocess
import requests
import atexit
from typing import Dict
from lambdaai.utils import close_enough_float, get_imports


TEST_FOLDER = "generated_tests"

IMPORT_CODE = [
    "from fastapi import FastAPI",
    "from typing import Dict, Any",
]
FASTAPI_CODE = """
app = FastAPI()
"""
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
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "8000"


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
                    "path": "",
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

        self.build_file()

        return "success"

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

        with open(self.file_path, "w") as file:
            file.write(file_string)

        return "success"

    def black_format_file(self):
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