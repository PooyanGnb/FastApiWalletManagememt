from pymongo import MongoClient
from dotenv import load_dotenv

from settings import Settings


settings = Settings() # Load settings using the Settings class which pulls from environment variables

class MongoDatabase:
    """
    A class for handling connections to MongoDB
    """

    def __init__(self):
        """
        Initializes a new instance of the MongoDatabase class.
        This includes loading environment variables, setting 
        up MongoDB client with settings from the environment,
        and connecting to the specified database.
        """
        load_dotenv()
        self.client = MongoClient(
            host=settings.mongo_host,
            port=27017,
            username=settings.mongo_username,
            password=settings.mongo_password
        )
        self.db = self.client[settings.mongo_database]
        
    @property
    def users(self):
        """
        Provides access to the 'users' collection of the database.
        """
        return self.db['users']
    
    @property
    def wallet(self):
        """
        Provides access to the 'user_wallet' collection of the database.
        """        
        return self.db['user_wallet']
    
    @property
    def payouts(self):
        """
        Provides access to the 'payout_affiliate' collection of the database.
        """
        return self.db['payout_affiliate']
