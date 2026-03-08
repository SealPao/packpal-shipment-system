from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QSettings, QStandardPaths


@dataclass(frozen=True)
class AppSettings:
    operator_name: str
    nas_url: str
    local_storage_path: str


class SettingsService:
    OPERATOR_KEY = "app/operator_name"
    NAS_URL_KEY = "nas/base_url"
    STORAGE_PATH_KEY = "storage/local_path"

    def default_storage_path(self) -> str:
        locations = QStandardPaths.standardLocations(QStandardPaths.StandardLocation.AppDataLocation)
        base = Path(locations[0]) if locations else Path.cwd() / ".packpal"
        target = base / "storage"
        target.mkdir(parents=True, exist_ok=True)
        return str(target)

    def load(self) -> AppSettings:
        settings = QSettings()
        return AppSettings(
            operator_name=str(settings.value(self.OPERATOR_KEY, "")),
            nas_url=str(settings.value(self.NAS_URL_KEY, "http://nas.local:8000")),
            local_storage_path=str(settings.value(self.STORAGE_PATH_KEY, self.default_storage_path())),
        )

    def save(self, data: AppSettings) -> None:
        settings = QSettings()
        settings.setValue(self.OPERATOR_KEY, data.operator_name)
        settings.setValue(self.NAS_URL_KEY, data.nas_url)
        settings.setValue(self.STORAGE_PATH_KEY, data.local_storage_path)
        settings.sync()