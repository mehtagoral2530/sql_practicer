"""Load lesson JSON files from lessons/ directory."""
from __future__ import annotations

import json
from pathlib import Path

LESSONS_ROOT = Path(__file__).resolve().parent.parent / "lessons"
MANIFEST_PATH = LESSONS_ROOT / "manifest.json"

SCHEMA_SNIPPETS: dict[str, str] = {
    "hospitals": "hospital_id, name, org_type, state",
    "patients": "patient_id, hospital_id, age, insurance_type",
    "encounters": "encounter_id, patient_id, visit_date, department",
    "device_orders": "order_id, patient_id, device_name, unit_cost, order_date",
}


def load_manifest() -> list[dict]:
    data = json.loads(MANIFEST_PATH.read_text())
    return data["lessons"]


def load_lesson(lesson_id: str) -> dict | None:
    for entry in load_manifest():
        if entry["id"] == lesson_id:
            path = LESSONS_ROOT / entry["file"]
            lesson = json.loads(path.read_text())
            lesson["module"] = entry.get("module", "")
            lesson["schemaSnippet"] = {
                t: SCHEMA_SNIPPETS.get(t, "") for t in lesson.get("schemaTables", [])
            }
            return lesson
    return None


def list_lessons_summary() -> list[dict]:
    result = []
    for entry in load_manifest():
        path = LESSONS_ROOT / entry["file"]
        lesson = json.loads(path.read_text())
        result.append(
            {
                "id": lesson["id"],
                "title": lesson["title"],
                "module": entry.get("module", ""),
            }
        )
    return result
