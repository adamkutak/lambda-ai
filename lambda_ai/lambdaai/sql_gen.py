# given a test case, take natural language input and create pre-sql and post-sql

# ie) input: price, quantity; output: total_price
#     test_case: in: 10, 5; out: 50
#     pre-test: setup the database so there is 45 products in inventory column before the call and 40 products after.

from lambda_ai.lambdaai.gpt_management import openAIchat
from lambda_ai.lambdaai.prompts import (
    ONE_SHOT_SQL_GENERATION_USER,
    ONE_SHOT_SQL_GENERATION_FUNCTION_ARGS,
    SQL_GENERATION_PROMPT,
)
from lambda_ai.lambdaai.gpt_function_calls import FUNCTION_CALLING_SQL_GENERATION
from lambda_ai.lambdaai.db import DB


class SQLGenAgent:
    def __init__(self, database: DB, model: str = "gpt-3.5-turbo-0613"):
        self.model = model
        self.database = database  # NOTE: This creates a 1:1 rel for db and agent. Could take db as a method param to resolve this.

    def generate_sql(
        self, nat_lang_sql: str, table_name: str
    ):  # TODO: update dict with TestCase schema
        ai_chat = openAIchat(
            model=self.model,
            system_message="You are an SQL generation bot.",
            functions=FUNCTION_CALLING_SQL_GENERATION,
        )

        ai_chat.add_function_one_shot_prompt(
            name="create_sql",
            input_data=ONE_SHOT_SQL_GENERATION_USER,
            output_data=ONE_SHOT_SQL_GENERATION_FUNCTION_ARGS,
        )

        db_details = self.database.view_table_details(table_name)

        prompt = SQL_GENERATION_PROMPT.format(
            nat_lang_description=nat_lang_sql, db_details=db_details
        )

        ai_response = ai_chat.send_chat(message=prompt, function_call="creat_sql")

        return ai_response
