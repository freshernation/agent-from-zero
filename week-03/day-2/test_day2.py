"""Week 3, Day 2 - try, except, raise, and tools that never crash.

Run me:  pytest week-03/day-2 -v
"""

import pytest


class TestParseInt:
    @pytest.mark.parametrize("text,answer", [
        ("42", 42), ("-7", -7), ("  9 ", 9), ("abc", None), ("", None), ("4.5", None),
    ])
    def test_parse_int(self, load, text, answer):
        assert load("calc.py").parse_int(text) == answer


class TestCalculate:
    @pytest.mark.parametrize("expression,answer", [
        ("2+2", 4), ("17 * 23", 391), ("10 / 4", 2.5),
        ("(2 + 3) * 4", 20), ("7 - 9", -2), ("1.5 * 2", 3.0),
    ])
    def test_arithmetic(self, load, expression, answer):
        assert load("calc.py").calculate(expression) == answer

    @pytest.mark.parametrize("expression", [
        "__import__('os').system('ls')",
        "open('/etc/passwd').read()",
        "2 + abc",
        "print(1)",
        "9**9**9**9",
        "2 ** 3",
    ])
    def test_refuses_anything_unsafe(self, load, expression):
        with pytest.raises(ValueError) as caught:
            load("calc.py").calculate(expression)
        assert str(caught.value) == "Unsafe expression", (
            "Check the characters before evaluating. A tool that evaluates "
            "whatever it is handed is not a tool, it is a way in. (And ** is "
            "made of safe characters but can freeze the machine.)"
        )

    def test_divide_by_zero(self, load):
        with pytest.raises(ValueError) as caught:
            load("calc.py").calculate("1 / 0")
        assert str(caught.value) == "Cannot divide by zero"

    @pytest.mark.parametrize("expression", ["2 +", "", "   ", "(1 + 2", "* 3"])
    def test_not_a_calculation(self, load, expression):
        with pytest.raises(ValueError) as caught:
            load("calc.py").calculate(expression)
        assert str(caught.value) == "Not a calculation"


class TestCalculateTool:
    def test_answers_as_a_string(self, load):
        result = load("calc.py").calculate_tool("17 * 23")
        assert result == "391", (
            f"Got {result!r}. A tool hands back text - 391 and '391' are the "
            "same thing to whoever reads it."
        )

    @pytest.mark.parametrize("expression,answer", [
        ("1 / 0", "Error: Cannot divide by zero"),
        ("rm -rf /", "Error: Unsafe expression"),
        ("2 +", "Error: Not a calculation"),
    ])
    def test_reports_failure_instead_of_raising(self, load, expression, answer):
        assert load("calc.py").calculate_tool(expression) == answer

    def test_names_the_error_it_catches(self, load, source):
        load("calc.py").calculate_tool
        code = source("calc.py", code_only=True)
        assert "except:" not in code.replace(" ", ""), (
            "There is a bare `except:` in calc.py. Name the error you expect - "
            "a bare except hides your own typos."
        )


class TestLoadOrEmpty:
    def test_reads_good_json(self, load, tmp_path):
        path = tmp_path / "notes.json"
        path.write_text('[{"title": "milk"}]')
        assert load("storage.py").load_or_empty(path) == [{"title": "milk"}]

    def test_missing_file(self, load, tmp_path):
        assert load("storage.py").load_or_empty(tmp_path / "nope.json") == []

    @pytest.mark.parametrize("damaged", ["", "{not json", "[1, 2,"])
    def test_damaged_file(self, load, tmp_path, damaged):
        path = tmp_path / "notes.json"
        path.write_text(damaged)
        assert load("storage.py").load_or_empty(path) == [], (
            "A file that is not valid JSON should give [] rather than crash."
        )
