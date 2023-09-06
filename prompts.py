# CREATE_ENDPOINT = """
# Your goal is to create a Python FastAPI API endpoint.
# You will return a json object with two elements:
# "imports": python code of the imports section. Can be empty if not needed.
# "endpoint": python code for the FastAPI API endpoint function, including the decorator.
# It is essential that you include the FastAPI decorator.
# Your response is going to be parsed automatically into a JSON object, so return nothing except the valid json.
# Do not import FastAPI.

# The name of the endpoint is {name}, the url path is {path}
# The function takes in the following parameters: {inputs}
# you can decide to use path or query parameters for the inputs.
# the function outputs the following: {outputs}

# This is the description of the endpoint function:
# {functionality}
# """


# ON_CREATE_ERROR = """
# Error when testing the function.
# Review the original instructions, and modify your output based on the error:
# {error}

# Do not return anything except the JSON object with "imports" and "endpoint".
# Do not include any apology message or other useless text.
# """

FUNCTION_CALLING_ENDPOINT_CREATION = {
    "name": "create_api",
    "description": "Create a new API endpoint and test it. If an error occurs during testing, the error will be returned to you.",
    "parameters": {
        "type": "object",
        "properties": {
            "imports": {
                "type": "string",
                "description": "the python code to import the necessary requirements.",
            },
            "endpoint": {
                "type": "string",
                "description": "the python code for your FastAPI endpoint. It must include the decorator and function definition",
            },
        },
        "required": ["imports", "endpoint"],
    },
}


CREATE_ENDPOINT = """
Your goal is to create a Python FastAPI API endpoint.
Call the create_api function with the two arguments:
"imports": python code of the imports section. Can be empty if not needed.
"endpoint": python code for the FastAPI API endpoint function, including the decorator.
It is essential that you include the FastAPI decorator.
Do not import FastAPI.

The name of the endpoint is {name}, the url path is {path}
The function takes in the following parameters: {inputs}
you can decide to use path or query parameters for the inputs.
the function outputs the following: {outputs}

This is the description of the endpoint function:
{functionality}
"""


ON_CREATE_ERROR = """
Error when testing the API endpoint you passed in.
Review the original instructions, and modify your function call based on the error:
{error}

Do not include any apology message or other useless text.
Do not include the function definition in your output.
"""

CREATE_ENDPOINT_WITH_FUNCTION_DEFINITION = """
You are an expert programmer. You need to fill in the following python function.

This is a user created FastAPI function definition. Never include this in your function call or output.
{function_def}

The user has supplied this explanation of what the function should do:
{functionality}

the inputs are: {inputs}
the outputs are: {outputs}

The function's return object must be a dictionary, as per FastAPI standards.
Call the create_api function with the two arguments:
"imports": python code of the imports section. Can be empty if not needed.
"endpoint": python code for the FastAPI API endpoint function.

Do not include the function definition in the endpoint code, just give the code inside the function.
Do not include FastAPI in the imports section.
"""
