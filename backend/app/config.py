import os
from pydantic import BaseModel


class Settings(BaseModel):
    sd_key: str = os.getenv("SPORTSDATAIO_API_KEY", "")
    season: str = os.getenv("SEASON", "2025REG")
    refetch_minutes: int = int(os.getenv("REFETCH_INTERVAL_MINUTES", "10"))
    use_llm: bool = os.getenv("USE_LLM", "false").lower() == "true"
    openai_key: str = os.getenv("OPENAI_API_KEY", "")
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")


settings = Settings()