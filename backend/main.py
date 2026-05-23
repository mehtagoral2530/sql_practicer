"""FastAPI backend for SQL Healthcare Practice."""
from __future__ import annotations

from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from errors import (
    RawError,
    build_teaching_error,
    extract_db_error_line,
    parse_sql_syntax,
    teaching_error_to_dict,
)
from executor import check_db_health, execute_query, validate_sql_safe
from lessons import list_lessons_summary, load_lesson
from validation import validate_lesson

app = FastAPI(title="SQL Healthcare Practice API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    sql: str
    dialect: Literal["postgres", "mysql"] = "postgres"
    lessonId: str | None = None


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {
        "postgres": check_db_health("postgres"),
        "mysql": check_db_health("mysql"),
    }


@app.get("/api/lessons")
def get_lessons() -> list[dict]:
    return list_lessons_summary()


@app.get("/api/lessons/{lesson_id}")
def get_lesson(lesson_id: str) -> dict:
    lesson = load_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    # hide solution from client
    safe = {k: v for k, v in lesson.items() if k != "validation"}
    safe["hasValidation"] = "validation" in lesson
    return safe


@app.post("/api/run")
def run_query(body: RunRequest) -> dict[str, Any]:
    sql = body.sql
    dialect = body.dialect
    lesson = load_lesson(body.lessonId) if body.lessonId else None
    schema_tables = lesson.get("schemaTables", []) if lesson else []

    # Safety check (returns teaching error without DB)
    safety = validate_sql_safe(sql)
    if safety:
        raw = RawError(line=1, column=None, message=safety, source="guard")
        err = build_teaching_error(raw, sql, dialect, schema_tables)
        return {"ok": False, "error": teaching_error_to_dict(err), "sql": sql}

    # Syntax parse
    syntax = parse_sql_syntax(sql, dialect)
    if syntax:
        err = build_teaching_error(syntax, sql, dialect, schema_tables)
        return {"ok": False, "error": teaching_error_to_dict(err), "sql": sql}

    cols, rows, db_err = execute_query(sql, dialect)
    if db_err:
        line = extract_db_error_line(db_err, dialect) or 1
        raw = RawError(line=line, column=None, message=db_err, source="database")
        err = build_teaching_error(raw, sql, dialect, schema_tables)
        return {"ok": False, "error": teaching_error_to_dict(err), "sql": sql}

    passed = False
    feedback: str | None = None
    if lesson and "validation" in lesson:
        passed, feedback = validate_lesson(sql, dialect, lesson["validation"])

    return {
        "ok": True,
        "passed": passed,
        "feedback": feedback,
        "columns": cols,
        "rows": rows,
        "rowCount": len(rows),
        "sql": sql,
    }
