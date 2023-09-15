import openai
import json
from lambdaai.prompts import ONE_SHOT_PROMPT_FUNCTION_ARGS

MAX_MESSAGE_CHAR_LENGTH = 3000


class openAIchat:
    def __init__(
        self,
        model: str = "gpt-3.5-turbo-16k",
        system_message: str = None,
        functions: dict = None,
    ):
        self.model = model
        self.messages = []

        if system_message:
            self.messages.append(
                {
                    "role": "system",
                    "content": system_message,
                }
            )

        self.functions = functions

    def send_chat(self, message, function_call) -> str:
        if function_call:
            try_to_call_function = {"name": function_call}
        else:
            None

        if len(message) > MAX_MESSAGE_CHAR_LENGTH:
            message = message[:MAX_MESSAGE_CHAR_LENGTH]
        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            functions=self.functions,
            function_call=try_to_call_function,
        )

        message = response.choices[0].message
        self.messages.append(message)

        if function_call:
            return message.get("function_call")
        else:
            return message.get("content")

    def add_one_shot_prompt(
        self,
        input_data,
        output_data,
    ):
        user_message = {"role": "user", "content": input_data}
        self.messages.append(user_message)

        function_call_response = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": "create_api",
                "arguments": json.dumps(output_data),
            },
        }

        self.messages.append(function_call_response)

        return

    def validate_json_function_call(
        ai_response,
        expected_function,
        expected_arguments,
    ):
        if ai_response is None or ai_response.name != expected_function:
            return (
                1,
                f"Error, you did not use a valid function call. Use the {expected_function }function to pass in and test the code you generated.",  # noqa
            )

        try:
            new_function = json.loads(
                ai_response.arguments,
                strict=False,
            )
        except Exception as e:
            return (
                1,
                f"Error decoding the JSON function call provided. Error: {e}",
            )

        missing_args = []
        for argument in expected_arguments:
            out = new_function.get(argument)
            if out is None:
                missing_args.append(argument)

        if missing_args:
            return (
                1,
                f"Error, the following arguments are missing from the provided function call: {missing_args}",
            )

        return 0, "success"

    def get_function_call_args(
        ai_response,
        expected_function,
    ):
        assert ai_response.name == expected_function

        arguments = json.loads(
            ai_response.arguments,
            strict=False,
        )

        return arguments
