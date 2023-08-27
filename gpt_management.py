import openai


def openai_chat_response(
    prompt,
    model="gpt-3.5-turbo-16k",
    system_message=None,
    existing_messages=None,
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

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    messages.append(response.choices[0].message)
    return messages
