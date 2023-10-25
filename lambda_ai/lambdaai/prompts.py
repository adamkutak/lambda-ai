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

ONE_SHOT_PROMPT_USER_WITH_DB = """
Your goal is to create a Python FastAPI API endpoint.
It is essential that your function calls are valid JSON.
Call the create_api function with the two arguments:
"imports": python code of the imports section. Can be empty if not needed.
"endpoint": python code for the FastAPI API endpoint function, including the decorator.
It is essential that you include the FastAPI decorator.
Do not import FastAPI. 
Do not add any comments.

The name of the endpoint is sell_quantity, the url path is /tests/sell_quantity/
The endpoint function takes in the following parameters: {'item_id': 'int', 'status': 'bool', 'bought': 'int'}
you can decide to use path or query parameters for the inputs.
the endpoint function outputs the following: {'cost': 'float'}

This is the description of the endpoint function:
if status is true, sell the bought quantity of item_id from the database. Return the logarithm (base 10) of the cost of the purchase. Use the math library to do that.

The function decorator and definition must be the following:
@app.get('/tests/sell_quantity/')
def sell_quantity(item_id: int, status: bool, bought: int) -> Dict[str, Any]:


There is also a database with the following tables:
Table Items has 4 columns:
- item_id: INTEGER
  - PRIMARY KEY constraint
- name: VARCHAR(255)
  - NOT NULL constraint
- quantity: INTEGER
  - NOT NULL constraint
- price: FLOAT
  - NOT NULL constraint
Sample of Table Items rows:
(100, 'Banana', 57, 1.05)
(200, 'Macaroni', 450, 3.4)


your function may need to perform an SQL operation on one or more of these tables.
To do some operation on a table (for example, to add, change, or get a row, or create a new column),
your python code can call the function execute_sql(VALID_SQL_STRING) where VALID_SQL_STRING is valid SQL.
If using a sql SELECT statement, the return value of execute_sql is a list of tuples, where each tuple is a row.
If you need to run multiple queries, put each query in a seperate execute_sql() call.
Do not try to import the execute_sql function. Assume it exists and is usable already.
Careful with variable types when calling SQL. For strings, they need to be wrapped in ''
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
"""

ONE_SHOT_PROMPT_FUNCTION_ARGS = {
    "imports": "import math",
    "endpoint": "@app.get('/tests/set2/')\ndef specific_power(ability: str, exponent: float) -> Dict[str, Any]:\n    base = 5 if ability.startswith('h') and ability.endswith('t') else 10\n    log_sum = math.log(sum(ord(c) for c in ability), base)\n    result = math.pow(log_sum, exponent)\n    return {'result': result}",
}

ONE_SHOT_PROMPT_WITH_DB_FUNCTION_ARGS = {
    "imports": "import math",
    "endpoint": "@app.get('/tests/sell_quantity/')\ndef sell_quantity(item_id: int, status: bool, bought: int) -> Dict[str, Any]:\n    import math\n    if status:\n        quantity = execute_sql(f'SELECT quantity FROM Items WHERE item_id = {item_id}')[0][0]\n        if quantity >= bought:\n            execute_sql(f'UPDATE Items SET quantity = quantity - {bought} WHERE item_id = {item_id}')\n            cost = bought * execute_sql(f'SELECT price FROM Items WHERE item_id = {item_id}')[0][0]\n            return {'cost': math.log10(cost)}\n        else:\n            return {'cost': 0.0}\n    else:\n        return {'cost': 0.0}\n",
}


AUTO_TESTER_BUILD_PROMPT = """
You are an expert test case builder for FastAPI endpoints.
You must use the "add_test" function given to you. Your function call must be valid JSON.
You will create a new test case for the following endpoint, named {name}:
The inputs are: {inputs}
The outputs are: {outputs}

This is the description of the endpoint:
{functionality}

For the test case, you must give inputs and outputs that test the endpoint works correctly.
Do not create test cases that go outside the core functionality of the test case.{ext_str}
"""

AUTO_TESTER_DATABASE_EXT = """
This endpoint also uses a database. You must generate the SQL tests in coordination with the input/output test you generate.
You do this by adding test rows with sql before the endpoint runs with the pre_sql list parameter.
Then, after the endpoint runs, the post_sql sql will be run, and we will assert the output matches the assert_value.
Use post_sql to verify that the database was updated or modified correctly when the function is tested with the inputs.
Your function call of add_test should return the inputs, outputs, pre_sql, and post_sql. Do not forget to include any of those, they are all required.
Be very cautious when inserting new rows. If doing so, use highly random primary_keys of at least 12 digits/characters.
Here is an overview of the database:
{database_info}
"""

AUTO_TESTER_ON_ERROR = """
Error on creating test data. The error message is the following:
{error}

Please retry. 
"""

AUTO_TESTER_ONESHOT_ARGS = {
    "input": {"item_id": 1, "status": True, "bought": 80},
    "output": {"item_id": 1, "quantity": 20},
}

AUTO_TESTER_ONESHOT_PROMPT = """
You are an expert test case builder for FastAPI endpoints.
You must use the "add_test" function given to you. Your function call must be valid JSON.
You will create a new test case for the following endpoint, named subtract_quantity:
The inputs are: {'item_id': 'int', 'status': 'bool', 'bought': 'int'}
The outputs are: {'item_id': 'int', 'quantity': 'int'}

This is the description of the endpoint:
quantity is 100. If status is true, deduct bought from quantity.

For the test case, you must give inputs and outputs that test the endpoint works correctly.
Do not create test cases that go outside the core functionality of the test case.
"""

AUTO_TESTER_WITH_DB_ONESHOT_ARGS = {
    "input": {"item_id": 1, "status": True, "bought": 80},
    "output": {"item_id": 1, "quantity": 20},
}

AUTO_TESTER_WITH_DB_ONESHOT_PROMPT = """
You are an expert test case builder for FastAPI endpoints.
You must use the "add_test" function given to you. Your function call must be valid JSON.
You will create a new test case for the following endpoint, named sell_quantity:
The inputs are: {'item_id': 'int', 'status': 'bool', 'bought': 'int'}
The outputs are: {'cost': 'float'}

This is the description of the endpoint:
if status is true, sell the bought quantity of item_id from the database. Return the logarithm (base 10) of the cost of the purchase. Use the math library to do that.

For the test case, you must give inputs and outputs that test the endpoint works correctly.
Do not create test cases that go outside the core functionality of the test case.
This endpoint also uses a database. You must generate the SQL tests in coordination with the input/output test you generate.
You do this by adding test rows with sql before the endpoint runs with the pre_sql list parameter.
Then, after the endpoint runs, the post_sql sql will be run, and we will assert the output matches the assert_value.
Here is an overview of the database:
Table Items has 4 columns:
- item_id: INTEGER
  - PRIMARY KEY constraint
- name: VARCHAR(255)
  - NOT NULL constraint
- quantity: INTEGER
  - NOT NULL constraint
- price: FLOAT
  - NOT NULL constraint
Sample of Table Items rows:
(300, 'Apple', 600, 3.59)
(400, 'Pineapple', 15, 3.41)

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
        "INSERT INTO inventory VALUES (1, bananas, 100, 1.00)",
        "INSERT INTO inventory VALUES (2, apples, 100, 2.00)",
        "INSERT INTO inventory VALUES (3, pears, 100, 2.25)",
    ],
    "post_sql": [
        {
            "sql": "SELECT quantity FROM inventory WHERE item_id=2;",
            "assert_value": "90",
        }
    ],
}

SQL_GENERATION_PROMPT = """
Your goal is to translate natural language description of database operations into SQL code. 
The SQL you generate must be valid SQL.
Only create SQL statements that interact with the columns provided in the database description provided.

This is the natural language to translate to sql:
{pre_sql}
{post_sql}


Here is the description of the database:
{db_details}"""
