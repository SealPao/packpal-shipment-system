from __future__ import annotations

import sys
from pathlib import Path


APP_NAME = "PackPal Shipment System"
APP_TITLE = "出貨小幫手"
APP_ORG_NAME = "PackPal"
APP_ORG_DOMAIN = "packpal.local"
WINDOW_MIN_WIDTH = 960
WINDOW_MIN_HEIGHT = 640
DEFAULT_DB_FILENAME = "packpal-local.db"
DEFAULT_EMPLOYEE_FILENAME = "employees.csv"


def runtime_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS"))
    return Path(__file__).resolve().parents[3]


def logo_path() -> Path:
    return runtime_root() / "Logo.png"
