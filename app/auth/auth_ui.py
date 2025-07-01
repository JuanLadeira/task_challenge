from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status, Cookie, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from jwt import DecodeError, ExpiredSignatureError, decode

from app.auth.router import login as auth_login
from app.user.services import UserServiceDep
from app.user.models import User
from app.settings import Settings

settings = Settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

router = APIRouter(
    prefix="/ui/auth",
    tags=["Interface de Autenticação (HTMX)"],
    responses={404: {"description": "Não encontrado"}},
)

templates = Jinja2Templates(directory="app/templates")

def get_current_user_from_cookie(service: UserServiceDep, access_token: str = Cookie(None)):
    if not access_token:
        return None
    
    token = access_token.split(" ")[1]

    try:
        payload = decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        username = payload.get('sub')

        if not username:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    except (DecodeError, ExpiredSignatureError):
        return None

    user = service.get_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

AuthenticatedUser = Annotated[User, Depends(get_current_user_from_cookie)]


def get_user(user: AuthenticatedUser):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail="Not authenticated",
            headers={"Location": "/ui/auth/login"},
        )
    return user

UserDep = Annotated[User, Depends(get_user)]



@router.get("/login", response_class=HTMLResponse)
async def get_login_form(request: Request):
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.post("/login")
async def login(
    service: UserServiceDep, 
    request: Request, 
    username: str = Form(...), 
    password: str = Form(...),
    ):
    
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
    except HTTPException as e:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": f"Invalid credentials:{str(e)}"},
            status_code=400,
        )

@router.post("/logout")
async def logout(response: Response):
    # A maneira mais idiomática para um backend que serve HTMX
    response.delete_cookie("access_token")
    response.headers["HX-Redirect"] = "/ui/auth/login"
    response.status_code = status.HTTP_200_OK # A resposta foi bem sucedida
    return response


@router.get("/register", response_class=HTMLResponse)
def get_register_page(request: Request):
    """
    Serve a página HTML para criação de um novo usuário.
    """
    return templates.TemplateResponse("components/create_user.html", {"request": request})
