CREATE_ENDPOINT = """
Your goal is to create a Python FastAPI API endpoint.
You will return a json object with two elements:
"imports": python code of the imports section. Can be empty if not needed.
"function": python code for the FastAPI API endpoint function, including the decorator.
It is essential that you include the FastAPI decorator.
Your response is going to be parsed automatically into a JSON object, so return nothing except the valid json.
Do not import FastAPI.

The name of the endpoint is {name}, the url path is {path}
The function takes in the following parameters: {inputs}
you can decide to use path or query parameters for the inputs.
the function outputs the following: {outputs}

This is the description of the endpoint function:
{functionality}
"""
