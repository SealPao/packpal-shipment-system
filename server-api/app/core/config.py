from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("PACKPAL_API_NAME", "PackPal Shipment System API")
    app_version: str = os.getenv("PACKPAL_API_VERSION", "0.1.0")
    debug: bool = os.getenv("PACKPAL_API_DEBUG", "false").lower() == "true"
    environment: str = os.getenv("PACKPAL_API_ENV", "development")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
