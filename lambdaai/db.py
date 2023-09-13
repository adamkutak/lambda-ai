import sqlite3
import os

DEFAULT_DB_LOCATION = "generated_dbs"
MAX_ROWS_TO_DISPLAY = 3


class DB:
    def __init__(
        self,
        name,
        location: str = None,
    ):
        db_name = f"{name}.db"
        curr_dbs_at_path = os.listdir(location)
        assert db_name not in curr_dbs_at_path

        self.name = db_name
        location = location or DEFAULT_DB_LOCATION
        self.path = location + "/" + db_name
        self.table_names = []

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
            col_type = col_info["type"]
            col_constraints = " ".join(col_info["constraints"])
            create_table_sql += f"{col_name} {col_type} {col_constraints}, "

        create_table_sql = create_table_sql[:-2] + ")"

        breakpoint()

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

    def execute_sql(self, sql: str):
        connection = sqlite3.connect(self.path)
        crsr = connection.cursor()
        crsr.execute(sql)
        connection.commit()
        connection.close()

    def list_tables(self):
        return self.table_names

    def view_table_details(self, table_name: str):
        conn = sqlite3.connect(self.name)
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table_name})")

        output = ""
        columns = cur.fetchall()
        output += f"Table {table_name} has {len(columns)} columns:\n"
        for column in columns:
            output += f"- {column[1]}: {column[2]}\n"
            if column[3] == 1:
                output += "  - NOT NULL constraint\n"
            if column[4] != "":
                output += f"  - DEFAULT value: {column[4]}\n"
            if column[5] == 1:
                output += "  - PRIMARY KEY constraint\n"
        cur.execute(f"SELECT * FROM {table_name} LIMIT {MAX_ROWS_TO_DISPLAY}")
        rows = cur.fetchall()
        output += f"Table {table_name} has {len(rows)} rows:\n"
        for row in rows:
            output += str(row) + "\n"

        conn.close()
        return output
