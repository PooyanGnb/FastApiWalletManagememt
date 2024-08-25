import unittest
from unittest.mock import patch, MagicMock
import asyncio
from pymongo.collection import Collection

from services.pagination_service import PaginationService

class TestPaginationService(unittest.TestCase):
    """
    Unit tests for the PaginationService class that handles data pagination.
    """

    @patch('services.pagination_service.WalletService.check_available_and_pending_balance')
    @patch('services.pagination_service.TextTransformService.convert_dict_camel_case')
    @patch('services.pagination_service.db')
    def test_create_paginate_response(self, mock_db, mock_convert, mock_wallet):
        """
        Test the create_paginate_response method for proper pagination logic, ensuring it handles
        MongoDB collection operations correctly and transforms documents appropriately.
        """
        # Create a mock MongoDB collection object
        mock_collection = MagicMock()
        mock_db.wallet.return_value = mock_collection
        
        # Set up method chaining for MongoDB collection operations
        mock_collection.find.return_value = mock_collection
        mock_collection.skip.return_value = mock_collection
        mock_collection.limit.return_value = mock_collection
        
        # Simulate count_documents and cursor iteration for a collection
        mock_collection.count_documents.return_value = 10  # Assume there are 10 documents total
        mock_docs = [{'_id': '123', 'data': 'value'} for _ in range(3)]
        mock_collection.__iter__.return_value = iter(mock_docs)
        
        # Mock data transformation and wallet balance check
        mock_convert.side_effect = lambda x: x  # Return unchanged document for simplicity
        mock_wallet.return_value = (100, 50)  # Mocked available and pending balances

        # Execute the pagination asynchronously
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            PaginationService.create_paginate_response(1, mock_collection, {}, add_wallet=True)
        )

        # Assertions to verify pagination results
        self.assertEqual(response['page'], 1)
        self.assertEqual(response['totalDocs'], 10)
        self.assertEqual(len(response['results']), 3)
        for doc in response['results']:
            self.assertIn('available_balance', doc)
            self.assertIn('pending_balance', doc)
            mock_convert.assert_called()

if __name__ == '__main__':
    unittest.main()
