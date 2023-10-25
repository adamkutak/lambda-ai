# given a test case, take natural language input and create pre-sql and post-sql

# ie) input: price, quantity; output: total_price
#     test_case: in: 10, 5; out: 50
#     pre-test: setup the database so there is 45 products in inventory column before the call and 40 products after.

from .gpt_management import openAIchat
from .prompts import (
    ONE_SHOT_SQL_GENERATION_USER,
    ONE_SHOT_SQL_GENERATION_FUNCTION_ARGS,
    SQL_GENERATION_PROMPT,
)
from .gpt_function_calls import FUNCTION_CALLING_SQL_GENERATION, SQLGeneration
from .db import DB

MAX_ATTEMPTS = 10


class SQLGenAgent:
    def __init__(self, database: DB, model: str = "gpt-3.5-turbo-0613"):
        self.model = model
        self.database = database  # NOTE: This creates a 1:1 rel for db and agent. Could take db as a method param to resolve this.

    def generate_sql(self, pre_sql: str, post_sql: str):
        ai_chat = openAIchat(
            model=self.model,
            system_message="You are an SQL generation bot. Use the functions given to you.",
            functions=[FUNCTION_CALLING_SQL_GENERATION],
        )

        ai_chat.add_function_one_shot_prompt(
            name="create_sql",
            input_data=ONE_SHOT_SQL_GENERATION_USER,
            output_data=ONE_SHOT_SQL_GENERATION_FUNCTION_ARGS,
        )

        db_details = self.database.view_db_details()

        prompt = SQL_GENERATION_PROMPT.format(
            pre_sql=pre_sql, post_sql=post_sql, db_details=db_details
        )

        attempts = 0

        while attempts < MAX_ATTEMPTS:
            ai_response = ai_chat.send_chat(message=prompt, function_call="create_sql")

            result_code, data = openAIchat.validate_json_function_call(
                ai_response, "create_sql", SQLGeneration
            )

            if result_code < 1:
                breakpoint()
                return data

        return None

    def process_and_validate_response(ai_response):
        # 1. use openAIchat.validate_json_function_call to validate func call errors
        # 2. check to see if sql is formatted properly
        # 3. make sure sql calls won't error when called on attached db (or maybe this is done in test_harness)
        pass
