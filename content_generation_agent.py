from openai import OpenAI
def generate_content(website_type):
    prompt = f"Write homepage content for a {website_type} website."
    response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    return response["choices"][0]["message"]["content"]
