import os

from app import errors
from dotenv import load_dotenv

# Load env from .env if possible.
load_dotenv(verbose=True)


class Config:
    ENVIRONMENT = os.environ.get("ENVIRONMENT")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO", False)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    silent_exceptions = os.environ.get(
        "SILENT_EXCEPTIONS", ["ENTRY_NOT_FOUND", "MISSING_ENTRY_DATA"]
    )
    SILENT_EXCEPTIONS = []
    for exception in silent_exceptions:
        value = getattr(errors, exception, None)
        if not value:
            continue
        SILENT_EXCEPTIONS.append(value)

    LOG_LEVEL = int(os.environ.get("LOG_LEVEL", 10))
