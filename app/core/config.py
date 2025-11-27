import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    APP_NAME: str = "ControlZ"
    SECRET_KEY=os.getenv("SECRET_KEY")

settings = Settings()
