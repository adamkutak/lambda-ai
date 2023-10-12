import math
import sqlite3
import hashlib
import datetime

SAFE_NAME_CHARACTERS = "/_"


def generate_fastapi_definition(
    name: str,
    path: str,
    inputs: dict,
    outputs: dict,
    is_async: bool,
):
    # check that everything is validly named firstly.
    assert name.isidentifier()
    assert path.replace("/", "").isidentifier()
    for input in inputs.keys():
        assert input.isidentifier()
    for output in outputs.keys():
        assert output.isidentifier()

    input_def_list = []
    for key, value in inputs.items():
        if value:
            input_def_list.append(f"{key}: {value}")
        else:
            input_def_list.append(f"{key}")

    input_def = ", ".join(input_def_list)

    decorator = f"@app.get('{path}')"
    function = (
        f"{'async ' if is_async else ''}def {name}({input_def}) -> Dict[str, Any]:\n"
    )
    function_def = "\n".join([decorator, function])
    function_def.replace("\n ", "\n")

    return function_def


def close_enough_float(json_response, output_test_case):
    if json_response.keys() != output_test_case.keys():
        return False
    for key in json_response:
        value1 = json_response[key]
        value2 = output_test_case[key]
        if isinstance(value1, float) and isinstance(value2, float):
            if not math.isclose(value1, value2):
                if abs(value1 - value2) / value1 > 0.01:
                    return False
        else:
            if value1 != value2:
                return False
    return True


def get_imports(imports):
    libraries = []
    for line in imports:
        if line.startswith("import "):
            library = line.split()[1]
            if "." in library:
                library = library.split(".")[0]
            libraries.append(library)
        elif line.startswith("from "):
            library = line.split()[1]
            libraries.append(library)
    return libraries


def execute_sql(db_path: str, sql: str):
    connection = sqlite3.connect(db_path)
    crsr = connection.cursor()
    result = crsr.execute(sql)
    if "SELECT" in sql:
        result = result.fetchall()
    connection.commit()
    connection.close()
    return result


def unsafe_session_id(rand_str: str):
    timestamp_str = str(datetime.datetime.timestamp())

    data = (timestamp_str + rand_str).encode()
    hash = hashlib.sha256(data).hexdigest()

    return hash
