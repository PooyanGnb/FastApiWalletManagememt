from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    """
    A model to validate login request data.
    """
    email: str # The email address of the user trying to log in.
    password: str # The password for the user trying to log in.

class SignupRequest(BaseModel):
    """
    A model to validate signup request data.
    """
    email: str # The email address of the user signing up.
    password: str # The chosen password for the new account.
    user_type: str # The type of user (e.g., admin).

class PayoutQueryParams(BaseModel):
    """
    A model for filtering payout queries.
    """
    statuses: Optional[str] = None # Filter payouts by statuses.
    page: Optional[int] = None # Page number for pagination
    start_date: Optional[datetime] = None # Filter payouts starting from this date.
    end_date: Optional[datetime] = None # Filter payouts up to this date.
    user_type: Optional[str] = None # Filter payouts by user type.
    payment_start_date: Optional[datetime] = None # Filter payouts with payments starting from this date.
    payment_end_date: Optional[datetime] = None # Filter payouts with payments up to this date.
