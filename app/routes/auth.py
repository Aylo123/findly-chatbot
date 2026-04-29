from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import os

router = APIRouter()

# Base directory (deploy үед хэрэгтэй)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Түр user (дараа DB болгоно)
USER = {
    "username": "admin",
    "password": "1234"
}


# 🔓 Login page
@router.get("/login", response_class=HTMLResponse)
def login_page():
    with open(os.path.join(BASE_DIR, "templates/login.html"), encoding="utf-8") as f:
        return f.read()


# 🔐 Login submit
@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username == USER["username"] and password == USER["password"]:
        response = RedirectResponse("/", status_code=302)
        response.set_cookie(key="auth", value="true")
        return response

    return HTMLResponse("<h3>❌ Нэвтрэх нэр эсвэл нууц үг буруу</h3>")


# 🚪 Logout
@router.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("auth")
    return response