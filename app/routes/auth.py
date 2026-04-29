from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()

# Fake user (дараа DB болгоно)
USER = {
    "username": "admin",
    "password": "Zeely@123"
}

@router.get("/login", response_class=HTMLResponse)
def login_page():
    with open("templates/login.html", encoding="utf-8") as f:
        return f.read()


@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username == USER["username"] and password == USER["password"]:
        response = RedirectResponse("/", status_code=302)
        response.set_cookie(key="auth", value="true")
        return response

    return HTMLResponse("<h3>Нэвтрэх нэр эсвэл нууц үг буруу</h3>")


@router.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("auth")
    return response