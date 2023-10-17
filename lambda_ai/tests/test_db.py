from lambdaai.db import DB
import os


def test_createdb_add_drop_tables():
    test_db = DB("my_test_db", "generated_dbs", replace_existing=True)

    table_1_columns = {
        "item_id": {
            "type": "INTEGER",
            "constraints": ["PRIMARY KEY"],
        },
        "quantity": {
            "type": "INTEGER",
            "constraints": ["NOT NULL"],
        },
        "weight": {
            "type": "FLOAT",
            "constraints": ["NOT NULL"],
        },
    }
    table_2_columns = {
        "id": {
            "type": "INTEGER",
            "constraints": ["PRIMARY KEY"],
        },
        "name": {
            "type": "VARCHAR(255)",
            "constraints": ["NOT NULL"],
        },
        "title": {
            "type": "VARCHAR(255)",
            "constraints": ["NOT NULL"],
        },
    }

    test_db.add_table("Items", table_1_columns)
    test_db.add_table("Employee", table_2_columns)

    table_1_view = test_db.view_table_details("Items")
    table_2_view = test_db.view_table_details("Employee")

    print("--------------------------------------------")
    print(table_1_view)
    print("--------------------------------------------")
    print(table_2_view)
    print("--------------------------------------------")

    test_db.drop_table("Items")
    test_db.drop_table("Employee")

    os.remove(test_db.path)


test_createdb_add_drop_tables()
