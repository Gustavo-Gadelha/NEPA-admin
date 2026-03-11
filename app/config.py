import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

DEBUG = os.getenv("DEBUG")
SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_ECHO = False
