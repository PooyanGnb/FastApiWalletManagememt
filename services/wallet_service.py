from fastapi import HTTPException
from datetime import datetime
from bson.objectid import ObjectId

from database.connection import MongoDatabase


# Initialize a database connection
db = MongoDatabase()

class WalletService:
    """
    Service class to manage wallet-related operations.
    """

    @staticmethod
    async def check_available_and_pending_balance(user_id):
        """
        Checks and returns the available and pending balances for a specified user's wallet.
        
        Args:
        - user_id (str): The MongoDB ObjectId string of the user whose balance is being checked.

        Returns:
        - tuple: A tuple containing the available balances.

        Raises:
        - HTTPException: If the user_id is not a valid ObjectId or if the wallet data is not found.
        """

        # Validate the user_id is a proper ObjectId
        if not ObjectId.is_valid(user_id):
            raise HTTPException(detail="not valid object id", status_code=400)
        
        # Retrieve the wallet data from the database
        wallet = db.wallet.find_one({"user_id": ObjectId(user_id)})
        if not wallet:
            raise HTTPException(detail="Wallet not found.", status_code=404)
        
        # Calculate available balances
        available_balance = wallet.get('available_balance', 0)
        pending_balance = 0
        transactions_to_delete = []
        for transaction in wallet["transactions"]:
            if transaction["date_available"] <= datetime.now():
                available_balance += transaction["amount"]
                transactions_to_delete.append(transaction["id"])
            else:
                pending_balance += transaction["amount"]

        # Update the wallet with the new balances
        wallet.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "available_balance": available_balance,
                    "pending_balance": pending_balance,
                },
                "$pull": {
                    "transactions": {"id": {"$in": transactions_to_delete}}
                },
            },
        )

        return available_balance, pending_balance
