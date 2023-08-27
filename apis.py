import openai
from prompts import CREATE_ENDPOINT
import json
from dotenv import load_dotenv
import os
from gpt_management import openai_chat_response
import subprocess

API_FILE_LOCATION = "created_apis.py"

FASTAPI_SPLIT_CODE = """
# --xyz123--
app = FastAPI()

# --xyz123--
"""


# make an API with fast API
def create_api(
    name: str,
    path: str,
    inputs: dict,
    outputs: dict,
    functionality: str,
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

    test_api(imports, function)
    add_api(imports, function)

    deploy_apis()

    breakpoint()


# add the API to the existing set of APIs
def add_api(new_imports: str, new_function: str):
    with open(API_FILE_LOCATION, "r") as fr:
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

    with open(API_FILE_LOCATION, "w") as fw:
        fw.write(updated_api_file)

    subprocess.run(["black", API_FILE_LOCATION])  # black formatting

    return "success"


# test out the API
def test_api(new_imports: str, new_function: str):
    return "success"


# deploy the API
def deploy_apis():
    ret_obj = subprocess.Popen(["uvicorn", "created_apis:app"])

    return ret_obj.pid


# kill the server
def undeploy_apis(pid: int):
    subprocess.run(["kill", str(pid)])


load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
# status = create_api(
#     "test_func",
#     "/tests/set1/",
#     {
#         "item_id": int,
#         "status": bool,
#         "bought": int,
#     },
#     {
#         "item_id": int,
#         "quantity": int,
#     },
#     "quantity is 100. If status is true, deduct bought from quantity.",
# )
server_pid = deploy_apis()
breakpoint()
undeploy_apis(server_pid)
