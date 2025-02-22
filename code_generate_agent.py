from openai import OpenAI
def generate_code(content):
    prompt = f"Generate a simple HTML and CSS page with this content: {content}"
    response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    return response["choices"][0]["message"]["content"]
