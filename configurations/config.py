from pydantic_settings import BaseSettings, SettingsConfigDict #type:ignore
from pathlib import Path

CURRENT_FOLDER = Path(__file__).parent.absolute()
ENV_FILE_PATH = CURRENT_FOLDER / ".env"

class Settings(BaseSettings):
    

    ANTHROPIC_API_KEY: str
    WHATS_APP_SEND_MESSAGE_URL: str
    LOCAL_FILE_MCP_SERVER: str
    GMAIL_MCP_SERVER: str
    CALENDAR_MCP_SERVER: str


    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

settings = Settings()