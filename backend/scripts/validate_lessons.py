#!/usr/bin/env python3
"""Verify all lesson solutionSql queries run on PostgreSQL and MySQL."""
from __future__ import annotations

import json
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND))

from executor import execute_query  # noqa: E402
from lessons import LESSONS_ROOT, load_manifest  # noqa: E402


def main() -> int:
    failures: list[tuple[str, str, str]] = []
    checked = 0

    for entry in load_manifest():
        path = LESSONS_ROOT / entry["file"]
        lesson = json.loads(path.read_text())
        validation = lesson.get("validation", {})
        solution_sql = validation.get("solutionSql")
        if not solution_sql:
            continue

        lesson_id = lesson["id"]
        for dialect in ("postgres", "mysql"):
            checked += 1
            cols, rows, err = execute_query(solution_sql, dialect)
            if err:
                failures.append((lesson_id, dialect, err))
            elif not cols:
                failures.append((lesson_id, dialect, "query returned no columns"))

    if failures:
        print(f"FAILED: {len(failures)} of {checked} solution query runs")
        for lesson_id, dialect, err in failures:
            print(f"  {lesson_id} [{dialect}]: {err}")
        return 1

    lesson_count = len([e for e in load_manifest() if _has_solution(e)])
    print(
        f"OK: all {lesson_count} lesson solutionSql queries run on postgres and mysql "
        f"({checked} executions)"
    )
    return 0


def _has_solution(entry: dict) -> bool:
    path = LESSONS_ROOT / entry["file"]
    lesson = json.loads(path.read_text())
    return bool(lesson.get("validation", {}).get("solutionSql"))


if __name__ == "__main__":
    sys.exit(main())
