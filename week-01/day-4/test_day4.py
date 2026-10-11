"""Week 1, Day 4 - five broken programs.

Run me:  pytest week-01/day-4 -v
"""

from pathlib import Path


def test_broken_1(run):
    assert run("broken_1.py").line(0) == "Steps left: 5"


def test_broken_2(run):
    assert run("broken_2.py").line(0) == "You sent 3 messages."


def test_broken_3(run):
    run("broken_3.py", answers=["4"]).expect("Next turn: 5")
    run("broken_3.py", answers=["41"]).expect("Next turn: 42")


def test_broken_4_stops(run):
    r = run("broken_4.py", timeout=4)
    assert r.lines == ["step 0", "step 1", "step 2"]


def test_broken_5_stops_at_the_limit(run):
    assert run("broken_5.py").line(0) == "Stop", (
        "With 10 steps used and a limit of 10, the agent must stop. No error told "
        "you about this one - you had to know what the answer should be."
    )


def test_broken_5_still_allows_nine(run_variant):
    r = run_variant("broken_5.py", {"used = 10": "used = 9"})
    assert r.line(0) == "Keep going", "9 of 10 steps used should keep going."


def test_notes_are_filled_in():
    notes = (Path(__file__).parent / "NOTES.md").read_text()
    left = notes.count("_(your answer)_")
    assert left == 0, (
        f"NOTES.md still has {left} unanswered row(s). The notes are the part of "
        "today that Friday's defence is about."
    )
