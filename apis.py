import openai
from prompts import CREATE_ENDPOINT
import json
from dotenv import load_dotenv
import os
from gpt_management import openai_chat_response
import subprocess
import requests
import atexit

# TODO:
# 1. theres an Occasional bug with the port number, even though it claims to be hosted on port 8000
# the requests library can't find it. However, I can access it at port 8000 on my browser

API_FOLDER = "generated_apis"
TEST_FOLDER = "generated_tests"
API_FILE_LOCATION = "created_apis.py"


FASTAPI_SPLIT_CODE = """
# --xyz123--
app = FastAPI()

# --xyz123--
"""

FAST_API_IMPORT = "from fastapi import FastAPI\n"

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "8000"


# make an API with fast API
def create_api(
    name: str,
    path: str,
    inputs: dict,
    outputs: dict,
    functionality: str,
    test_cases: list[dict],
) -> str:
    data = {
        "prompt": CREATE_ENDPOINT.format(
            name=name,
            path=path,
            inputs=str(inputs),
            outputs=str(outputs),
            functionality=functionality,
        ),
        "model": "gpt-3.5-turbo",
    }
    result_messages = openai_chat_response(**data)

    try:
        new_function = json.loads(result_messages[-1].content)
        imports = new_function["imports"]
        function = new_function["function"]
    except Exception as e:
        return f"error: {e}"

    test_result = test_api(imports, function, name, path, inputs, outputs, test_cases)
    breakpoint()
    # add_api(imports, function)

    # server_pid = deploy_apis()

    return "success"


# add the API to the existing set of APIs
def add_api(new_imports: str, new_function: str):
    api_location = API_FOLDER + "/" + API_FILE_LOCATION
    with open(api_location, "r") as fr:
        existing_code = fr.read()
    code_list = existing_code.split(
        "# --xyz123--",  # we use this marker to split the existing code
        2,
    )
    if len(code_list) != 3:
        return "error: couldn't split code 3 ways"

    existing_imports = code_list[0]
    if new_imports:
        new_imports = new_imports.split("\n")
        existing_imports = existing_imports.split("\n")
        updated_imports = "/n".join(set(new_imports + existing_imports))
    else:
        updated_imports = existing_imports

    functions = code_list[2] + "\n\n" + new_function

    updated_api_file_set = [updated_imports, FASTAPI_SPLIT_CODE, functions]
    updated_api_file = "\n".join(updated_api_file_set)

    with open(api_location, "w") as api_file:
        api_file.write(updated_api_file)

    subprocess.run(["black", api_location])  # black formatting

    return "success"


# test out the API
def test_api(
    new_imports: str,
    new_function: str,
    name: str,
    path: str,
    inputs: dict,
    outputs: dict,
    test_cases: list[dict],
):
    file_name = f"{name}.py"
    testable_python_file_string = "\n".join(
        [
            FAST_API_IMPORT,
            new_imports,
            "\n",
            FASTAPI_SPLIT_CODE,
            "\n",
            new_function,
        ]
    )

    test_file_location = TEST_FOLDER + "/" + file_name
    with open(test_file_location, "w") as test_file:
        test_file.write(testable_python_file_string)

    subprocess.run(["black", test_file_location])  # black formatting

    test_file_uvicorn = TEST_FOLDER + "." + file_name.replace(".py", "")

    try:
        server_process = subprocess.Popen(
            [
                "uvicorn",
                "--host",
                DEFAULT_HOST,
                "--port",
                DEFAULT_PORT,
                f"{test_file_uvicorn}:app",
            ],
        )
        atexit.register(server_process.terminate)
    except Exception as e:
        return f"error starting api deployment: {e}"

    # now run the test cases
    for test_case in test_cases:
        try:
            response = requests.get(
                f"http://{DEFAULT_HOST}:{DEFAULT_PORT}{path}",
                params=test_case["input"],
            )
        except Exception as e:
            return f"error on test case: {str(test_case)}, error: {e}"

        test_output = response.json()
        if test_output != test_case["output"]:
            return f"error on test case: {str(test_case['input'])}, expected output is: {str(test_case['output'])}. Actual output is {str(test_output)}"

    undeploy_apis(server_process.pid)

    return "success"


# deploy the API
def deploy_apis():
    api_location = API_FOLDER + "." + API_FILE_LOCATION.replace(".py", "")
    server_process = subprocess.Popen(
        [
            "uvicorn",
            "--host",
            DEFAULT_HOST,
            "--port",
            DEFAULT_PORT,
            f"{api_location}:app",
        ],
    )
    atexit.register(server_process.terminate)

    return server_process.pid


# kill the server
def undeploy_apis(pid: int):
    subprocess.run(["kill", str(pid)])


load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
status = create_api(
    "test_func2",
    "/tests/set2/",
    {
        "item_id": int,
        "status": bool,
        "bought": int,
    },
    {
        "item_id": int,
        "quantity": int,
    },
    "quantity is 100. If status is true, deduct bought from quantity.",
    test_cases=[
        {
            "input": {
                "item_id": 9478,
                "status": True,
                "bought": 99,
            },
            "output": {
                "item_id": 9478,
                "quantity": 1,
            },
        },
        {
            "input": {
                "item_id": 1234,
                "status": False,
                "bought": 99,
            },
            "output": {
                "item_id": 1234,
                "quantity": 100,
            },
        },
        {
            "input": {
                "item_id": 645609,
                "status": True,
                "bought": 105,
            },
            "output": {
                "item_id": 645609,
                "quantity": -5,
            },
        },
    ],
)
print(status)
