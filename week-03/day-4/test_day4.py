"""Week 3, Day 4 - files, JSON, and excepts that are too wide or too narrow.

Run me:  pytest week-03/day-4 -v
"""

import json
from pathlib import Path

import pytest

NOTES = [{"title": "milk", "body": "two litres"}]


def test_broken_1(load, tmp_path):
    path = tmp_path / "notes.json"
    path.write_text(json.dumps(NOTES))
    assert load("broken_1.py").read_notes(path) == NOTES


def test_broken_2_converts(load):
    assert load("broken_2.py").to_number("4.5") == 4.5


def test_broken_2_still_handles_nonsense(load):
    assert load("broken_2.py").to_number("abc") == 0


def test_broken_2_names_its_error(load, source):
    load("broken_2.py").to_number
    code = source("broken_2.py", code_only=True)
    assert "except:" not in code.replace(" ", ""), (
        "The bare `except:` is what hid the typo from you. Name the error."
    )


def test_broken_3(load, tmp_path):
    path = tmp_path / "notes.json"
    load("broken_3.py").write_notes(path, NOTES)
    try:
        saved = json.loads(path.read_text())
    except json.JSONDecodeError:
        pytest.fail(
            "The file was written, but it is not JSON. Open it and look:\n  "
            + path.read_text()
        )
    assert saved == NOTES


def test_broken_4_averages(load):
    assert load("broken_4.py").average_tool("2, 4") == "3.0"


@pytest.mark.parametrize("text", ["1, x", "", "one two"])
def test_broken_4_never_raises(load, text):
    assert load("broken_4.py").average_tool(text) == "Error: not a number"


def test_notes_are_filled_in():
    notes = (Path(__file__).parent / "NOTES.md").read_text()
    left = notes.count("_(your answer)_")
    assert left == 0, f"NOTES.md still has {left} unanswered row(s)."
