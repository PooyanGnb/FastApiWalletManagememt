import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from datetime import datetime, timedelta

from services.wallet_service import WalletService


class TestWalletService(unittest.TestCase):
    """
    Test suite for WalletService class, which manages wallet-related operations.
    """

    def setUp(self):
        """
        Set up common test data used in different test cases.
        """
        self.valid_user_id = '507f1f77bcf86cd799439011'
        self.invalid_user_id = 'invalid_id'
        self.wallet_data = {
            'available_balance': 100,
            'transactions': [
                {'id': '1', 'amount': 50, 'date_available': datetime.now() + timedelta(days=-1)},
                {'id': '2', 'amount': 150, 'date_available': datetime.now() + timedelta(days=1)}
            ]
        }

    @patch('services.wallet_service.db')
    async def test_check_balances_valid_user(self, mock_db):
        """
        Test checking balances for a valid user. This test verifies that balances are correctly
        calculated and the database update function is called.
        """
        # Mock the MongoDB document
        mock_wallet_doc = MagicMock()
        mock_wallet_doc.find_one.return_value = self.wallet_data
        mock_wallet_doc.update_one = MagicMock()

        mock_db.wallet.return_value = mock_wallet_doc

        # Execute the service method
        available_balance, pending_balance = await WalletService.check_available_and_pending_balance(
            self.valid_user_id)
        
        # Assertions
        self.assertEqual(available_balance, 150)  # 100 initial + 50 from past transaction
        self.assertEqual(pending_balance, 150)  # Only the future transaction
        mock_wallet_doc.update_one.assert_called_once()

    @patch('services.wallet_service.db')
    async def test_check_balances_invalid_user(self, mock_db):
        """
        Test behavior with an invalid user ID. This test checks that an HTTPException is raised
        for an invalid user ID.
        """
        # Mock the MongoDB operation to not find the user
        mock_db.wallet.find_one.return_value = None
        
        # Expecting an HTTPException for invalid user ID
        with self.assertRaises(HTTPException) as context:
            await WalletService.check_available_and_pending_balance(self.invalid_user_id)
        
        self.assertEqual(context.exception.status_code, 400)

    @patch('services.wallet_service.db')
    async def test_check_balances_wallet_not_found(self, mock_db):
        """
        Test behavior when the wallet is not found in the database. This test checks that an
        HTTPException is raised for a missing wallet.
        """
        # Mock the MongoDB operation to not find the wallet
        mock_db.wallet.find_one.return_value = None
        
        # Expecting an HTTPException for wallet not found
        with self.assertRaises(HTTPException) as context:
            await WalletService.check_available_and_pending_balance(self.valid_user_id)
        
        self.assertEqual(context.exception.status_code, 404)


if __name__ == '__main__':
    unittest.main()
