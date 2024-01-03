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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@api.get("/users/me", tags=["Auth"])
def read_users_me(token: str = Depends(oauth2_scheme), user_service: UserService = Depends()):
    """TODO: Add documentation here."""
    try:
      return user_service.get_current_active_user(token=token)
    except Exception as e:
       raise HTTPException(status_code=404, detail=str(e))

@api.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends()):
    """TODO: Add documentation here."""
    print("request recieved.")
    try:
      return user_service.login(username=form_data.username, plain_password=form_data.password)
    except Exception as e:
       raise HTTPException(status_code=404, detail=str(e))