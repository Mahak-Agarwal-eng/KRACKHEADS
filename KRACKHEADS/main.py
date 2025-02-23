from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import json
import os
import re
import logging
from pathlib import Path
import uuid
import asyncio
import aiofiles
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="templates"), name="static")


# Templates directory for rendering HTML pages
templates = Jinja2Templates(directory="templates")

# Constants
AGENT_AI_ENDPOINT = "https://api-lr.agent.ai/v1/agent/t6ng02te5kyaodjl/webhook/56847f23"
SITES_DIR = Path("generated_sites")
BASE_URL = "http://localhost:8000"  # Change this to your domain in production

# Create sites directory if it doesn't exist
SITES_DIR.mkdir(exist_ok=True)


def extract_code_blocks(response_text):
    """
    Extract HTML, CSS, and JavaScript code blocks from Agent.ai response.
    """
    try:
        response_data = json.loads(response_text)
        response_content = response_data.get('response', '')
        print(response_content)
        code_blocks = {'html': '', 'css': '', 'js': ''}

        html_match = re.search(r'### HTML[^<]*<!DOCTYPE html>(.*?)(?=###|$)', response_content, re.DOTALL)
        if html_match:
            code_blocks['html'] = f"<!DOCTYPE html>{html_match.group(1).strip()}"

        css_match = re.search(r'### CSS[^{]*(.*?)(?=###|$)', response_content, re.DOTALL)
        if css_match:
            code_blocks['css'] = css_match.group(1).strip()

        js_match = re.search(r'### JavaScript[^{]*(.*?)(?=###|$)', response_content, re.DOTALL)
        if js_match:
            code_blocks['js'] = js_match.group(1).strip()
        if not code_blocks.get('css'):
            logger.error("CSS content is empty")

        return code_blocks
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        raise ValueError("Invalid response format from Agent.ai")
    except Exception as e:
        logger.error(f"Error extracting code blocks: {e}")
        raise ValueError("Failed to extract code from response")

async def save_website_files(code_blocks, site_id):
    """
    Save the generated code files to a new directory.
    """
    try:
        site_dir = SITES_DIR / site_id
        site_dir.mkdir(exist_ok=True)

        # Debugging: Print site directory path
        print(f"Site directory: {site_dir}")

        # Save HTML file
        async with aiofiles.open(site_dir / 'index.html', 'w') as f:
            await f.write(code_blocks['html'])

        # Check if 'css' key exists
        if 'css' in code_blocks and code_blocks['css'].strip():
            async with aiofiles.open(site_dir / 'styles.css', 'w') as f:
                await f.write(code_blocks['css'])
            print(f"✅ CSS file saved at: {site_dir / 'styles.css'}")
        else:
            print("❌ CSS content is missing or empty")

        # Save JavaScript file
        async with aiofiles.open(site_dir / 'script.js', 'w') as f:
            await f.write(code_blocks['js'])

        return True
    except Exception as e:
        logger.error(f"Error saving files: {e}")
        raise ValueError("Failed to save website files")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Serve index.html where the user will enter the prompt.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-website")
async def generate_website(user_input: str = Form(...)):
    """
    Handle website generation request:
    1. Send request to Agent.ai
    2. Extract code from response
    3. Save files
    4. Mount static files
    5. Return public URL
    """
    try:
        site_id = str(uuid.uuid4())

        async with httpx.AsyncClient() as client:
            response = await client.post(AGENT_AI_ENDPOINT,json={"user_input": user_input},timeout=30.0)
                
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, 
                            detail="Failed to generate website")

            ai_response = response.text  # Store the AI response text
             # Debugging statement
            print("Agent.ai Full Response:", response.text)

            code_blocks = extract_code_blocks(ai_response)
            print("AI Response Code Blocks:", code_blocks)
            if 'css' not in code_blocks or not code_blocks['css'].strip():
                print("⚠️ No CSS provided. Using default.")
                code_blocks['css'] = "body { font-family: Arial, sans-serif; }"
            await save_website_files(code_blocks, site_id)


            try:
                app.mount(
                    f"/sites/{site_id}",
                    StaticFiles(directory=str(SITES_DIR / site_id), html=True),
                    name=f"site_{site_id}"
                )
            except Exception as e:
                logger.error(f"Error mounting static files: {e}")
                raise HTTPException(status_code=500, 
                                  detail="Failed to deploy website")

            public_url = f"{BASE_URL}/sites/{site_id}"
            
            return JSONResponse({
                "status": "success",
                "url": public_url,
                "message": "Website generated and deployed successfully"
            })

    except httpx.RequestError as e:
        logger.error(f"Error calling Agent.ai: {e}")
        raise HTTPException(status_code=502, detail="Failed to reach AI service")
    
    except ValueError as e:
        logger.error(f"Value error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, 
                          detail="An unexpected error occurred")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
