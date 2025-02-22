from fastapi import FastAPI

app = FastAPI()

@app.post("/generate")
def generate_website(user_input: str):
    website_type = process_prompt(user_input)
    content = generate_content(website_type)
    code = generate_code(content)
    deployment_result = deploy_website(code)
    return {"status": "success", "url": deployment_result["url"]}
