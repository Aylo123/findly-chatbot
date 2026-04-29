from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routes import chat
import os
from app.routes import auth
app.include_router(auth.router)

# Base directory (deploy үед хэрэгтэй)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# FastAPI app
app = FastAPI()

# API routes
app.include_router(chat.router)

# Static files (css, js, images)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Homepage
@app.get("/", response_class=HTMLResponse)
def home():
    with open(os.path.join(BASE_DIR, "templates/index.html"), encoding="utf-8") as f:
        return f.read()