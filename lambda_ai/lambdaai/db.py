import sqlite3
import os

DEFAULT_DB_PATH = "lambda_ai/generated_dbs"
MAX_ROWS_TO_DISPLAY = 3

SQL_type_conversion = {
    "str": "VARCHAR(255)",
    "int": "INTEGER",
    "float": "FLOAT",
    "bool": "BOOL",
}


class DB:
    def __init__(
        self,
        name,
        location: str = None,
        replace_existing: bool = False,
    ):
        db_name = f"{name}.db"

        self.name = db_name
        location = location or DEFAULT_DB_PATH
        self.path = location + "/" + db_name
        self.test_db_path = location + "/test_dbs/" + db_name
        self.table_names = []

        # TODO: temporarily removing existing file for ease of use...
        if replace_existing:
            curr_dbs_at_path = os.listdir(location)
            if db_name in curr_dbs_at_path:
                os.remove(self.path)
            curr_dbs_at_test_path = os.listdir(location + "/test_dbs")
            if db_name in curr_dbs_at_test_path:
                os.remove(self.test_db_path)

    def add_table(
        self,
        name: str,
        columns: dict,
    ):
        assert name.isidentifier()
        assert name not in self.table_names

        connection = sqlite3.connect(self.path)
        crsr = connection.cursor()

        create_table_sql = f"CREATE TABLE {name} ("

        for col_name, col_info in columns.items():
            col_type = SQL_type_conversion[col_info["type"]]
            col_constraints = " ".join(col_info["constraints"])
            create_table_sql += f"{col_name} {col_type} {col_constraints}, "

        create_table_sql = create_table_sql[:-2] + ")"
        crsr.execute(create_table_sql)

        connection.commit()
        connection.close()

        self.table_names.append(name)

    def drop_table(self, name: str):
        assert name in self.table_names

        connection = sqlite3.connect(self.path)
        crsr = connection.cursor()

        drop_table_sql = f"DROP TABLE {name}"

        crsr.execute(drop_table_sql)
        connection.commit()
        connection.close()

    def view_table_details(self, table_name: str):
        assert table_name in self.table_names

        connection = sqlite3.connect(self.path)
        crsr = connection.cursor()
        crsr.execute(f"PRAGMA table_info({table_name})")

        output = ""
        columns = crsr.fetchall()
        output += f"Table {table_name} has {len(columns)} columns:\n"
        for column in columns:
            output += f"- {column[1]}: {column[2]}\n"
            if column[3] == 1:
                output += "  - NOT NULL constraint\n"
            if column[5] == 1:
                output += "  - PRIMARY KEY constraint\n"

        crsr.execute(f"SELECT * FROM {table_name} LIMIT {MAX_ROWS_TO_DISPLAY}")
        rows = crsr.fetchall()

        if len(rows) > 0:
            output += f"Sample of Table {table_name} rows:\n"
            for row in rows:
                output += str(row) + "\n"

        connection.close()
        return output

    def view_db_details(self):
        db_output = ""
        for table in self.table_names:
            db_output += self.view_table_details(table)

        return db_output

    def insert_db_path_into_function_exec_calls(
        self, function_code: str, for_test: bool = False
    ) -> str:
        if for_test:
            replace_path = self.test_db_path
        else:
            replace_path = self.path

        new_function_code = function_code.replace(
            "execute_sql(", f"execute_sql('{replace_path}', "
        )

        return new_function_code

    def create_testing_copy(self):
        test_db = sqlite3.connect(self.test_db_path)
        file_db = sqlite3.connect(self.path)

        query = "".join(line for line in file_db.iterdump())
        test_db.executescript(query)
        test_db.commit()

        test_db.close()

        return test_db
