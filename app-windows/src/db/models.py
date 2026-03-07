from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LocalRecordDraft:
    id: int
    module_key: str
    payload_json: str
    camera_name: str
    updated_at: str