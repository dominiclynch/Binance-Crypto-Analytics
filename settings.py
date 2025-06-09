"""Runtime configuration for Analytics-API (FastAPI layer)."""
from pathlib import Path
from functools import lru_cache
from pydantic import AnyUrl, BaseSettings, Field


class Settings(BaseSettings):
    """Project-wide settings (override via ENV)."""

    data_api_url: AnyUrl = Field("http://localhost:8001", env="DATA_API_URL")
    signals_dir: Path = Path("/root/ml-engine/signals")
    market_db: Path = Path("/root/analytics-tool-v2/market_data.db")
    bucket_mapping: Path = Path("/root/analytics-tool-v2/bucket_mapping.csv")

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> "Settings":  # pragma: no cover
    """Return cached Settings instance."""
    return Settings()
