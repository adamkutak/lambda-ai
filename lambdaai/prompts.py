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
It is essential that your function calls are valid JSON.
Call the create_api function with the two arguments:
"imports": python code of the imports section. Can be empty if not needed.
"endpoint": python code for the FastAPI API endpoint function, including the decorator.
It is essential that you include the FastAPI decorator.
Do not import FastAPI. 
Do not add any comments. 

The name of the endpoint is {name}, the url path is {path}
The endpoint function takes in the following parameters: {inputs}
you can decide to use path or query parameters for the inputs.
the endpoint function outputs the following: {outputs}

This is the description of the endpoint function:
{functionality}

The function decorator and definition must be the following:
{function_def}
"""


ON_CREATE_ERROR = """
Error when testing the API endpoint you passed in.
Review the original instructions, and modify your output based on the error:
{error}

Do not include any apology message or other useless text.
Make sure your function decorator and definition match the one specified in the original message.

"""

ONE_SHOT_PROMPT_USER = """
Your goal is to create a Python FastAPI API endpoint.
It is essential that your function calls are valid JSON.
Call the create_api function with the two arguments:
"imports": python code of the imports section. Can be empty if not needed.
"endpoint": python code for the FastAPI API endpoint function, including the
decorator.
It is essential that you include the FastAPI decorator.
Do not import FastAPI.
Do not add any comments.

The name of the endpoint is specific_power, the url path is /tests/set2/
The endpoint function takes in the following parameters: {'ability': 'str', 'exponent': 'float'}
you can decide to use path or query parameters for the inputs.
the endpoint function outputs the following: {'result': 'float'}

This is the description of the endpoint function:
take the logarithm of the sum of the ascii character values of the ability
input.
The base of the log is 5 if ability starts with an 'h' and ends with a 't', otherwise its 10.
After getting the logarithm, return it to the power of exponent.
Use the math library in this function.


The function decorator and definition must be the following:
@app.get('/tests/set2/')
def specific_power(ability: str, exponent: float) -> Dict[str, Any]:

"""

ONE_SHOT_PROMPT_FUNCTION_ARGS = {
    "imports": "import math",
    "endpoint": "@app.get('/tests/set2/')\ndef specific_power(ability: str, exponent: float) -> Dict[str, Any]:\n    base = 5 if ability.startswith('h') and ability.endswith('t') else 10\n    log_sum = math.log(sum(ord(c) for c in ability), base)\n    result = math.pow(log_sum, exponent)\n    return {'result': result}",
}

CREATE_ENDPOINT_WITH_DB = """
Your goal is to create a Python FastAPI API endpoint.
It is essential that your function calls are valid JSON.
Call the create_api function with the two arguments:
"imports": python code of the imports section. Can be empty if not needed.
"endpoint": python code for the FastAPI API endpoint function, including the decorator.
It is essential that you include the FastAPI decorator.
Do not import FastAPI. 
Do not add any comments.

The name of the endpoint is {name}, the url path is {path}
The endpoint function takes in the following parameters: {inputs}
you can decide to use path or query parameters for the inputs.
the endpoint function outputs the following: {outputs}

This is the description of the endpoint function:
{functionality}

The function decorator and definition must be the following:
{function_def}

There is also a database with the following tables:
{table_list}

your function may need to perform an SQL operation on one or more of these tables.
To do some operation on a table (for example, to add, change, or get a row, or create a new column),
your python code can call the function execute_sql(VALID_SQL_STRING) where VALID_SQL_STRING is valid SQL.
If using a sql SELECT statement, the return value of execute_sql is a list of tuples, where each tuple is a row.
If you need to run multiple queries, put each query in a seperate execute_sql() call.
Do not try to import the execute_sql function. Assume it exists and is usable already.
"""
