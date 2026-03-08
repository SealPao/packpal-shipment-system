from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from app.config import DEFAULT_EMPLOYEE_FILENAME
from services.settings_service import SettingsService


@dataclass(frozen=True)
class EmployeeRecord:
    employee_id: str
    name: str


class EmployeeService:
    def __init__(self, settings_service: SettingsService | None = None) -> None:
        self.settings_service = settings_service or SettingsService()

    def employee_file_path(self) -> Path:
        return self.settings_service.default_app_data_path() / DEFAULT_EMPLOYEE_FILENAME

    def load_records(self) -> list[EmployeeRecord]:
        target = self.employee_file_path()
        if not target.exists():
            return []

        records: list[EmployeeRecord] = []
        with target.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                employee_id = self._pick_value(row, "employee_id", "員工編號", "id")
                name = self._pick_value(row, "name", "員工名稱", "姓名")
                if employee_id and name:
                    records.append(EmployeeRecord(employee_id=employee_id, name=name))
        return records

    def save_records(self, records: list[EmployeeRecord]) -> int:
        cleaned: list[dict[str, str]] = []
        for record in records:
            employee_id = record.employee_id.strip()
            name = record.name.strip()
            if employee_id and name:
                cleaned.append({"employee_id": employee_id, "name": name})

        target = self.employee_file_path()
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["employee_id", "name"])
            writer.writeheader()
            writer.writerows(cleaned)
        return len(cleaned)

    def find_by_id(self, employee_id: str) -> EmployeeRecord | None:
        normalized = employee_id.strip()
        if not normalized:
            return None
        for record in self.load_records():
            if record.employee_id == normalized:
                return record
        return None

    def import_csv(self, source_path: str | Path) -> int:
        source = Path(source_path)
        rows = self._read_rows(source)
        return self.save_records([EmployeeRecord(**row) for row in rows])

    def export_sample_csv(self, target_path: str | Path) -> None:
        target = Path(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        sample_rows = [
            {"employee_id": "A001", "name": "王小明"},
            {"employee_id": "A002", "name": "陳美玲"},
            {"employee_id": "A003", "name": "林志豪"},
        ]
        with target.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["employee_id", "name"])
            writer.writeheader()
            writer.writerows(sample_rows)

    def _read_rows(self, source: Path) -> list[dict[str, str]]:
        rows: list[dict[str, str]] = []
        with source.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for raw_row in reader:
                employee_id = self._pick_value(raw_row, "employee_id", "員工編號", "id")
                name = self._pick_value(raw_row, "name", "員工名稱", "姓名")
                if employee_id and name:
                    rows.append({"employee_id": employee_id, "name": name})

        if not rows:
            raise ValueError("員工檔案沒有可匯入的資料，請確認包含員工編號與名稱欄位。")
        return rows

    @staticmethod
    def _pick_value(row: dict[str, object], *candidates: str) -> str:
        for candidate in candidates:
            value = row.get(candidate)
            if value is not None and str(value).strip():
                return str(value).strip()
        return ""
