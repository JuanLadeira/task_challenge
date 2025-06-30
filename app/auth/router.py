
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import HTTPException, status
from fastapi import APIRouter, Depends
from app.auth.security import verify_password, create_access_token
from app.user.services import UserServiceDep

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
async def login(
    service:UserServiceDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
    ):
    """
    Endpoint to handle user login.
    It receives a username and password, validates them, and returns an access token.
    """
    user = service.get_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        # If the user does not exist or the password is incorrect, raise an error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # If the user exists and the password is correct, generate a token
    access_token = create_access_token(data={"sub": user.username}) 

    return {"access_token": access_token, "token_type": "bearer"}