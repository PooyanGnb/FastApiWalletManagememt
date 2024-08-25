from fastapi import APIRouter, Depends

from services.payout_service import PayoutService
from services.pagination_service import PaginationService
from dependencies import check_user_is_admin
from database.connection import MongoDatabase
from database.models import PayoutQueryParams

# Initialize database connection
db = MongoDatabase()

# Configure router with relevant tags for organized documentation
router = APIRouter(tags=["Receipts"])

@router.get("/payout")
async def fetch_payouts(
    query_params: PayoutQueryParams = Depends(),
    admin: str = Depends(check_user_is_admin)
):
    """
    Fetches paginated payouts based on provided query parameters.

    Parameters:
    - query_params: Filter and pagination criteria for payouts.
    - admin: Admin status validated by dependency to ensure user has admin privileges.

    Returns:
    - json: Paginated list of payouts that match the query criteria.
    """

    # Generate MongoDB filter parameters from the query parameters
    match = PayoutService.filter_payouts(query_params)
    page = query_params.page  # Extract the page number directly from the query parameters

    # Retrieve paginated results based on the generated filters
    paginated_result = await PaginationService.create_paginate_response(page, db.payouts, match)
    return paginated_result