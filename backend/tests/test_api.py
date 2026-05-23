import os
import time

import pytest
from fastapi.testclient import TestClient

from executor import check_db_health
from main import app

client = TestClient(app)


def _dbs_ready() -> bool:
    return check_db_health("postgres") and check_db_health("mysql")


@pytest.fixture(scope="session", autouse=True)
def wait_for_dbs():
    if os.getenv("SKIP_DB_TESTS") == "1":
        yield
        return
    for _ in range(30):
        if _dbs_ready():
            break
        time.sleep(1)
    yield


@pytest.mark.skipif(os.getenv("SKIP_DB_TESTS") == "1", reason="SKIP_DB_TESTS=1")
class TestExecutorIntegration:
    @pytest.mark.parametrize("dialect", ["postgres", "mysql"])
    def test_select_hospitals(self, dialect):
        if not check_db_health(dialect):
            pytest.skip(f"{dialect} not available")
        from executor import execute_query

        cols, rows, err = execute_query("SELECT COUNT(*) AS c FROM hospitals", dialect)
        assert err is None
        assert cols == ["c"]
        assert rows[0][0] == 5


@pytest.mark.skipif(os.getenv("SKIP_DB_TESTS") == "1", reason="SKIP_DB_TESTS=1")
class TestAPI:
    def test_health(self):
        r = client.get("/api/health")
        assert r.status_code == 200
        data = r.json()
        assert "postgres" in data

    def test_lessons_list(self):
        r = client.get("/api/lessons")
        assert r.status_code == 200
        assert len(r.json()) >= 25

    def test_run_fro_typo(self):
        r = client.post(
            "/api/run",
            json={
                "sql": "SELECT name\nFRMO hospitals",
                "dialect": "postgres",
                "lessonId": "01-01-hello-select",
            },
        )
        data = r.json()
        assert data["ok"] is False
        assert data["error"]["line"] == 2
        assert "FROM" in data["error"]["fix"]

    @pytest.mark.parametrize("dialect", ["postgres", "mysql"])
    def test_run_lesson1_pass(self, dialect):
        if not check_db_health(dialect):
            pytest.skip(f"{dialect} not available")
        r = client.post(
            "/api/run",
            json={
                "sql": "SELECT name FROM hospitals",
                "dialect": dialect,
                "lessonId": "01-01-hello-select",
            },
        )
        data = r.json()
        assert data["ok"] is True
        assert data["passed"] is True
