from database.models import PayoutQueryParams


class PayoutService:
    """
    Service class to handle the creation of database query filters for payouts based on provided parameters.
    """

    @staticmethod
    def filter_payouts(params: PayoutQueryParams):
        """
        Generates MongoDB query filters for fetching payouts based on various criteria.

        Args:
        - params (PayoutQueryParams): A model that encapsulates all possible filter criteria.

        Returns:
        - json: A json containing MongoDB query filters.
        """

        # Extract parameters and exclude None values to ensure they don't affect the MongoDB query
        query_params = params.dict(exclude_none=True)
        match = {'created': {}, 'payment_date': {}}

        # Extracting parameters
        start_date = query_params.get("start_date")
        end_date = query_params.get("end_date")
        payment_start_date = query_params.get("payment_start_date")
        payment_end_date = query_params.get("payment_end_date")
        user_type = query_params.get("user_type")
        statuses = query_params.get("statuses")

        # Building the query filter for MongoDB based on the presence of parameters
        if start_date:
            match['created']['$gte'] = start_date
        if end_date:
            match['created']['$lte'] = end_date
        if payment_start_date:
            match['payment_date']['$gte'] = payment_start_date
        if payment_end_date:
            match['payment_date']['$lte'] = payment_end_date

        # Remove empty filters to prevent MongoDB from performing unnecessary operations
        if not match['created']:
            del match['created']
        if not match['payment_date']:
            del match['payment_date']

        # Additional filters based on user type and statuses
        if user_type:
            match['user_type'] = user_type
        if statuses:
            match['status'] = {'$in': statuses.split(",")}

        return match