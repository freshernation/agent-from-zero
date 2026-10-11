"""Week 2, Day 4 - five functions that are wrong.

Run me:  pytest week-02/day-4 -v
"""

from pathlib import Path

import pytest


@pytest.fixture
def history():
    return [
        {"role": "user", "content": "Remember to buy milk"},
        {"role": "assistant", "content": "Saved."},
        {"role": "user", "content": "Thanks"},
    ]


def test_broken_1(load):
    assert load("broken_1.py").label("user", "hi") == "user: hi"


def test_broken_2(load, history):
    assert load("broken_2.py").first_words(history) == ["Remember", "Saved.", "Thanks"]


def test_broken_3(load, history):
    assert load("broken_3.py").contents(history) == [
        "Remember to buy milk", "Saved.", "Thanks",
    ]


def test_broken_4_returns_the_longer_list(load, history):
    extra = {"role": "assistant", "content": "Any time."}
    result = load("broken_4.py").with_message(history, extra)
    assert len(result) == 4 and result[-1] == extra


def test_broken_4_leaves_the_original_alone(load, history):
    load("broken_4.py").with_message(history, {"role": "assistant", "content": "x"})
    assert len(history) == 3, (
        "The caller's history grew. `extended = history` does not copy anything - "
        "it is a second name for the same list."
    )


def test_broken_5(load, history):
    assert load("broken_5.py").count_user(history) == 2


def test_notes_are_filled_in():
    notes = (Path(__file__).parent / "NOTES.md").read_text()
    left = notes.count("_(your answer)_")
    assert left == 0, f"NOTES.md still has {left} unanswered row(s)."
