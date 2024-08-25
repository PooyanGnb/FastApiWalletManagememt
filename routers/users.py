from fastapi import APIRouter

from database.models import LoginRequest, SignupRequest
from services.auth_service import AuthService
from services.token_service import TokenService

router = APIRouter(tags=["Auth"])

@router.post("/login")
async def login(request: LoginRequest):
    """
    Authenticate a user and return a JWT token if successful.

    Args:
    - LoginRequest: A model that contains the user's email and password.

    Returns:
    - json: A json containing the JWT access token and its type.
    """

    # check credentials
    user = AuthService.verify_user(request.email, request.password)
    if not user: 
        return {"message": "Authentication failed"}, 401
    token = TokenService.create_jwt(user['email']) # If user was found, creates jwt and
    return {"access_token": token, "token_type": "bearer"}

@router.post("/signup")
async def signup(request: SignupRequest):
    """
    Register a new user and return a JWT token if registration is successful.

    Args:
    - SignupRequest: A model that includes the user's email, password, and user type.

    Returns:
    - dict: A dictionary containing the JWT access token and its type.
    """

    # creates user, then creates jwt token and returns it
    AuthService.create_user(request.dict())
    token = TokenService.create_jwt(request.email)
    return {"access_token": token, "token_type": "bearer"}