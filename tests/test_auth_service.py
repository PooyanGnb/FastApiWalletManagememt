import unittest
from unittest.mock import patch
from fastapi import HTTPException

from services.auth_service import AuthService

class TestAuthService(unittest.TestCase):
    """
    Unit tests for AuthService which handles user authentication and account management.
    """

    @patch('services.auth_service.db')
    def test_verify_user_success(self, mock_db):
        """
        Test successful user verification when correct credentials are provided.
        """
        # Setup dummy data for a successful lookup
        mock_db.users.find_one.return_value = {'email': 'test@example.com', 'password': 'password'}
        
        # Test successful verification
        result = AuthService.verify_user('test@example.com', 'password')
        self.assertEqual(result, {'email': 'test@example.com', 'password': 'password'})
        
    @patch('services.auth_service.db')
    def test_verify_user_failure_by_email(self, mock_db):
        """
        Test user verification fails correctly when the email does not exist.
        """
        # Setup mock to return None, simulating user not found
        mock_db.users.find_one.return_value = None
        
        # Test verification failure
        with self.assertRaises(HTTPException) as context:
            AuthService.verify_user('test@example.com', 'password')
            
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Incorrect credentials")
        
    @patch('services.auth_service.db')
    def test_verify_user_failure_by_password(self, mock_db):
        """
        Test user verification fails correctly when the password is incorrect.
        """
        # Setup dummy data for the existing user but incorrect password scenario
        mock_db.users.find_one.return_value = {'email': 'test@example.com', 'password': 'password'}
        
        # Test verification failure
        with self.assertRaises(HTTPException) as context:
            AuthService.verify_user('test@example.com', 'not_password')
            
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Incorrect credentials")
    
    @patch('services.auth_service.db')
    def test_create_user_success(self, mock_db):
        """
        Test successful creation of a new user when no existing user is found.
        """
        # Setup mock to simulate user does not exist then return new user data
        user_data = {'email': 'test@example.com', 'password': 'password', "user_type": 'admin'}
        mock_db.users.find_one.side_effect = [None, user_data]  # No user found initially, then simulate user creation
        
        # Execution: Try to create the user
        try:
            AuthService.create_user(user_data)
        except HTTPException:
            self.fail("HTTPException was raised unexpectedly!")

        # Verification: Ensure the user was created correctly
        mock_db.users.find_one.assert_called_with({'email': 'test@example.com'})
        created_user = mock_db.users.find_one({'email': 'test@example.com'})
        self.assertEqual(created_user, user_data)
    
    @patch('services.auth_service.db')
    def test_create_user_failure(self, mock_db):
        """
        Test failure to create a user when the email already exists in the database.
        """
        # Setup: Mock find_one to return existing user data
        mock_db.users.find_one.return_value = {'email': 'exists@example.com'}
        
        # Execution: Attempt to create a user that should already exist
        with self.assertRaises(HTTPException) as context:
            AuthService.create_user({'email': 'exists@example.com', 'password': 'secure'})
            
        # Verification: Check correct HTTPException is raised
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Email already exists")

if __name__ == '__main__':
    unittest.main()
