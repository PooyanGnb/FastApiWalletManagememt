import unittest
from unittest.mock import patch, MagicMock
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

from services.token_service import TokenService


class TestTokenService(unittest.TestCase):
    """
    Unit tests for the TokenService class which handles JWT token operations.
    """

    def setUp(self):
        """
        Set up the environment for each test:
        - Mock settings for JWT configuration.
        - Prepare a valid token for testing.
        """
        # Mock settings with predefined JWT secret and algorithm
        self.mock_settings = MagicMock()
        self.mock_settings.jwt_secret = "secret"
        self.mock_settings.jwt_algorithm = "HS256"
        self.mock_settings.jwt_expiration_minutes = 30

        # Apply settings patch to all tests
        self.settings_patch = patch('services.token_service.settings', self.mock_settings)
        self.settings_patch.start()

        # Encode a valid JWT for testing purposes
        self.valid_email = "user@example.com"
        self.valid_token = jwt.encode(
            {"sub": self.valid_email, "exp": datetime.utcnow() + timedelta(minutes=30)},
            self.mock_settings.jwt_secret,
            algorithm=self.mock_settings.jwt_algorithm
        )

    def tearDown(self):
        """
        Clean up (stop) settings patch after each test.
        """
        self.settings_patch.stop()

    def test_create_jwt(self):
        """
        Test the creation of a JWT to ensure it encodes the correct email and validates against the expected algorithm.
        """
        # Create token using the service
        token = TokenService.create_jwt(self.valid_email)
        
        # Decode the token to verify its contents
        decoded = jwt.decode(token, self.mock_settings.jwt_secret, algorithms=[self.mock_settings.jwt_algorithm])
        self.assertEqual(decoded['sub'], self.valid_email)

    def test_decode_token(self):
        """
        Test decoding of a valid and invalid JWT to ensure proper handling of errors.
        """
        # Decode valid token and check payload
        payload = TokenService.decode_token(self.valid_token)
        self.assertEqual(payload['sub'], self.valid_email)
        
        # Ensure that decoding an invalid token raises an HTTPException
        with self.assertRaises(HTTPException):
            TokenService.decode_token('invalid.token')

    def test_get_email_from_token(self):
        """
        Test extracting email from a given JWT, including handling of an invalid token.
        """
        # Extract email from valid token
        email = TokenService.get_email_from_token(self.valid_token)
        self.assertEqual(email, self.valid_email)
        
        # Verify that an invalid token raises an HTTPException
        with self.assertRaises(HTTPException):
            TokenService.get_email_from_token('invalid.token')


if __name__ == '__main__':
    unittest.main()