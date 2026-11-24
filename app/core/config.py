from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

APP_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """App settings. Each value can be overridden with an environment variable
    that starts with TAROT_, for example TAROT_DATA_PATH=/path/to/tarot.yaml."""

    model_config = SettingsConfigDict(env_prefix="TAROT_")

    app_name: str = "Tarot Card Generation API"
    data_path: Path = APP_DIR / "data" / "tarot.yaml"

    @property
    def tarot_data_path(self) -> Path:
        return self.data_path


settings = Settings()
