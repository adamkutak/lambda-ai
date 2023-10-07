from lambda_ai.database.crud.api_container import (
    create_api_environment,
    create_api_file,
    get_api_file,
    update_api_file,
)
from lambda_ai.database.crud.api_function import (
    create_api_function,
    get_api_function,
    update_api_function,
)
from lambda_ai.database.crud.db import create_db, delete_db, get_all_dbs, get_db
from lambda_ai.database.crud.table import create_table, get_all_tables_by_db
from lambda_ai.database.main import db_test_session
from lambda_ai.database.schemas.api_function import APIFunctionCreate
from lambda_ai.database.schemas.db import DBCreate
from lambda_ai.database.schemas.api_container import APIFileCreate, APIEnvironmentCreate
from lambda_ai.database.schemas.table import TableCreate


# FIXME: some of the transactions are not being rolled back with db_test_session, and the data in the db is persisting between tests


def test_create_and_retrieve_api_function():
    with db_test_session() as db:
        new_function = APIFunctionCreate(
            name="SampleFunction",
            path="/sample_path",
            inputs={"arg1": "int", "arg2": "str"},
            outputs={"result": "str"},
            functionality="Demonstration",
            test_cases=[
                {"input": {"arg1": 5, "arg2": "test"}, "output": {"result": "test5"}}
            ],
            force_use_db=False,
            is_async=False,
            attached_db=None,
        )

        # Create the APIFunction
        created_function = create_api_function(db, new_function)

        # Ensure it's created
        assert created_function is not None
        assert created_function.name == "SampleFunction"

        # Retrieve and verify
        retrieved_function = get_api_function(db, created_function.id)
        assert retrieved_function is not None
        assert retrieved_function.name == "SampleFunction"
        assert retrieved_function.path == "/sample_path"


def test_update_api_function():
    with db_test_session() as db:
        # First, create a function to later update
        initial_function = APIFunctionCreate(
            name="InitialFunction",
            path="/initial_path",
            inputs={"arg1": "int", "arg2": "str"},
            outputs={"result": "str"},
            functionality="Initial Demonstration",
            test_cases=[
                {"input": {"arg1": 5, "arg2": "test"}, "output": {"result": "test5"}}
            ],
            force_use_db=False,
            is_async=False,
            attached_db=None,
        )

        created_function = create_api_function(db, initial_function)

        updated_function_data = {
            "test_cases": [
                {"input": {"arg1": 5, "arg2": 3.5}, "output": {"result": 8.5}}
            ],
            "force_use_db": True,
            "name": "UpdatedFunction",
            "path": "/updated_path",
            "inputs": {"arg1": "int", "arg2": "float"},
        }

        updated_function = update_api_function(
            db, created_function.id, **updated_function_data
        )

        # Assertions for the update
        assert updated_function is not None
        assert updated_function.name == "UpdatedFunction"
        assert updated_function.path == "/updated_path"
        assert updated_function.inputs["arg2"] == "float"


def test_create_db():
    with db_test_session() as session:
        # Create a new DB entry
        db_data = DBCreate(name="TestDB", location="/path/to/db")
        db = create_db(session, db_data)

        # Check if the DB entry has been created
        assert db is not None
        assert db.name == "TestDB"
        assert "/path/to/db/TestDB.db" in db.path


def test_get_db():
    with db_test_session() as session:
        # Create a new DB entry for testing
        db_data = DBCreate(name="SampleDB", location="/path/to/sample")
        db_obj = create_db(session, db_data)

        # Try retrieving it
        db = get_db(session, db_obj.id)

        # Check if the retrieved DB entry matches the created one
        assert db is not None
        assert db.name == "SampleDB"
        assert "/path/to/sample/SampleDB.db" in db.path


def test_get_all_dbs():
    with db_test_session() as session:
        # Create multiple DB entries for testing
        for i in range(5):
            db_data = DBCreate(name=f"DB_{i}", location=f"/path/to/db_{i}")
            create_db(session, db_data)

        # Retrieve all DB entries
        all_dbs = get_all_dbs(session)

        # Check if we retrieved all
        assert len(all_dbs) == 5


def test_delete_db():
    with db_test_session() as session:
        # Create a new DB entry for testing
        db_data = DBCreate(name="DeleteDB", location="/path/to/delete")
        db_obj = create_db(session, db_data)

        # Delete the DB entry
        delete_db(session, db_obj.id)

        # Try retrieving the deleted DB
        db = get_db(session, db_obj.id)

        # Check if the DB entry has been deleted
        assert db is None


def test_add_db_to_api_function():
    with db_test_session() as session:
        # Create a new DB entry for testing
        db_data = DBCreate(name="SampleDB", location="/path/to/sample")
        db_obj = create_db(session, db_data)

        # Try retrieving it
        db = get_db(session, db_obj.id)

        new_function = APIFunctionCreate(
            name="InitialFunction",
            path="/initial_path",
            inputs={"arg1": "int", "arg2": "str"},
            outputs={"result": "str"},
            functionality="Initial Demonstration",
            test_cases=[
                {"input": {"arg1": 5, "arg2": "test"}, "output": {"result": "test5"}}
            ],
            force_use_db=False,
            is_async=False,
            attached_db=db.id,
        )
        created_function = create_api_function(session, new_function)

        # second DB object
        db_data_2 = DBCreate(name="testdb2", location="/path/to/sample")
        db_obj_2 = create_db(session, db_data_2)

        db_2 = get_db(session, db_obj_2.id)

        updated_function_data = {
            "attached_db_id": db_2.id,
        }

        updated_function = update_api_function(
            session, created_function.id, **updated_function_data
        )

        db_get = get_db(session, updated_function.attached_db_id)

        assert db_get.id == db_2.id


def test_create_api_file_and_environment():
    with db_test_session() as session:
        api_file = APIFileCreate(
            name="test1", file_path="test/file/path", functions={}, attach_db=False
        )

        api_file = create_api_file(session, api_file)

        api_env = APIEnvironmentCreate(
            api_file_id=api_file.id,
            file_uvicorn="deployer.py",
            requirements_file="ab/cd/req.txt",
        )

        create_api_environment(session, api_env)

        new_function = {
            "name": "test_function",
            "code": "do some stuff",
            "imports": "import some stuff",
        }

        retrieved_api_file = get_api_file(session, api_file.id)
        current_functions = (
            retrieved_api_file.functions.copy()
        )  # IMPORTANT: YOU MUST COPY THE DICT SO IT GETS A NEW MEM LOCATION

        current_functions["new_function"] = new_function

        updated_api_file = update_api_file(
            session, retrieved_api_file.id, functions=current_functions
        )

        assert updated_api_file.functions.get("new_function") != None


def test_create_tables_and_db():
    with db_test_session() as session:
        # Create a new DB entry for testing
        db_data = DBCreate(name="SampleDBWithTables", location="/path/to/sample")
        db_obj = create_db(session, db_data)

        # Try retrieving it
        db = get_db(session, db_obj.id)
        table_data = TableCreate(
            name="testtable1",
            columns={
                "myname": {"type": "string", "constraints": ["primary key", "unique"]},
                "secondcol": {"type": "int", "constraints": []},
            },
            db_id=db.id,
        )
        create_table(session, table_data)
        table_data = TableCreate(
            name="secondTableIadded",
            columns={
                "colfirst": {"type": "string", "constraints": ["primary key"]},
                "colsecond": {"type": "int", "constraints": ["unique"]},
            },
            db_id=db.id,
        )
        create_table(session, table_data)
        tables = get_all_tables_by_db(session, db.id)

        assert tables[0].name == "testtable1"
        assert tables[1].db_id == db.id


test_create_and_retrieve_api_function()
test_update_api_function()
test_create_db()
test_get_db()
test_get_all_dbs()
test_delete_db()
test_add_db_to_api_function()
test_create_api_file_and_environment()
test_create_tables_and_db()
