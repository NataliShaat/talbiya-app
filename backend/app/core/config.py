import os
from dotenv import load_dotenv # type: ignore

load_dotenv()


class Settings:
    ELM_BASE_URL: str = os.getenv("ELM_BASE_URL", "https://elmodels.ngrok.app/v1")
    ELM_API_KEY: str = os.getenv("ELM_API_KEY", "")
    ELM_MODEL: str = os.getenv("ELM_MODEL", "nuha-2.0")

    


settings = Settings()