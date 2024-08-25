import unittest
from datetime import datetime
from database.models import PayoutQueryParams
from services.payout_service import PayoutService

class TestPayoutService(unittest.TestCase):
    """
    Unit tests for the PayoutService class that handles creating filters for MongoDB queries
    based on given payout query parameters.
    """

    def test_filter_payouts_full(self):
        """
        Test the creation of a full filter with all fields specified.
        This tests the ability to create complex MongoDB queries from a full set of parameters.
        """
        # Setup: Fully specified payout parameters
        params = PayoutQueryParams(
            start_date=datetime(2021, 1, 1),
            end_date=datetime(2021, 1, 31),
            payment_start_date=datetime(2021, 1, 15),
            payment_end_date=datetime(2021, 1, 20),
            user_type='contractor',
            statuses='pending,completed'
        )
        
        # Expected MongoDB query filters
        expected_match = {
            'created': {'$gte': datetime(2021, 1, 1), '$lte': datetime(2021, 1, 31)},
            'payment_date': {'$gte': datetime(2021, 1, 15), '$lte': datetime(2021, 1, 20)},
            'user_type': 'contractor',
            'status': {'$in': ['pending', 'completed']}
        }
        
        # Execute the service method
        result = PayoutService.filter_payouts(params)
        
        # Assert the expected MongoDB query is constructed correctly
        self.assertEqual(result, expected_match)

    def test_filter_payouts_partial(self):
        """
        Test the creation of a filter with some fields left unspecified (None).
        This ensures that the service can handle partial input gracefully.
        """
        # Setup: Partially specified payout parameters
        params = PayoutQueryParams(
            start_date=datetime(2021, 1, 1),
            end_date=None,
            payment_start_date=None,
            payment_end_date=None,
            user_type=None,
            statuses=None
        )
        
        # Expected MongoDB query filters with only start_date
        expected_match = {
            'created': {'$gte': datetime(2021, 1, 1)}
        }
        
        # Execute the service method
        result = PayoutService.filter_payouts(params)
        
        # Assert only the relevant filter is applied
        self.assertEqual(result, expected_match)

    def test_filter_payouts_empty(self):
        """
        Test the creation of a filter when no fields are specified.
        This checks the service's ability to handle empty input, expecting no filters to apply.
        """
        # Setup: Empty payout parameters
        params = PayoutQueryParams()
        
        # Expected MongoDB query filters should be empty
        expected_match = {}
        
        # Execute the service method
        result = PayoutService.filter_payouts(params)
        
        # Assert no filters are created
        self.assertEqual(result, expected_match)


if __name__ == '__main__':
    unittest.main()
