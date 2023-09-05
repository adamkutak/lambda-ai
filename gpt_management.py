import openai


def openai_chat_response(
    prompt,
    model="gpt-3.5-turbo-16k",
    system_message=None,
    existing_messages=None,
    functions=None,
    function_call=None,
):
    messages = []
    if system_message:
        messages.append(
            {
                "role": "system",
                "content": system_message,
            }
        )
    elif existing_messages:
        messages.extend(existing_messages)

    messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    if functions:
        if function_call:
            function_call = {"name": function_call}
        else:
            function_call = "auto"

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        functions=functions,
        function_call=function_call,
    )

    messages.append(response.choices[0].message)
    return messages
