from fastapi import Header, HTTPException
import jwt
from datetime import datetime, timedelta

from settings import Settings

# Initialize settings
settings = Settings()

class TokenService:
    """
    Service class for handling JWT token operations, including creation and decoding of tokens.
    """
    
    @staticmethod
    def create_jwt(email):
        """
        Creates a JWT token with an expiration set from the current time.

        Args:
        - email (str): User's email to encode within the JWT.

        Returns:
        - str: Encoded JWT.
        """

        expiration = datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_minutes)
        payload = {"sub": email, "exp": expiration}
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    @staticmethod
    def decode_token(token):
        """
        Decodes a JWT token to extract the payload.

        Args:
        - token (str): The JWT token to be decoded.

        Returns:
        - dict: The decoded token payload or an empty dict if decoding fails.
        """

        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
            return payload
        except:
            raise HTTPException(detail="Invalid token", status_code=401)
        
    @staticmethod
    def get_email_from_token(authorization: str = Header(...)):
        """
        Extracts the email from a JWT token provided in the authorization header.

        Args:
        - authorization (str): The JWT token from the authorization header.

        Returns:
        - str: Email extracted from the token.

        Raises:
        - HTTPException: If the token is invalid or the email is not present.
        """

        try:
            decode_token = TokenService.decode_token(authorization)
            email = decode_token["sub"]
        except:
            raise HTTPException(detail="Invalid token", status_code=401)
        return email
            
        