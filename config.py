import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get("BASE_URL", "https://www.saucedemo.com/")
LOGIN_USERNAME = os.environ.get("LOGIN_USERNAME", "standard_user")
LOGIN_PASSWORD = os.environ.get("LOGIN_PASSWORD", "secret_sauce")
