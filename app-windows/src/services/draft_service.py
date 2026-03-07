from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

from db.models import LocalRecordDraft
from db.session import connect, initialize_database


class DraftService:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = db_path
        initialize_database(self.db_path)

    def save_draft(self, module_key: str, payload: dict[str, str], camera_name: str = "") -> int:
        updated_at = datetime.now(timezone.utc).isoformat()
        payload_json = json.dumps(payload, ensure_ascii=False)

        with connect(self.db_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO record_drafts (module_key, payload_json, camera_name, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (module_key, payload_json, camera_name, updated_at),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def latest_draft(self, module_key: str) -> LocalRecordDraft | None:
        with connect(self.db_path) as connection:
            row = connection.execute(
                """
                SELECT id, module_key, payload_json, camera_name, updated_at
                FROM record_drafts
                WHERE module_key = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (module_key,),
            ).fetchone()

        if row is None:
            return None

        return LocalRecordDraft(
            id=int(row["id"]),
            module_key=str(row["module_key"]),
            payload_json=str(row["payload_json"]),
            camera_name=str(row["camera_name"]),
            updated_at=str(row["updated_at"]),
        )

    def parse_payload(self, draft: LocalRecordDraft | None) -> dict[str, str]:
        if draft is None:
            return {}
        return {key: str(value) for key, value in json.loads(draft.payload_json).items()}