from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the application, loading values from an environment file.
    """

    mongo_host: str
    mongo_database: str
    mongo_username: str
    mongo_password: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_expiration_minutes: int

    class Config:
        env_file = ".env"