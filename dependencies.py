from fastapi import Header, HTTPException

from services.token_service import TokenService
from database.connection import MongoDatabase

# Initialize database connection
db = MongoDatabase()

async def check_user_is_admin(authorization: str = Header(...)):
    """
    Middleware function to check if a user is an admin based on the provided JWT token.

    Args:
    - authorization (str): JWT token passed in the request header.

    Returns:
    - json: User document from the database if the user is an admin.

    Raises:
    - HTTPException: If the token is invalid, user not found, or user is not an admin.
    """

    try:
        # Extract email from token using TokenService
        email = TokenService.get_email_from_token(authorization)
    except Exception as e:
        # Handle any exception that might arise from decoding the token
        raise HTTPException(detail=str(e), status_code=401)
    
    # Retrieve user information from database
    user = db.users.find_one({'email': email})
    if user is None:
        raise HTTPException(detail='User not found', status_code=404)

    # Check if the user has admin privileges
    if user.get('user_type') != 'admin':
        raise HTTPException(detail='User is not Admin', status_code=403)  # 403 for Forbidden

    return user
