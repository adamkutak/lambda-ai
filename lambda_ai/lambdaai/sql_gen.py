# given a test case, take natural language input and create pre-sql and post-sql

# ie) input: price, quantity; output: total_price
#     test_case: in: 10, 5; out: 50
#     pre-test: setup the database so there is 45 products in inventory column before the call and 40 products after.

import os
from .gpt_management import openAIchat
from .prompts import (
    ONE_SHOT_SQL_GENERATION_FUNCTION_ARGS,
    ONE_SHOT_SQL_GENERATION_FUNCTION_ARGS_2,
    SQL_GENERATION_PROMPT,
    SQL_ON_CREATE_ERROR,
)
from .gpt_function_calls import FUNCTION_CALLING_SQL_GENERATION, SQLGeneration
from .db import DB
from .utils import execute_sql

MAX_ATTEMPTS = 4


class SQLGenAgent:
    def __init__(self, database: DB, model: str = "gpt-3.5-turbo-0613"):
        self.model = model
        self.database = database
        self.usage = {"prompt_tokens": 0, "completion_tokens": 0}

    def generate_sql(self, pre_sql: str, post_sql: str):
        ai_chat = openAIchat(
            model=self.model,
            system_message="You are an SQL generation bot. Use the functions given to you.",
            functions=[FUNCTION_CALLING_SQL_GENERATION],
        )

        ai_chat.add_function_one_shot_prompt(
            name="create_sql",
            input_data=None,
            output_data=ONE_SHOT_SQL_GENERATION_FUNCTION_ARGS,
        )

        ai_chat.add_function_one_shot_prompt(
            name="create_sql",
            input_data=None,
            output_data=ONE_SHOT_SQL_GENERATION_FUNCTION_ARGS_2,
        )

        db_details = self.database.view_db_details()

        prompt = SQL_GENERATION_PROMPT.format(
            pre_sql=pre_sql, post_sql=post_sql, db_details=db_details
        )

        attempts = 0
        result_code = 1
        ai_response = ai_chat.send_chat(message=prompt, function_call="create_sql")

        while result_code > 0 and attempts < MAX_ATTEMPTS:
            result_code, data = self.process_and_test_response(ai_response)
            if result_code > 0:
                message = SQL_ON_CREATE_ERROR.format(error=data)
                ai_response = ai_chat.send_chat(
                    message=message, function_call="create_sql"
                )
            attempts += 1

        self.usage["prompt_tokens"] += ai_chat.usage["prompt_tokens"]
        self.usage["completion_tokens"] += ai_chat.usage["completion_tokens"]
        return result_code, data

    def process_and_test_response(self, ai_response):
        validate_json, data = openAIchat.validate_json_function_call(
            ai_response, "create_sql", SQLGeneration
        )
        if validate_json > 0:
            return 2, data

        pre_sql_test = data["pre_sql"]
        post_sql_test = data["post_sql"]

        isolated_test_db = self.database.create_isolated_copy()

        for pre_sql in pre_sql_test:
            try:
                execute_sql(isolated_test_db, pre_sql)
            except Exception as e:
                os.remove(isolated_test_db)
                return 1, f"error with pre sql query: {pre_sql}, The error is: {e}"

        for post_sql in post_sql_test:
            try:
                ret_value = execute_sql(isolated_test_db, post_sql["sql"])
            except Exception as e:
                os.remove(isolated_test_db)
                return (
                    1,
                    f"error with pre sql query: {post_sql['sql']}, The error is: {e}",
                )

            if not ret_value:
                os.remove(isolated_test_db)
                return (
                    1,
                    f"error: post sql statement: {post_sql['sql']} did not return any comparison value to assert against.",
                )

        os.remove(isolated_test_db)
        return 0, data
