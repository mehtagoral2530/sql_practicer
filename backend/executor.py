"""Execute read-only SQL against PostgreSQL or MySQL."""
from __future__ import annotations

import os
import re
from typing import Any

import pymysql
import psycopg2
from psycopg2.extras import RealDictCursor

ALLOWED_START = re.compile(
    r"^\s*(SELECT|WITH|SHOW|EXPLAIN)\b",
    re.IGNORECASE | re.DOTALL,
)
FORBIDDEN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|GRANT|REVOKE)\b",
    re.IGNORECASE,
)


def validate_sql_safe(sql: str) -> str | None:
    """Return error message if SQL is not allowed, else None."""
    stripped = sql.strip()
    if not stripped:
        return "Query is empty. Type a SELECT statement."
    if ";" in stripped.rstrip(";"):
        parts = [p.strip() for p in stripped.split(";") if p.strip()]
        if len(parts) > 1:
            return "Only one SQL statement at a time is allowed."
    if not ALLOWED_START.match(stripped):
        return "Only SELECT queries are allowed for practice (plus WITH, SHOW, EXPLAIN)."
    if FORBIDDEN.search(stripped):
        return "This query contains forbidden keywords. Use SELECT only."
    return None


def _pg_config() -> dict[str, Any]:
    return {
        "host": os.getenv("PG_HOST", "localhost"),
        "port": int(os.getenv("PG_PORT", "5433")),
        "dbname": os.getenv("PG_DB", "healthcare"),
        "user": os.getenv("PG_USER", "learner_ro"),
        "password": os.getenv("PG_PASSWORD", "learner"),
    }


def _mysql_config() -> dict[str, Any]:
    return {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3307")),
        "database": os.getenv("MYSQL_DB", "healthcare"),
        "user": os.getenv("MYSQL_USER", "learner_ro"),
        "password": os.getenv("MYSQL_PASSWORD", "learner"),
    }


def execute_query(sql: str, dialect: str) -> tuple[list[str], list[list[Any]], str | None]:
    """
    Run query. Returns (columns, rows, error_message).
    rows are JSON-serializable values.
    """
    safety = validate_sql_safe(sql)
    if safety:
        return [], [], safety

    try:
        if dialect == "postgres":
            return _execute_postgres(sql)
        return _execute_mysql(sql)
    except Exception as e:
        return [], [], str(e)


def _execute_postgres(sql: str) -> tuple[list[str], list[list[Any]], str | None]:
    conn = psycopg2.connect(**_pg_config())
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            if cur.description is None:
                return [], [], None
            cols = [d.name for d in cur.description]
            rows = [[_serialize(v) for v in row.values()] for row in cur.fetchall()]
            return cols, rows, None
    finally:
        conn.close()


def _execute_mysql(sql: str) -> tuple[list[str], list[list[Any]], str | None]:
    conn = pymysql.connect(**_mysql_config(), cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            if cur.description is None:
                return [], [], None
            cols = [d[0] for d in cur.description]
            raw = cur.fetchall()
            rows = [[_serialize(row[c]) for c in cols] for row in raw]
            return cols, rows, None
    finally:
        conn.close()


def _serialize(val: Any) -> Any:
    if val is None:
        return None
    if hasattr(val, "isoformat"):
        return val.isoformat()
    if isinstance(val, (int, float, str, bool)):
        return val
    return str(val)


def check_db_health(dialect: str) -> bool:
    try:
        if dialect == "postgres":
            conn = psycopg2.connect(**_pg_config())
        else:
            conn = pymysql.connect(**_mysql_config())
        conn.close()
        return True
    except Exception:
        return False
