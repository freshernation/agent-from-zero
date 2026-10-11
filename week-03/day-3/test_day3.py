"""Week 3, Day 3 - modules, the main guard, and writing tests.

Run me:  pytest week-03/day-3 -v
"""

import pytest

BROKEN = {
    "clamp ignores the lower bound": '''
def clamp(value, low, high):
    if value > high:
        return high
    return value

def percent(part, whole):
    if whole == 0:
        raise ValueError("Cannot take a percentage of zero")
    return part / whole * 100
''',
    "clamp ignores the upper bound": '''
def clamp(value, low, high):
    if value < low:
        return low
    return value

def percent(part, whole):
    if whole == 0:
        raise ValueError("Cannot take a percentage of zero")
    return part / whole * 100
''',
    "percent returns a fraction": '''
def clamp(value, low, high):
    return max(low, min(high, value))

def percent(part, whole):
    if whole == 0:
        raise ValueError("Cannot take a percentage of zero")
    return part / whole
''',
    "percent does not refuse zero": '''
def clamp(value, low, high):
    return max(low, min(high, value))

def percent(part, whole):
    if whole == 0:
        return 0
    return part / whole * 100
''',
}


class TestMathtools:
    @pytest.mark.parametrize("value,answer", [(5, 5), (-3, 0), (99, 10), (0, 0), (10, 10)])
    def test_clamp(self, load, value, answer):
        assert load("mathtools.py").clamp(value, 0, 10) == answer

    def test_percent(self, load):
        module = load("mathtools.py")
        assert module.percent(1, 4) == 25.0
        assert module.percent(1, 3) == pytest.approx(33.333, abs=0.01)

    def test_percent_refuses_zero(self, load):
        with pytest.raises(ValueError) as caught:
            load("mathtools.py").percent(1, 0)
        assert str(caught.value) == "Cannot take a percentage of zero"


class TestReport:
    @pytest.mark.parametrize("done,total,answer", [
        (3, 12, "3 of 12 (25%)"),
        (1, 3, "1 of 3 (33%)"),
        (12, 12, "12 of 12 (100%)"),
        (15, 12, "15 of 12 (100%)"),
        (0, 0, "nothing to do"),
    ])
    def test_progress(self, load, done, total, answer):
        assert load("report.py").progress(done, total) == answer

    def test_imports_rather_than_copies(self, load, source):
        load("report.py").progress
        code = source("report.py", code_only=True)
        assert "mathtools" in code, "report.py should import from mathtools."
        assert "def percent" not in code and "def clamp" not in code, (
            "percent and clamp are defined again in report.py. Import them."
        )

    def test_importing_prints_nothing(self, load, capsys):
        load("report.py").progress
        assert capsys.readouterr().out == "", (
            "Importing report.py printed something. Put the call to main() "
            'behind  if __name__ == "__main__":'
        )

    def test_running_it_prints_the_report(self, run):
        assert run("report.py").line(0) == "3 of 12 (25%)"


class TestYourTests:
    def test_there_are_at_least_five(self, source):
        count = source("test_mine.py", code_only=True).count("def test_")
        assert count >= 5, f"test_mine.py has {count} test(s). Write at least five."

    def test_they_pass_against_your_own_code(self, load, run_tests_against):
        load("mathtools.py").clamp
        outcome = run_tests_against("test_mine.py", {}, also_copy=["mathtools.py"])
        assert not outcome.no_tests, "pytest found no tests in test_mine.py."
        assert outcome.passed, (
            "Your tests fail against your own mathtools.py:\n" + outcome.output
        )

    @pytest.mark.parametrize("fault", list(BROKEN))
    def test_they_catch_a_broken_version(self, load, run_tests_against, fault):
        load("mathtools.py").clamp
        outcome = run_tests_against("test_mine.py", {"mathtools.py": BROKEN[fault]})
        assert not outcome.no_tests, "pytest found no tests in test_mine.py."
        assert not outcome.passed, (
            f"Your tests all passed against a mathtools.py where {fault}. "
            "A test that passes against broken code is not testing that code. "
            "Which input would have exposed it?"
        )
