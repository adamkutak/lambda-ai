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

An expert software designer included some information
about one potential way to write this function. However, 
if you believe it is incorrect, you can ignore it:
{line_by_line}
"""


ON_CREATE_ERROR = """
Error when testing the API endpoint you passed in.
Review the original instructions, and modify your output based on the error:
{error}

Do not include any apology message or other useless text.
Make sure your function decorator and definition match the one specified in the original message.
{analysis}
"""


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
Careful with variable types when calling SQL. For strings, they need to be wrapped in ''

An expert software designer included some information
about one potential way to write this function. However, 
if you believe it is incorrect, you can ignore it:
{line_by_line}
"""

ONE_SHOT_PROMPT_FUNCTION_ARGS = {
    "imports": "import math",
    "endpoint": "@app.get('/tests/set2/')\ndef specific_power(ability: str, exponent: float) -> Dict[str, Any]:\n    base = 5 if ability.startswith('h') and ability.endswith('t') else 10\n    log_sum = math.log(sum(ord(c) for c in ability), base)\n    result = math.pow(log_sum, exponent)\n    return {'result': result}",
}

ONE_SHOT_PROMPT_WITH_DB_FUNCTION_ARGS = {
    "imports": "import math",
    "endpoint": "@app.get('/tests/sell_quantity_of_itemid/')\ndef sell_quantity_of_itemid(item_id: int, status: bool, bought: int) -> Dict[str, Any]:\n    import math\n    if status:\n        quantity = execute_sql(f'SELECT quantity FROM Items WHERE item_id = {item_id}')[0][0]\n        if quantity >= bought:\n            execute_sql(f'UPDATE Items SET quantity = quantity - {bought} WHERE item_id = {item_id}')\n            cost = bought * execute_sql(f'SELECT price FROM Items WHERE item_id = {item_id}')[0][0]\n            return {'cost': math.log10(cost)}\n        else:\n            return {'cost': 0.0}\n    else:\n        return {'cost': 0.0}\n",
}
ONE_SHOT_PROMPT_WITH_DB_FUNCTION_ARGS_2 = {
    "imports": "import math",
    "endpoint": """@app.get('/tests/sell_quantity_of_name/')\ndef sell_quantity_of_name(name: str, status: bool, bought: int) -> Dict[str, Any]:\n    import math\n    if status:\n        quantity = execute_sql(f'SELECT quantity FROM Items WHERE name = "{name}"')[0][0]\n        if quantity >= bought:\n            execute_sql(f'UPDATE Items SET quantity = quantity - {bought} WHERE name = "{name}"')\n            cost = bought * execute_sql(f'SELECT price FROM Items WHERE name = "{name}"')[0][0]\n            return {'cost': math.log10(cost)}\n        else:\n            return {'cost': 0.0}\n    else:\n        return {'cost': 0.0}\n""",
}


CHAIN_OF_THOUGHT_REASONING = """
You are an expert reasoner and designer.
Given a description of a function that should be built (and its input and outputs), 
give back a line by line description in natural language of how to build it. 
The description you provide will be given to an engineer to code in Python.
Each line should be simple and not too cmompounded. If each line tries to do too much,
the engineer will get overwhelmed by the description and fail to build it.
Only return the line by line description in natural language.

The inputs are: {inputs}
The outputs are: {outputs}

The description is:
{functionality}
"""


CHAIN_OF_THOUGHT_REASONING_WITH_DB = """
You are an expert reasoner and software architect.
Given a description of a function that should be built (and its input and outputs), 
give back a line by line description in natural language of how to build it. 
The description you provide will be given to an engineer to code in Python.
Each line should be simple and not too compounded. If each line tries to do too much,
the engineer will get overwhelmed by the description and fail to build it.
Only return the line by line description in natural language.

The inputs are: {inputs}
The outputs are: {outputs}

The description is:
{functionality}

There is also a database. The function may need to make use of it. 
The database has the following tables:
{table_list}
"""


ERROR_ANALYSIS = """
Our team ran the following python function in FastAPI:
{function_code}

It gave us back the following error: {error}

The error exists in the code. Explain in natural language what the error is. 
This will be passed back to the developer to be fixed. If you don't know 
the error, say that you don't know. Don't make one up. 
Assume that the error is internal to the function.
Also, execute_sql function is not the problem. It is valid.
"""


ONE_SHOT_SQL_GENERATION_USER = """
Your goal is to translate natural language description of database operations into valid SQL code. The SQL you generate be valid SQL.
A description of the database table will be provided. You are to only create SQL statements that interact with the columns provided in the database description.

Your goal is to translate natural language description of database operations into SQL code. 
The SQL you generate be valid SQL.
A description of the database table will be provided. 
Only create SQL statements that interact with the columns provided in the database description.

This is the natural language to translate to sql:
The database should start with 3 rows of random food names. Set the prices based on the food name's average world price. Set all quantities to 100.
After a test case is run, check to see if the quantity of the apples went down 10. 

Here is the description of the database:
Table inventory has 4 columns:
- item_id: INTEGER
  - PRIMARY KEY constraint
- name: VARCHAR(255)
  - NOT NULL constraint
- quantity: INTEGER
  - NOT NULL constraint
- price: FLOAT
  - NOT NULL constraint"""

ONE_SHOT_SQL_GENERATION_FUNCTION_ARGS = {
    "pre_sql": [
        "INSERT INTO inventory (item_id, name, quantity, price) VALUES (1, bananas, 100, 1.00)",
        "INSERT INTO inventory (item_id, name, quantity, price) VALUES (2, apples, 100, 2.00)",
        "INSERT INTO inventory (item_id, name, quantity, price) VALUES (3, pears, 100, 1.25)",
    ],
    "post_sql": [
        {
            "sql": "SELECT quantity FROM inventory WHERE item_id=2",
            "assert_value": "(90,)",
        }
    ],
}

ONE_SHOT_SQL_GENERATION_FUNCTION_ARGS_2 = {
    "pre_sql": [
        "INSERT INTO customers (first_name, verified, email, customer_id) VALUES ('Michael', True, 'mj@gmail.com', 1)",
        "INSERT INTO customers (first_name, verified, email, customer_id) VALUES ('James', False, 'coolj@hotmail.com', 2)",
        "INSERT INTO customers (first_name, verified, email, customer_id) VALUES ('Adam', True, 'doubleaagent@gmail.com', 3)",
    ],
    "post_sql": [
        {
            "sql": "SELECT COUNT(*) FROM customers WHERE verified = True",
            "assert_value": "(2,)",
        }
    ],
}

ONE_SHOT_SQL_GENERATION_FUNCTION_ARGS_3 = {
    "pre_sql": [],
    "post_sql": [
        {
            "sql": "SELECT name, price, in_stores FROM test_inventory WHERE item_id = 111",
            "assert_value": "('beets', 2.25, 0)",
        }
    ],
}

SQL_GENERATION_PROMPT = """
Your goal is to translate natural language description of database operations into SQL code. 
The SQL you generate must be valid SQL.
Only create SQL statements that interact with the columns provided in the database description provided.
Note that for any assert values, booleans should be 0s or 1s instead of False and True

This is the natural language to translate to sql:
{pre_sql}
{post_sql}

Here is the description of the database:
{db_details}"""

SQL_ON_CREATE_ERROR = """
There was an error attempting to run the SQL you generated on the provided database.
Review the original instructions, and modify your SQL based on the error:
{error}

Do not include any apology message or other useless text.
Pay attention to which part of the SQL (pre or post) failed.
"""
