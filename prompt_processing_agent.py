from openai import OpenAI

def process_prompt(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Extract website type and features."},
                  {"role": "user", "content": user_input}]
    )
    return response["choices"][0]["message"]["content"]
