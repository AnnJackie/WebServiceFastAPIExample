from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_200_OK

from model.auth_response import AuthResponse
from model.exception import user_credentials_exception
from service import auth_service


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"description": "Unauthorized"}}
)

@router.post("/token", status_code=HTTP_200_OK, response_model=AuthResponse)
async def login_for_access_toekn(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise user_credentials_exception()
    return auth_service.create_access_token(user.username, user.id)