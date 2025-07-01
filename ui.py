from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.auth.router import login as auth_login
from app.user.services import UserServiceDep

router = APIRouter(
    prefix="/ui/auth",
    tags=["Interface de Autenticação (HTMX)"],
    responses={404: {"description": "Não encontrado"}},
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def get_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(service: UserServiceDep, request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    form_data = OAuth2PasswordRequestForm(username=username, password=password, scope="", client_id=None, client_secret=None)
    try:
        token_data = await auth_login(service, form_data)
        response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {token_data['access_token']}",
            httponly=True,
        )
        return response
    except Exception as e:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"},
            status_code=400,
        )

@router.post("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/ui/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response
