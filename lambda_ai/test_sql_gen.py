import os
import openai
from dotenv import load_dotenv
from lambdaai.sql_gen import SQLGenAgent
from lambdaai.db import DB

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")


def test_sql_1():
    test_db = DB(name="test_sql_db", replace_existing=True)

    table_columns = {
        "item_id": {
            "type": "int",
            "constraints": ["PRIMARY KEY"],
        },
        "name": {
            "type": "str",
            "constraints": ["NOT NULL"],
        },
        "quantity": {
            "type": "int",
            "constraints": ["NOT NULL"],
        },
        "price": {
            "type": "float",
            "constraints": ["NOT NULL"],
        },
    }

    test_db.add_table("inventory", table_columns)

    print("--------------------------------------------")
    print(test_db.view_table_details("inventory"))

    sql_agent = SQLGenAgent(test_db)
    pre_sql = "Before the test, the database should have only one row that contains 10000 of widget1."
    post_sql = "After the test is run, there should be 9999 of widget1."
    result_code, data = sql_agent.generate_sql(pre_sql, post_sql)

    print("--------------------------------------------")
    print(f"SQLAgent Response: {data}")


def test_sql_2():
    test_db = DB(name="test_sql_db", replace_existing=True)

    customer_columns = {
        "customer_id": {
            "type": "int",
            "constraints": ["PRIMARY KEY"],
        },
        "first_name": {
            "type": "str",
            "constraints": ["NOT NULL"],
        },
        "last_name": {
            "type": "str",
            "constraints": ["NOT NULL"],
        },
        "email": {
            "type": "str",
            "constraints": ["NOT NULL", "UNIQUE"],
        },
        "phone_number": {
            "type": "str",
            "constraints": ["NOT NULL"],
        },
    }

    test_db.add_table("customers", customer_columns)

    print("--------------------------------------------")
    print(test_db.view_table_details("customers"))

    sql_agent = SQLGenAgent(test_db)
    pre_sql = "Before the test, the database should have only one row with a customer named bob. Make up the rest of the details for the row."
    post_sql = "After the test is run, check to see if bobs name was changed to james."
    result_code, data = sql_agent.generate_sql(pre_sql, post_sql)

    print("--------------------------------------------")
    print(f"SQLAgent Response: {data}")


test_sql_1()
test_sql_2()
