import requests

def deploy_website(html_code):
    url = "https://some-deployment-service.com/api/deploy"
    response = requests.post(url, json={"html": html_code})
    return response.json()
