import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Amazon images"
    PROJECT_VERSION: str = "1.0.0"

    DATABASE_URL = ""
    SECRET_KEY: str = "f=-^*5qsy=z9a&#f9q@57ufz_-c^tldd$euiz1qs%+*w617xfs"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    BUCKET_NAME = "images.stateofyourhome.com"



settings = Settings()