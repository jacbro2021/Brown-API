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
                                                    InvalidTokenException,
                                                    InvalidUserInputPropertyException,
                                                    DuplicateUserException
                                                  )

api = APIRouter(prefix="/auth")
openapi_tags = {
    "name":"Auth",
    "description":"Routes to interact with auth API functionality."   
}

@api.post("/create", tags=["Auth"])
def create_user(username: str,
                password: str,
                email: str, 
                full_name: str, 
                auth_service: AuthenticationService = Depends()) -> NewUser:
    """
    Create a new user in the database.

    Args:
      username: The username of the user to be created.
      password: The password for the new user.
      email: The email for the new user.
      full_name: The full name for the new user.

    Returns:
      NewUser: The NewUser object for the newly created user.

    Raises:
      422: If the input username, password, or email are improperly formatted or being used by another user.
    """
    try:
      return auth_service.create_user(username=username,
                                      password=password,email=email, 
                                      full_name=full_name)
    except (InvalidUserInputPropertyException, DuplicateUserException) as e:
      raise HTTPException(status_code=422, detail=str(e))

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

@api.post("/refresh-access-token", tags=["Auth"])
def refresh_access_token(refresh_token: str = Header(), auth_service: AuthenticationService = Depends()) -> Token:
    """
    Refresh the Access token for a given user.

    Args:
      refresh_token: The refresh token for the user to refresh the access_token for (passed as a header)

    Returns:
      Token: The newly created access token for the user.

    Raises:

    """
    try:
      return auth_service.refresh_access_token(refresh_token=refresh_token)
    except UserNotFoundException as e:
       raise HTTPException(status_code=404, detail=str(e))

@api.get("/get", tags=["Auth"])
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
    
@api.delete("/delete", tags=["Auth"])
def delete_current_user(user_service: UserService = Depends()) -> User:
    """
    Deletes the currently authenticated user from the database.

    Returns:
      User: The user that was deleted from the database.

    Raises:
      401: If the user is disabled and needs to reauthenticate.
      422: If the token passed by the user is invalid.
      404: If the user is not found in the database.
    """
    try:
      return user_service.delete_current_user()
    except DisabledUserException as e:
      raise HTTPException(status_code=401, detail=str(e))
    except InvalidTokenException as e:
      raise HTTPException(status_code=422, detail=str(e))
    except UserNotFoundException as e:
      raise HTTPException(status_code=404, detail=str(e))