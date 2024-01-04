"""API routes for the Authentication module."""

from fastapi import (Depends,
                     HTTPException,
                     APIRouter,
                     Header
                    )
from fastapi.security import OAuth2PasswordRequestForm

from ...models.Authentication.user import User, NewUser
from ...models.Authentication.token import Token
from ...services.Authentication.user_service import UserService
from ...services.Authentication.authentication_service import AuthenticationService
from ...services.Authentication.exceptions import (UserNotFoundException,
                                                    DisabledUserException,
                                                    InvalidCredentialsException, 
                                                    InvalidTokenException
                                                  )

api = APIRouter(prefix="/auth")
openapi_tags = {
    "name":"Auth",
    "description":"Routes to interact with auth API functionality."   
}

@api.post("/token", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthenticationService = Depends()) -> Token:
    """
    Login a user and get a JWT to use to call protected routes in the API.
    
    Args:
      username: The username of the user to login.
      password: The password of the user to login.
      
    Returns:
      Token: The JWT token for the newly logged in user.
      
    Raises:
      404: If the user is not found in the database.
      422: If the credentials input by the user are invalid.
    """
    try:
      return auth_service.login(username=form_data.username, plain_password=form_data.password)
    except UserNotFoundException as e:
      raise HTTPException(status_code=404, detail=str(e))
    except InvalidCredentialsException as e:
      raise HTTPException(status_code=422, detail=str(e))

@api.get("/current_user", tags=["Auth"])
def get_current_user(user_service: UserService = Depends()) -> User:
    """
    Get the current user from the database. Depends on the Authorization header with a valid Bearer token.
    If testing endpoints using the docs page of the API, then the route will require no params when authorized.
    
    Returns:
      User: The currently logged in and active user.
      
    Raises:
      401: If the user is disabled and needs to reauthenticate.
      422: If the token passed by the user is invalid.
      404: If the user is not found in the database.
    """
    try:
      return user_service.get_current_active_user()
    except DisabledUserException as e:
      raise HTTPException(status_code=401, detail=str(e))
    except InvalidTokenException as e:
      raise HTTPException(status_code=422, detail=str(e))
    except UserNotFoundException as e:
      raise HTTPException(status_code=404, detail=str(e))
    

@api.post("/create", tags=["Auth"])
def create_user(username: str,
                password: str,
                email: str, 
                full_name: str, 
                auth_service: AuthenticationService = Depends()) -> NewUser:
  
  return auth_service.create_user(username=username, password=password,email=email, full_name=full_name)
  

@api.get("/test", tags=["Auth"])
def test(refresh_token: str = Header()):
  return {"refresh_token": refresh_token}

