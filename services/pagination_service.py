from datetime import datetime

from .wallet_service import WalletService
from .text_service import TextTransformService
from database.connection import MongoDatabase

# Initialize a database connection
db = MongoDatabase()

class PaginationService:
    """
    Service class to handle pagination of database queries.
    """
        
    DEFAULT_PAGE_SIZE = 3 # Standard size for pagination results

    @staticmethod
    async def create_paginate_response(page, collection, match, add_wallet=False):
        """
        Create a paginated response based on the database query.

        Args:
        - page (int): The current page number requested.
        - collection: The MongoDB collection to query.
        - match (json): The query parameters as a json.
        _ add_wallet (bool): Flag to decide if wallet data should be added to the results.

        Returns:
        - json: A json containing pagination data and results.
        """

        page, total_docs, result = await PaginationService.paginate_results(
            page, collection, match, add_wallet
        )
        
        return {
            "page": page,
            "pageSize": PaginationService.DEFAULT_PAGE_SIZE,
            "totalPages": -(-total_docs // PaginationService.DEFAULT_PAGE_SIZE),
            "totalDocs": total_docs if page else len(result),
            "results": result,
        }

    @staticmethod
    async def paginate_results(page, collection, match, add_wallet=False):
        """
        Helper method to fetch paginated documents from a database collection.

        Args:
        - page (int): The current page number requested.
        - collection: The MongoDB collection to query.
        - match (json): The query parameters as a json.
        - add_wallet (bool): Flag to decide if wallet data should be appended to each document.

        Returns:
        - tuple: A tuple containing the current page, total number of documents, and list of documents.
        """

        total_docs = 0
        result = []

        if page is not None:
            # Calculate total documents matching the query for pagination metadata
            total_docs = collection.count_documents(match)

            # Calculate the number of documents to skip based on the current page number and page size
            skip = (page - 1) * PaginationService.DEFAULT_PAGE_SIZE

            # Define the limit, which is the maximum number of documents to return
            limit = PaginationService.DEFAULT_PAGE_SIZE

            # Fetch the paginated documents from MongoDB, applying skip and limit for pagination
            cursor = collection.find(match).skip(skip).limit(limit)

            # Convert each document's keys from snake_case to camelCase asynchronously
            result = [await TextTransformService.convert_dict_camel_case(doc)
                      for doc in cursor]
        else:
            # If no page is specified, retrieve all documents matching the query
            cursor = collection.find(match)
            result = list(cursor)

        # Iterate over each document to possibly add wallet data and convert key naming format
        if add_wallet:
            for index, doc in enumerate(result):
                # Check and append the wallet balance details to the document if add_wallet is True
                available_balance, pending_balance = await WalletService.check_available_and_pending_balance(doc["_id"])
                doc.update({
                    "available_balance": available_balance,
                    "pending_balance": pending_balance
                })

                # Convert the document's keys from snake_case to camelCase
                result[index] = await TextTransformService.convert_dict_camel_case(doc)

        return page, total_docs, result

