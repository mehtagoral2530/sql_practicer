"""Lesson validation: compare user results to expected."""
from __future__ import annotations

from typing import Any

from executor import execute_query


def normalize_rows(cols: list[str], rows: list[list[Any]]) -> list[tuple]:
    """Sort rows for order-insensitive comparison."""
    indexed = []
    for row in rows:
        d = {cols[i]: row[i] for i in range(len(cols))}
        indexed.append(tuple(sorted((k, _norm_val(v)) for k, v in d.items())))
    return sorted(indexed)


def _norm_val(v: Any) -> Any:
    if isinstance(v, float):
        return round(v, 2)
    if isinstance(v, str) and v.replace(".", "", 1).isdigit():
        try:
            return round(float(v), 2)
        except ValueError:
            pass
    return v


def rows_equal(
    cols_a: list[str],
    rows_a: list[list[Any]],
    cols_b: list[str],
    rows_b: list[list[Any]],
    order_sensitive: bool = False,
) -> bool:
    if cols_a != cols_b:
        return False
    if order_sensitive:
        na = [_row_tuple(cols_a, r) for r in rows_a]
        nb = [_row_tuple(cols_b, r) for r in rows_b]
        return na == nb
    return normalize_rows(cols_a, rows_a) == normalize_rows(cols_b, rows_b)


def _row_tuple(cols: list[str], row: list[Any]) -> tuple:
    return tuple((cols[i], _norm_val(row[i])) for i in range(len(cols)))


def validate_lesson(
    user_sql: str,
    dialect: str,
    validation: dict[str, Any],
) -> tuple[bool, str | None]:
    """
    Returns (passed, feedback_message).
    feedback_message is None on pass, or a hint on fail.
    """
    vtype = validation.get("type", "runs_only")

    u_cols, u_rows, u_err = execute_query(user_sql, dialect)
    if u_err:
        return False, None  # execution error handled elsewhere

    if vtype == "runs_only":
        return True, None

    if vtype == "row_count_min":
        min_rows = validation.get("minRows", 1)
        if len(u_rows) >= min_rows:
            return True, None
        return False, f"Expected at least {min_rows} rows, got {len(u_rows)}."

    if vtype == "result_match":
        solution_sql = validation["solutionSql"]
        order_sensitive = validation.get("orderSensitive", False)
        s_cols, s_rows, s_err = execute_query(solution_sql, dialect)
        if s_err:
            return False, "Internal error: solution query failed."
        if rows_equal(u_cols, u_rows, s_cols, s_rows, order_sensitive):
            return True, None
        return False, "Your results do not match yet. Check columns, filters, and ORDER BY."

    return True, None
