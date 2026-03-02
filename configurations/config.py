from pydantic_settings import BaseSettings, SettingsConfigDict #type:ignore
from pathlib import Path

CURRENT_FOLDER = Path(__file__).parent.absolute()
ENV_FILE_PATH = CURRENT_FOLDER / ".env"

class Settings(BaseSettings):
    

    GH_TOKEN: str
    WHATS_APP_SEND_MESSAGE_URL: str
    LOCAL_FILE_MCP_SERVER: str
    LOCAL_FILE_SECRET_TOKEN: str
    SESSION_ID: str
    CODER_SKILLS: str = str(Path(__file__).parent / "skills" / "coder")


    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

settings = Settings()