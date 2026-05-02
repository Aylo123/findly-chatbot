from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat
from app.services.search import load_data
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── Startup: warm the knowledge-base cache ─────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    load_data()          # pre-load JSON once so first request is fast
    yield


# ── App ─────────────────────────────────────────────────────────
app = FastAPI(
    title="Findly Chatbot API",
    description="Internal employee chatbot for Zeely / HabiDo",
    version="2.0.0",
    lifespan=lifespan,
)

# Allow same-origin requests from the web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten to your domain in production
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ── Routes ───────────────────────────────────────────────────────
app.include_router(chat.router)

# Static files
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static",
)


# ── Pages ─────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def home():
    with open(os.path.join(BASE_DIR, "templates/index.html"), encoding="utf-8") as f:
        return f.read()


# ── Health check (useful for Docker / uptime monitors) ──────────
@app.get("/health")
def health():
    return {"status": "ok"}