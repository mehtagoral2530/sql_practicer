"""Parse SQL errors and produce teaching feedback with line numbers."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import sqlglot
from sqlglot import parse_one
from sqlglot.errors import ParseError


@dataclass
class RawError:
    line: int
    column: int | None
    message: str
    source: str  # "parser" | "database"


@dataclass
class TeachingError:
    line: int
    column: int | None
    severity: str
    title: str
    why: str
    fix: str
    suggestions: list[str]
    source: str
    raw_message: str


def parse_sql_syntax(sql: str, dialect: str) -> RawError | None:
    """Return syntax error from sqlglot before hitting the database."""
    try:
        parse_one(sql, read=dialect)
        return None
    except ParseError as e:
        line = 1
        col = None
        if hasattr(e, "errors") and e.errors:
            err = e.errors[0]
            line = err.get("line", 1) or 1
            col = err.get("col")
        else:
            m = re.search(r"line (\d+)", str(e), re.I)
            if m:
                line = int(m.group(1))
        return RawError(line=line, column=col, message=str(e), source="parser")


def extract_db_error_line(message: str, dialect: str) -> int | None:
    """Extract 1-based line number from PostgreSQL or MySQL error text."""
    if dialect == "postgres":
        m = re.search(r"LINE (\d+):", message, re.I)
        if m:
            return int(m.group(1))
        m = re.search(r"at character (\d+)", message, re.I)
        if m:
            return _line_from_char_offset(message, int(m.group(1)))
    else:
        m = re.search(r"at line (\d+)", message, re.I)
        if m:
            return int(m.group(1))
    return None


def _line_from_char_offset(sql: str, char_pos: int) -> int:
    line = 1
    for i, ch in enumerate(sql):
        if i >= char_pos - 1:
            break
        if ch == "\n":
            line += 1
    return line


def guess_line_from_sql(sql: str, keyword: str) -> int | None:
    """Fallback: find line containing a keyword (e.g. FRMO)."""
    upper = keyword.upper()
    for i, line in enumerate(sql.splitlines(), start=1):
        if upper in line.upper():
            return i
    return None


def build_teaching_error(
    raw: RawError,
    sql: str,
    dialect: str,
    schema_tables: list[str] | None = None,
) -> TeachingError:
    msg = raw.message.lower()
    schema_tables = schema_tables or []
    suggestions: list[str] = []
    title = "SQL error"
    why = raw.message
    fix = f"Review line {raw.line} and fix the issue there."

    # Typo: FRMO instead of FROM
    if "frmo" in sql.lower() or "frmo" in msg:
        line = guess_line_from_sql(sql, "FRMO") or raw.line
        return TeachingError(
            line=line,
            column=raw.column,
            severity="error",
            title="Syntax error near FROM",
            why="SQL keywords must be spelled exactly. `FRMO` is not a valid keyword.",
            fix=f"Change `FRMO` to `FROM` on line {line}.",
            suggestions=["Pattern: SELECT columns FROM table_name;"],
            source=raw.source,
            raw_message=raw.message,
        )

    # Missing FROM
    if "from" in msg and ("expected" in msg or "syntax" in msg):
        suggestions.append("Every SELECT needs a FROM clause: SELECT col1, col2 FROM table_name;")

    # GROUP BY
    if "group by" in msg or "must appear in the group by" in msg:
        return TeachingError(
            line=raw.line,
            column=raw.column,
            severity="error",
            title="GROUP BY required",
            why="When you use COUNT(), SUM(), or AVG(), every other column in SELECT must be in GROUP BY.",
            fix="Add GROUP BY with each non-aggregated column, or remove extra columns from SELECT.",
            suggestions=[
                "Example: SELECT department, COUNT(*) FROM encounters GROUP BY department;"
            ],
            source=raw.source,
            raw_message=raw.message,
        )

    # Table does not exist
    if "does not exist" in msg or "doesn't exist" in msg or "unknown table" in msg:
        tables_hint = ", ".join(schema_tables) if schema_tables else "hospitals, patients, encounters, device_orders"
        return TeachingError(
            line=raw.line,
            column=raw.column,
            severity="error",
            title="Table or column not found",
            why="The database could not find that table or column name.",
            fix=f"Check spelling. Tables in this lesson: {tables_hint}.",
            suggestions=["Table names are lowercase: hospitals, patients, encounters, device_orders."],
            source=raw.source,
            raw_message=raw.message,
        )

    # Ambiguous column
    if "ambiguous" in msg:
        return TeachingError(
            line=raw.line,
            column=raw.column,
            severity="error",
            title="Ambiguous column name",
            why="Two tables have a column with the same name, so the database does not know which one you mean.",
            fix="Prefix the column with the table name, e.g. patients.patient_id.",
            suggestions=["Example: SELECT patients.patient_id, hospitals.name FROM patients JOIN hospitals ..."],
            source=raw.source,
            raw_message=raw.message,
        )

    # Column does not exist
    if "column" in msg and ("does not exist" in msg or "unknown column" in msg):
        return TeachingError(
            line=raw.line,
            column=raw.column,
            severity="error",
            title="Column not found",
            why="That column name is not on the table you are querying.",
            fix="Check spelling and that you selected FROM the correct table.",
            suggestions=["Use SELECT * FROM table_name LIMIT 5; to see available columns."],
            source=raw.source,
            raw_message=raw.message,
        )

    # Syntax error generic
    if "syntax" in msg:
        title = "Syntax error"
        why = "The database could not understand your SQL. Check spelling of keywords and commas."
        fix = f"Focus on line {raw.line}. Common issues: missing comma, typo in SELECT/FROM/WHERE."
        suggestions.append("Keywords: SELECT, FROM, WHERE, ORDER BY, GROUP BY, HAVING, JOIN, ON.")

    return TeachingError(
        line=raw.line,
        column=raw.column,
        severity="error",
        title=title,
        why=why,
        fix=fix,
        suggestions=suggestions,
        source=raw.source,
        raw_message=raw.message,
    )


def teaching_error_to_dict(err: TeachingError) -> dict[str, Any]:
    return {
        "line": err.line,
        "column": err.column,
        "severity": err.severity,
        "title": err.title,
        "why": err.why,
        "fix": err.fix,
        "suggestions": err.suggestions,
        "source": err.source,
        "rawMessage": err.raw_message,
    }
