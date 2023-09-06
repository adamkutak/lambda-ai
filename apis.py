import openai
from prompts import (
    CREATE_ENDPOINT,
    ON_CREATE_ERROR,
    FUNCTION_CALLING_ENDPOINT_CREATION,
    CREATE_ENDPOINT_WITH_FUNCTION_DEFINITION,
)
import json
from dotenv import load_dotenv
import os
from gpt_management import openai_chat_response
import subprocess
import requests
import atexit
import pprint

# COMPLETE:
# Check for valid python code: use black formatting, seems to work perfectly
# JSON returning: seems to work fine 99%? Very occasional we get weird errors with "incorrect delimiter" or similar.
# - seems like the error handling can fix it though.

# TODO:
# Create fastAPI function definition via templates. Don't generate it with AI.
# test reliability, find more possible errors that can arise and patch them.
# turn some repetitive code into callable functions and add more class structure
# If we fail to create the function, the code should try again starting from scratch (new message history)
# - We can even get gpt-4 to rewrite the prompt and then try again?

# TODO (MAJOR STEPS):
# automatically pip install the requirements.
# Use Chain of thought reasoning for more complex functions. Break them down into smaller components
# Build a tool that lets you upload external interface documentation with the necessary API keys.
# - Generated functions can then incorporate these API's
# Add support for making databases, to create stateful APIs.


API_FOLDER = "generated_apis"
TEST_FOLDER = "generated_tests"
API_FILE_LOCATION = "created_apis.py"


FASTAPI_SPLIT_CODE = """
# --xyz123--
app = FastAPI()

# --xyz123--
"""

BASE_IMPORTS = """
from fastapi import FastAPI
from typing import Dict, Any
"""

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "8000"

MAX_TEST_CHANCES = 4


# make an API with fast API
def create_api(
    name: str,
    path: str,
    inputs: dict,
    outputs: dict,
    functionality: str,
    test_cases: list[dict],
    is_async: bool = False,
) -> str:
    function_def = generate_fastapi_definition(
        name,
        path,
        inputs,
        outputs,
        is_async,
    )

    data = {
        "prompt": CREATE_ENDPOINT_WITH_FUNCTION_DEFINITION.format(
            function_def=function_def,
            inputs=str(inputs),
            outputs=str(outputs),
            functionality=functionality,
        ),
        # "prompt": CREATE_ENDPOINT.format(
        #     name=name,
        #     path=path,
        #     inputs=str(inputs),
        #     outputs=str(outputs),
        #     functionality=functionality,
        # ),
        "model": "gpt-3.5-turbo-0613",
        "system_message": "Only use the functions you have been provided with.",  # noqa
        "functions": [FUNCTION_CALLING_ENDPOINT_CREATION],
        "function_call": "create_api",
    }
    result_messages = openai_chat_response(**data)

    test_result = None
    attempt_count = 0
    while test_result != "success" and attempt_count <= MAX_TEST_CHANCES:
        attempt_count += 1
        if (
            result_messages[-1].get("function_call")
            and result_messages[-1].function_call.name == "create_api"
        ):
            try:
                breakpoint()
                new_function = json.loads(
                    result_messages[-1].function_call.arguments,
                    strict=False,
                )
                imports = new_function["imports"]
                function = new_function["endpoint"]
                # function = function.replace("def", "def def")  # TEST TOOL TO CAUSE INVALID PYTHON # noqa
            except Exception as e:
                test_result = f"Error decoding your JSON function call. Error: {e}, make sure you provide a valid function call in JSON format."  # noqa
            else:
                if "def" in function or "@app" in function:
                    test_result = "Error: function definition or FastAPI decorator detected. Do not include these in your code."
                else:
                    function = (
                        function_def + "\t" + function.replace("\n", "\n\t")
                    )  # noqa
                    test_result = test_api(
                        imports,
                        function,
                        name,
                        path,
                        test_cases,
                    )
        else:
            test_result = "Error, you did not use a valid function call. Use the create_api function to pass in and test the code you generated."  # noqa

        print(result_messages[-1].function_call)
        print(test_result)
        if test_result != "success":
            data = {
                "prompt": ON_CREATE_ERROR.format(error=test_result),
                "model": "gpt-3.5-turbo-0613",
                "existing_messages": result_messages,
                "functions": [FUNCTION_CALLING_ENDPOINT_CREATION],
                "function_call": "create_api",
            }
            result_messages = openai_chat_response(**data)

    # add_api(imports, function)
    # server_pid = deploy_apis()
    return test_result


def generate_fastapi_definition(
    name: str,
    path: str,
    inputs: dict,
    outputs: dict,
    is_async: bool,
):
    # check that everything is validly named firstly.
    assert name.isidentifier()
    assert path.replace("/", "").isalnum()
    for input in inputs.keys():
        assert input.isidentifier()
    for output in outputs.keys():
        assert output.isidentifier()

    input_def = ", ".join(
        [f"{key}: {value.__name__}" for key, value in inputs.items()],
    )

    decorator = f"@app.get('{path}')"
    function = f"{'async ' if is_async else ''}def {name}({input_def}) -> Dict[str, Any]:\n"  # noqa
    function_def = "\n".join([decorator, function])
    function_def.replace("\n ", "\n")

    return function_def


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
    test_cases: list[dict],
):
    file_name = f"{name}.py"
    testable_python_file_string = "\n".join(
        [
            BASE_IMPORTS,
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

    test_file_uvicorn = TEST_FOLDER + "." + file_name.replace(".py", "")

    # FORMAT API (SERVES TO CHECK FOR VALID PYTHON CODE AS WELL)
    try:
        subprocess.run(
            ["black", test_file_location],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        black_subprocess_error = e.stderr.decode("utf-8")
        return f"{black_subprocess_error}. Python is likely invalid."

    # DEPLOY API
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

        # wait until its live before continuing
        live = False
        while not live:
            try:
                requests.get(
                    f"http://{DEFAULT_HOST}:{DEFAULT_PORT}",
                )
                live = True
            except Exception:
                pass
    except Exception as e:
        return f"error starting api deployment: {e}"

    # RUN TEST CASES
    for test_case in test_cases:
        try:
            response = requests.get(
                f"http://{DEFAULT_HOST}:{DEFAULT_PORT}{path}",
                params=test_case["input"],
            )
        except Exception as e:
            undeploy_apis(server_process.pid)
            return f"error on test case: {str(test_case)}, error: {e}"

        if response.status_code >= 400:
            undeploy_apis(server_process.pid)
            return f"error on test case: {str(test_case)}, error: {response.reason}"  # noqa

        test_output = response.json()
        if test_output != test_case["output"]:
            undeploy_apis(server_process.pid)
            return f"error on test case: {str(test_case['input'])}, expected output is: {str(test_case['output'])}. Actual output is {str(test_output)}"  # noqa

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

    # wait until its live before returning
    live = False
    while not live:
        try:
            requests.get(
                f"http://{DEFAULT_HOST}:{DEFAULT_PORT}",
            )
            live = True
        except Exception:
            pass

    return server_process.pid


# kill the server
def undeploy_apis(pid: int):
    subprocess.run(["kill", str(pid)])


load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

repetition = 10
for i in range(repetition):
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
