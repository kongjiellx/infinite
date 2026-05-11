# -*-coding: utf-8 -*-
import openai

def call_openai(msgs):
    openai.proxy = "http://127.0.0.1:7890"
    openai.api_key = "sk-REDACTED"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=msgs,
        stream=True,
    )
    prompt = "\n".join([f"{msg['role']}:{msg['content']}" for msg in msgs]) + "\n"
    print(prompt)
    reply_content = ""
    for chunk in response:
        chunk_message = dict(chunk['choices'][0]['delta'])
        char = chunk_message.get("content", "")
        print(char, end="", flush=True)
        reply_content += char
    return reply_content

