
# Project Title and Description
Autonomous Application Builder-This project automates web application development using a multi-agent AI system. Users can enter a simple text prompt like:
"Create an e-commerce site for handmade crafts"
and the system automatically designs, builds, and deploys a fully functional web application.

## Repository Structure
Folder/File	Purpose
main.py-Contains all the source code of the project
generate_code-	Stores static files like images, fonts, and HTML files
.gitignore	Lists files & folders to be ignored by Git (e.g., node_modules/, .env)
README.md	-Overview of the project, setup guide, and usage instructions
template folder-	Template for frontend
-index.html-html code of our website
-styles.css-styling code of our website
-about_styles.css-styling of about our website section 
-about.html-html file of about our website section 
-web_background-background image of website

## Prerequisites
* Python(>=3.8)
* FastAPI
* /usr/local/bin/python3 "/Users/dangiji/VS Code/Krackhack/__pycache__/communication_agent.py"
* pip install fastapi uvicorn
* pip install httpx
* pip install jinja2
* pip install fastapi[all]
* pip install starlette
* pip install logging
* hint
* uvicorn main:app --reload
* ls 
* uvicorn main:app --reload
* pip install fastapi uvicorn
* pip list
* pip install aiofiles
* pip install python-multipart

Run all the way commands given above to meet the system requirements and then clone the repository in your device.
Finally run the main.py file. Then in the ports section add port "8000" and give all other further permissions. And Huzzah! here we can use our GenAI to generate your website.

## Alternatively

If the platform is showing error recursively then, use the folloeing ai agent directly to generate your website:

* https://agent.ai/agent/ready-to-use-website

This will generate a response in which (excuted html), css and javascript codes for your website are present.

## Project Overview
* AI-Driven Website Development → Gives the user ready-to-use websites without going through the hassle of coding and deployment of websites. 
* Seamless Agent Collaboration → Our specialized AI agents handle UI/UX, backend, and deployment.
* Fast Deployment → User gets clickable links deployed by the platform Vercel.
## TECH STACK
* Frontend: React.js 
* Backend: FastAPI
* AI Agents: agent.ai
* Deployment: Vercel, Render
* Communication: RESTful API
## How It Works
1️⃣ User enters a prompt (e.g., "Build a restaurant reservation system").

2️⃣ Designer Agent creates UI/UX components.

3️⃣ Developer Agent writes frontend & backend code.

4️⃣ Project Manager Agent ensures smooth integration & deployment.

5️⃣ The system deploys the final website, making it live & accessible.

## Conclusion
Our project leverages AI agents to automate the end-to-end web development process, transforming a simple user prompt into a fully deployed website. This project showcases the power of AI in web development, enabling faster, smarter, and more efficient website creation. 

## Future Improvements
* Better local deployment platforms like EC2 instance can be used to enhance user- experience.
* Inclusion of PostgreSQL for better Database management.
* User can opt to Deploy the website on an authorized paid platform with a domain name of his/her choice.
* The website can take in multiple prompts to change the developed website according to user's requirement.

