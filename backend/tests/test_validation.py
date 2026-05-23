import pytest

from validation import normalize_rows, rows_equal


class TestValidation:
    def test_rows_equal_order_insensitive(self):
        cols = ["a", "b"]
        a = [[1, "x"], [2, "y"]]
        b = [[2, "y"], [1, "x"]]
        assert rows_equal(cols, a, cols, b, order_sensitive=False)

    def test_rows_equal_order_sensitive(self):
        cols = ["a"]
        a = [[1], [2]]
        b = [[2], [1]]
        assert not rows_equal(cols, a, cols, b, order_sensitive=True)

    def test_normalize_floats(self):
        cols = ["v"]
        rows = [[1.001]]
        norm = normalize_rows(cols, rows)
        assert norm[0][0][1] == 1.0
