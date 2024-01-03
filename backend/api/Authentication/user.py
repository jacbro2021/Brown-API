"""API routes for the Authentication module."""

from fastapi import (Depends,
                     HTTPException,
                     APIRouter
                    )
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ...models.Authentication.user import User
from ...services.Authentication.user_service import UserService

api = APIRouter(prefix="/auth")
openapi_tags = {
    "name":"Auth",
    "description":"Routes to interact with auth API functionality."   
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@api.get("/users/me", tags=["Auth"])
def read_items(token: str = Depends(oauth2_scheme), user_service: UserService = Depends()):
    return user_service.get_current_user(token=token)

# @api.post("/token")
# def login(form_data: OAuth2PasswordRequestForm = Depends()):

