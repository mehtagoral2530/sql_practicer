"""Pytest configuration for backend tests."""
from __future__ import annotations

import os

import pytest

pytest_plugins: list[str] = []


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "integration: requires Docker Postgres and MySQL (skipped when SKIP_DB_TESTS=1)",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if os.getenv("SKIP_DB_TESTS") != "1":
        return
    skip = pytest.mark.skip(reason="SKIP_DB_TESTS=1")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip)
