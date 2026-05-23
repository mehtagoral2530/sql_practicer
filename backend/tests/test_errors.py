import pytest

from errors import (
    RawError,
    build_teaching_error,
    extract_db_error_line,
    guess_line_from_sql,
)
from executor import validate_sql_safe


class TestErrors:
    def test_guess_line_fro_typo(self):
        sql = "SELECT name\nFRMO hospitals"
        assert guess_line_from_sql(sql, "FRMO") == 2

    def test_build_teaching_fro_typo(self):
        raw = RawError(line=2, column=None, message="syntax error", source="parser")
        sql = "SELECT name\nFRMO hospitals"
        err = build_teaching_error(raw, sql, "postgres", ["hospitals"])
        assert err.line == 2
        assert "FRMO" in err.why
        assert "FROM" in err.fix

    def test_extract_pg_line(self):
        msg = 'ERROR:  syntax error at or near "FRMO"\nLINE 2: FRMO hospitals'
        assert extract_db_error_line(msg, "postgres") == 2

    def test_extract_mysql_line(self):
        msg = "You have an error in your SQL syntax near 'FRMO' at line 2"
        assert extract_db_error_line(msg, "mysql") == 2

    def test_group_by_teaching(self):
        raw = RawError(
            line=1,
            column=None,
            message='column "name" must appear in the GROUP BY clause',
            source="database",
        )
        err = build_teaching_error(raw, "SELECT name, COUNT(*) FROM t", "postgres")
        assert "GROUP BY" in err.title


class TestExecutorSafety:
    def test_rejects_delete(self):
        assert validate_sql_safe("DELETE FROM hospitals") is not None

    def test_rejects_multi_statement(self):
        assert validate_sql_safe("SELECT 1; SELECT 2") is not None

    def test_allows_select(self):
        assert validate_sql_safe("SELECT 1") is None
