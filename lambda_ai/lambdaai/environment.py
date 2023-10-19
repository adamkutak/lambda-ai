import subprocess
import requests
import atexit
from typing import Dict
from .utils import get_imports
import psutil

TEST_FOLDER = "lambda_ai/generated_tests"

IMPORT_CODE = [
    "from fastapi import FastAPI, Request",
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

INTERNAL_500_RETURN_OVERRIDE = """@app.exception_handler(Exception)
async def server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )
"""

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "8005"
DEFAULT_TEST_PORT = "8010"


class APIFile:
    def __init__(
        self,
        name: str,
        file_path: str = None,
        attach_db: bool = False,
        pulling_old=False,
    ):
        self.name = name
        self.functions = {}
        self.imports = set(IMPORT_CODE)
        if not pulling_old:
            if file_path:
                self.file_path = file_path + "/" + self.name + ".py"
            else:
                self.file_path = TEST_FOLDER + "/" + self.name + ".py"
        else:
            self.file_path = file_path
        self.add_function(
            {
                "name": "exception_handler",
                "path": "exception_handler",
                "function_code": INTERNAL_500_RETURN_OVERRIDE,
                "imports": "from fastapi.responses import JSONResponse",
            }
        )

        if attach_db:
            self.add_function(
                {
                    "name": "execute_sql",
                    "path": "execute_sql",
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
    def __init__(
        self,
        api_file: APIFile,
        host: str = None,
        port: str = None,
        is_live: bool = False,
        for_testing: bool = False,
        server_process_id: int = None,
    ):
        self.api_file = api_file
        self.host = host or DEFAULT_HOST
        self.file_uvicorn = api_file.file_path.replace("/", ".").replace(".py", "")
        self.requirements_file = self.create_requirements_file()
        self.is_live = is_live
        self.server_process_id = server_process_id

        if for_testing:
            self.port = port or DEFAULT_TEST_PORT
        else:
            self.port = port or DEFAULT_PORT

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

        self.is_live = True
        self.server_process_id = self.server_process.pid
        return 0, "success"

    def undeploy(self):
        try:
            p = psutil.Process(self.server_process_id)
            p.terminate()
        except Exception as e:
            pass

        self.is_live = False
        self.server_process_id = None

        return

    def query(self, path, input):
        try:
            response = requests.get(
                f"http://{self.host}:{self.port}/{path}",  # REVIEW: Adding / after port. This means APIFunction.path should not have a / as its starting char.
                params=input,
            )
        except Exception as e:
            return e, None
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

    def find_server_process(self):
        pass
