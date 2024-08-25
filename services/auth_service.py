from fastapi import HTTPException

from database.connection import MongoDatabase


# Create a single instance of MongoDatabase to be used across the AuthService
db = MongoDatabase()

class AuthService:
    """
    A service class for managing authentication and user verification actions.
    """
        
    @staticmethod
    def verify_user(email, password):
        """
        Verifies if a user's email and password match the records in the database.

        Returns:
        - json: The user's information if credentials are correct.

        Raises:
        - HTTPException: If the credentials are incorrect or the user does not exist.
        """

        user = db.users.find_one({"email": email})
        if not user or user['password'] != password:
            raise HTTPException(status_code=400, detail="Incorrect credentials")
        return user

    @staticmethod
    def create_user(data):
        """
        Creates a new user record in the database.

        Raises:
        - HTTPException: If the user already exists.
        """
                
        if db.users.find_one({"email": data['email']}):
            raise HTTPException(status_code=400, detail="Email already exists")
        db.users.insert_one(data)
