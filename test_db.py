from lambdaai.db import DB


def test_createdb_add_drop_tables():
    test_db = DB("my_test_db", "generated_dbs")

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

    test_db.drop_table("Employee")


test_createdb_add_drop_tables()
