from lambda_ai.lambdaai.sql_gen import SQLGenAgent
from lambda_ai.lambdaai.db import DB


def test_sql_1():
    test_db = DB(name="test_sql_db", replace_existing=True)

    table_columns = {
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

    test_db.add_table("inventory", table_columns)

    print("--------------------------------------------")
    print(test_db.view_table_details("inventory"))

    sql_agent = SQLGenAgent(test_db)
    nat_lang_sql = "Before the test, the database should have only one row that contains 10000 of widget1. After the test is run, there should be 9999 of widget1."
    res = sql_agent.generate_sql(nat_lang_sql, "inventory")

    print("--------------------------------------------")
    print(f"SQLAgent Response: {res}")
