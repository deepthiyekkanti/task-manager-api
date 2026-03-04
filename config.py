import os
from dotenv import load_dotenv
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
DATABASE_URL = os.environ["DATABASE_URL"]

ACCESS_TOKEN_EXPIRE_SECONDS = int(os.environ["ACCESS_TOKEN_EXPIRE_SECONDS"])
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ["REFRESH_TOKEN_EXPIRE_DAYS"])