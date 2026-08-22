import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Force load the .env file explicitly
load_dotenv()

class Settings(BaseSettings):
    # No default value here; Pydantic will throw an error if it can't find it
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") 
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    CHROMA_DB_DIR: str = "./chroma_db"
    
    DATA_DIR: str = "./data"
    EXCEL_FILE_PATH: str = os.path.join(DATA_DIR, "ParcelPilot_Assessment_Data.xlsx")
    DOCS_DIR: str = os.path.join(DATA_DIR, "documents")
    SQLITE_DB_PATH: str = "./parcelpilot.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# Final safety check before the app starts
if not settings.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing! Make sure your .env file is correct.")