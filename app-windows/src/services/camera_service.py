from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QSettings
from PySide6.QtMultimedia import QMediaDevices


@dataclass(frozen=True)
class CameraOption:
    id: str
    name: str


class CameraService:
    SETTINGS_KEY = "camera/selected_id"

    def list_cameras(self) -> list[CameraOption]:
        cameras: list[CameraOption] = []

        for device in QMediaDevices.videoInputs():
            camera_id = bytes(device.id()).decode("utf-8", errors="ignore")
            cameras.append(CameraOption(id=camera_id, name=device.description()))

        return cameras

    def load_selected_camera_id(self) -> str:
        settings = QSettings()
        return str(settings.value(self.SETTINGS_KEY, ""))

    def save_selected_camera_id(self, camera_id: str) -> None:
        settings = QSettings()
        settings.setValue(self.SETTINGS_KEY, camera_id)
        settings.sync()

    def get_selected_camera(self, cameras: list[CameraOption] | None = None) -> CameraOption | None:
        available_cameras = cameras if cameras is not None else self.list_cameras()
        selected_id = self.load_selected_camera_id()

        for camera in available_cameras:
            if camera.id == selected_id:
                return camera

        if available_cameras:
            fallback = available_cameras[0]
            self.save_selected_camera_id(fallback.id)
            return fallback

        return None