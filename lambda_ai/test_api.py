from dotenv import load_dotenv
import openai
import os
from lambdaai.apis import APIFunction
from lambdaai.environment import APIEnvironment, APIFile
from lambdaai.db import DB
from lambdaai.utils import execute_sql

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")


def test_basic_1():
    repetition = 1
    build_result_list = []
    for i in range(repetition):
        api_function = APIFunction(
            "subtract_quantity",
            "/tests/set1/",
            {
                "item_id": "int",
                "status": "bool",
                "bought": "int",
            },
            {
                "item_id": "int",
                "quantity": "int",
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

        _, result_message = api_function.create_api_function()
        print("-----0------")
        print(f"i: {i}")
        print(api_function.build_attempts)
        print(result_message)
        build_result_list.append(api_function.build_attempts)

    print(build_result_list)


def test_basic_2():
    repetition = 1
    build_result_list = []
    function_def = """take the logarithm of the sum of the ascii character values of the ability input.
The base of the log is 5 if ability starts with an 'h' and ends with a 't', otherwise its 10. 
After getting the logarithm, return it to the power of exponent. 
Use the math library in this function.
"""
    test_abilities = [
        "heartquiet".encode("ascii").decode("ascii"),
        "harpoon".encode("ascii").decode("ascii"),
    ]
    for i in range(repetition):
        api_function = APIFunction(
            "specific_power",
            "/tests/set2/",
            {
                "ability": "str",
                "exponent": "float",
            },
            {
                "result": "float",
            },
            function_def,
            test_cases=[
                {
                    "input": {
                        "ability": test_abilities[0],
                        "exponent": 2,
                    },
                    "output": {
                        "result": 18.854225346913122,
                    },
                },
                {
                    "input": {
                        "ability": test_abilities[1],
                        "exponent": 0.2,
                    },
                    "output": {
                        "result": 1.2356224461821987,
                    },
                },
            ],
        )

        _, result_message = api_function.create_api_function()
        print("-----0------")
        print(f"i: {i}")
        print(api_function.build_attempts)
        print(result_message)
        build_result_list.append(api_function.build_attempts)

    print(build_result_list)


def test_basic_3():
    repetition = 1
    build_result_list = []
    function_def = """use a monte carlo simulation to approximate the area of an elipse. The inputs are the height and width of the elipse.
Use numpy's matrix functionality to speed up computation time.
"""
    for i in range(repetition):
        api_function = APIFunction(
            "elipse_area_calc",
            "/tests/elipse_calc/",
            {
                "height": "float",
                "width": "float",
            },
            {
                "result": "float",
            },
            function_def,
            test_cases=[
                {
                    "input": {
                        "height": 5.2,
                        "width": 1.36,
                    },
                    "output": {
                        "result": 5.55434,
                    },
                },
                {
                    "input": {
                        "height": 60.2,
                        "width": 60.2,
                    },
                    "output": {
                        "result": 2846.31436,
                    },
                },
                {
                    "input": {
                        "height": 0.02,
                        "width": 10,
                    },
                    "output": {
                        "result": 0.15708,
                    },
                },
            ],
        )

        _, result_message = api_function.create_api_function()
        print("-----0------")
        print(f"i: {i}")
        print(api_function.build_attempts)
        print(result_message)
        build_result_list.append(api_function.build_attempts)

    print(build_result_list)


def test_create_multiple_in_live_file():
    master_api_file = APIFile("my_end_points_test_1", "generated_apis")

    api_function_1 = APIFunction(
        "subtract_quantity",
        "/tests/set1/",
        {
            "item_id": "int",
            "status": "bool",
            "bought": "int",
        },
        {
            "item_id": "int",
            "quantity": "int",
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
    api_function_1.create_api_function()

    if api_function_1.api_function_created:
        master_api_file.add_function(api_function_1.api_function_created)
    else:
        print(f"error: function {api_function_1.name} failed to be created")

    function_def = """take the logarithm of the sum of the ascii character values of the ability input.
The base of the log is 5 if ability starts with an 'h' and ends with a 't', otherwise its 10. 
After getting the logarithm, return it to the power of exponent. 
Use the math library in this function.
"""
    test_abilities = [
        "heartquiet".encode("ascii").decode("ascii"),
        "harpoon".encode("ascii").decode("ascii"),
    ]
    api_function_2 = APIFunction(
        "specific_power",
        "/tests/set2/",
        {
            "ability": "str",
            "exponent": "float",
        },
        {
            "result": "float",
        },
        function_def,
        test_cases=[
            {
                "input": {
                    "ability": test_abilities[0],
                    "exponent": 2,
                },
                "output": {
                    "result": 18.854225346913122,
                },
            },
            {
                "input": {
                    "ability": test_abilities[1],
                    "exponent": 0.2,
                },
                "output": {
                    "result": 1.2356224461821987,
                },
            },
        ],
    )

    api_function_2.create_api_function()

    if api_function_2.api_function_created:
        master_api_file.add_function(api_function_2.api_function_created)
    else:
        print(f"error: function {api_function_2.name} failed to be created")

    master_api_env = APIEnvironment(api_file=master_api_file)

    master_api_env.deploy()
    breakpoint()  # break here and test with your browser, then continue when ready
    master_api_env.undeploy()


def test_basic_with_database_1():
    my_test_db = DB("my_test_db", "generated_dbs", replace_existing=True)
    table_1_columns = {
        "item_id": {
            "type": "INTEGER",
            "constraints": ["PRIMARY KEY"],
        },
        "name": {
            "type": "VARCHAR(255)",
            "constraints": ["NOT NULL"],
        },
        "quantity": {
            "type": "INTEGER",
            "constraints": ["NOT NULL"],
        },
        "price": {
            "type": "FLOAT",
            "constraints": ["NOT NULL"],
        },
    }
    my_test_db.add_table("Items", table_1_columns)

    insert_test_values = f"""INSERT INTO Items (item_id, name, quantity, price)\nVALUES (300, 'Apple', 600, 3.59)"""
    execute_sql(my_test_db.path, insert_test_values)

    insert_test_values = f"""INSERT INTO Items (item_id, name, quantity, price)\nVALUES (400, 'Pineapple', 15, 3.41)"""
    execute_sql(my_test_db.path, insert_test_values)

    api_function_1 = APIFunction(
        "sell_quantity",
        "/tests/sell_quantity/",
        {
            "item_id": "int",
            "status": "bool",
            "bought": "int",
        },
        {
            "cost": "float",
        },
        "if status is true, sell the bought quantity of item_id from the database. Return the logarithm (base 10) of the cost of the purchase. Use the math library to do that.",
        test_cases=[
            {
                "input": {
                    "item_id": 100,
                    "status": True,
                    "bought": 6,
                },
                "output": {
                    "cost": 0.79934,
                },
                "pre_sql": [
                    "INSERT INTO Items (item_id, name, quantity, price)\nVALUES (100, 'Banana', 57, 1.05)",
                ],
                "post_sql": [
                    {
                        "sql": "SELECT quantity FROM Items WHERE item_id=100",
                        "assert_value": 51,
                    }
                ],
            },
            {
                "input": {
                    "item_id": 200,
                    "status": False,
                    "bought": 120,
                },
                "output": {
                    "cost": 0,
                },
                "pre_sql": [
                    "INSERT INTO Items (item_id, name, quantity, price)\nVALUES (200, 'Macaroni', 450, 3.40)",
                ],
                "post_sql": [
                    {
                        "sql": "SELECT quantity FROM Items WHERE item_id=200",
                        "assert_value": 450,
                    }
                ],
            },
        ],
        attached_db=my_test_db,
    )
    api_function_1.create_api_function()
    os.remove(my_test_db.path)


def test_basic_with_database_2():
    my_test_db = DB("my_test_db", "generated_dbs", replace_existing=True)
    table_1_columns = {
        "ship_id": {
            "type": "INTEGER",
            "constraints": ["PRIMARY KEY"],
        },
        "country": {
            "type": "VARCHAR(255)",
            "constraints": ["NOT NULL"],
        },
        "weight": {
            "type": "FLOAT",
            "constraints": ["NOT NULL"],
        },
        "num_guns": {
            "type": "INTEGER",
            "constraints": ["NOT NULL"],
        },
        "num_crew": {
            "type": "INTEGER",
            "constraints": ["NOT NULL"],
        },
    }
    my_test_db.add_table("Navy", table_1_columns)

    insert_test_values = f"""INSERT INTO Navy (ship_id, country, weight, num_guns, num_crew)\nVALUES (11, 'Canada', 150, 8, 45)"""
    execute_sql(my_test_db.path, insert_test_values)

    insert_test_values = f"""INSERT INTO Navy (ship_id, country, weight, num_guns, num_crew)\nVALUES (21, 'China', 500, 40, 315)"""
    execute_sql(my_test_db.path, insert_test_values)

    api_function_1 = APIFunction(
        "add_crew_to_navy",
        "/tests/add_crew/",
        {
            "country": "str",
            "active": "bool",
            "gun_preference": "int",
        },
        {
            "ship_id": "int",
        },
        "given a new crewmember of a certain country, if they are an active crewmember, add them to the crew of the ship of their countries navy with the number of guns closest to their gun_preference. Return the ship_id of the ship they are assigned.",
        test_cases=[
            {
                "input": {
                    "country": "Canada",
                    "active": True,
                    "gun_preference": 17,
                },
                "output": {
                    "ship_id": 12,
                },
                "pre_sql": [
                    "INSERT INTO Navy (ship_id, country, weight, num_guns, num_crew)\nVALUES (12, 'Canada', 300.442, 22, 120)",
                ],
                "post_sql": [
                    {
                        "sql": "SELECT num_crew FROM Navy WHERE ship_id=12",
                        "assert_value": 121,
                    }
                ],
            },
            {
                "input": {
                    "country": "China",
                    "active": False,
                    "gun_preference": 18,
                },
                "output": {
                    "ship_id": 0,
                },
                "pre_sql": [],
                "post_sql": [
                    {
                        "sql": "SELECT num_crew FROM Navy WHERE ship_id=21",
                        "assert_value": 315,
                    }
                ],
            },
        ],
        attached_db=my_test_db,
    )
    api_function_1.create_api_function()
    os.remove(my_test_db.path)


def test_basic_1_autogenerate_tests():
    repetition = 1
    build_result_list = []
    for i in range(repetition):
        api_function = APIFunction(
            "subtract_quantity",
            "/tests/set1/",
            {
                "item_id": "int",
                "status": "bool",
                "bought": "int",
            },
            {
                "item_id": "int",
                "quantity": "int",
            },
            "quantity is 100. If status is true, deduct bought from quantity.",
            test_cases=[],
        )

        _, result_message = api_function.create_api_function()
        print("-----0------")
        print(f"i: {i}")
        print(api_function.build_attempts)
        print(result_message)
        build_result_list.append(api_function.build_attempts)

    print(build_result_list)


def test_basic_2_autogenerate_tests():
    repetition = 1
    build_result_list = []
    function_def = """take the logarithm of the sum of the ascii character values of the ability input.
The base of the log is 5 if ability starts with an 'h' and ends with a 't', otherwise its 10. 
After getting the logarithm, return it to the power of exponent. 
Use the math library in this function.
"""
    for i in range(repetition):
        api_function = APIFunction(
            "specific_power",
            "/tests/set2/",
            {
                "ability": "str",
                "exponent": "float",
            },
            {
                "result": "float",
            },
            function_def,
            test_cases=[],
        )

        _, result_message = api_function.create_api_function()
        print("-----0------")
        print(f"i: {i}")
        print(api_function.build_attempts)
        print(result_message)
        build_result_list.append(api_function.build_attempts)

    print(build_result_list)


def test_basic_with_database_1_autogenerate_tests():
    my_test_db = DB("my_test_db", "generated_dbs", replace_existing=True)
    table_1_columns = {
        "item_id": {
            "type": "INTEGER",
            "constraints": ["PRIMARY KEY"],
        },
        "name": {
            "type": "VARCHAR(255)",
            "constraints": ["NOT NULL"],
        },
        "quantity": {
            "type": "INTEGER",
            "constraints": ["NOT NULL"],
        },
        "price": {
            "type": "FLOAT",
            "constraints": ["NOT NULL"],
        },
    }
    my_test_db.add_table("Items", table_1_columns)

    insert_test_values = f"""INSERT INTO Items (item_id, name, quantity, price)\nVALUES (300, 'Apple', 600, 3.59)"""
    execute_sql(my_test_db.path, insert_test_values)

    insert_test_values = f"""INSERT INTO Items (item_id, name, quantity, price)\nVALUES (400, 'Pineapple', 15, 3.41)"""
    execute_sql(my_test_db.path, insert_test_values)

    api_function_1 = APIFunction(
        "sell_quantity",
        "/tests/sell_quantity/",
        {
            "item_id": "int",
            "status": "bool",
            "bought": "int",
        },
        {
            "cost": "float",
        },
        "if status is true, sell the bought quantity of item_id from the database. Return the logarithm (base 10) of the cost of the purchase. Use the math library to do that.",
        test_cases=[],
        attached_db=my_test_db,
    )
    api_function_1.create_api_function()
    os.remove(my_test_db.path)


test_basic_1()
test_basic_2()
test_create_multiple_in_live_file()
test_basic_with_database_1()
test_basic_with_database_2()
# test_basic_1_autogenerate_tests()
# test_basic_2_autogenerate_tests()
# test_basic_with_database_1_autogenerate_tests()
