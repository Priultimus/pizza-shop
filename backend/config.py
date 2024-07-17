import os

from dotenv import load_dotenv

# Load env from .env if possible.
load_dotenv(verbose=True)


class Config:
    ENVIRONMENT = os.environ.get("ENVIRONMENT")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO", False)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_LEVEL = int(os.environ.get("LOG_LEVEL", 10))
