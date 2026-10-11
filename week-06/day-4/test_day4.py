"""Week 6, Day 4 - four broken agents.

Run me:  pytest week-06/day-4 -v
"""

from pathlib import Path

import pytest

from llm import FakeModel, say, use, use_many


@pytest.fixture
def kit(load):
    return load("kit.py")


@pytest.mark.parametrize("name", ["broken_1.py", "broken_2.py", "broken_3.py", "broken_4.py"])
def test_each_still_answers_a_plain_question(load, kit, name):
    result = load(name).run_agent(FakeModel([say("Paris.")]), "Capital?", kit.SCHEMAS, kit.TOOLS)
    assert result["answer"] == "Paris."
    assert result["stopped"] == "done"
    assert result["steps"] == 1


def test_broken_1_one_tool(load, kit):
    model = FakeModel([use("calculate", {"expression": "17 * 23"}), say("391.")])
    result = load("broken_1.py").run_agent(model, "17 * 23?", kit.SCHEMAS, kit.TOOLS)
    assert result["answer"] == "391."
    assert result["steps"] == 2


def test_broken_2_obeys_the_cap(load, kit):
    script = [use("calculate", {"expression": f"{n} + 1"}, id=f"c{n}") for n in range(15)]
    model = FakeModel(script)
    result = load("broken_2.py").run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS, max_steps=5)
    assert model.call_count == 5
    assert result["stopped"] == "max_steps"
    assert result["steps"] == 5


def test_broken_2_counts_steps_correctly(load, kit):
    model = FakeModel([use("list_titles"), say("None.")])
    result = load("broken_2.py").run_agent(model, "Notes?", kit.SCHEMAS, kit.TOOLS)
    assert result["steps"] == 2


def test_broken_3_two_tools_at_once(load, kit):
    model = FakeModel([
        use_many([("add_note", {"title": "milk"}), ("add_note", {"title": "eggs"})]),
        use("list_titles", id="c3"),
        say("Milk and eggs."),
    ])
    result = load("broken_3.py").run_agent(model, "Add both.", kit.SCHEMAS, kit.TOOLS)
    assert result["answer"] == "Milk and eggs."
    assert model.requests[2]["messages"][-1]["content"] == "1. milk\n2. eggs", (
        "Both tools should have run."
    )


def test_broken_4_stops_early(load, kit):
    model = FakeModel([use("list_titles", id=f"c{n}") for n in range(15)])
    result = load("broken_4.py").run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS)
    assert result["stopped"] == "repeating", (
        f"The run ended with {result['stopped']!r}. The cap saved it - but the "
        "repeat check never fired, and nothing crashed to tell you."
    )
    assert model.call_count == 3, (
        f"The model was called {model.call_count} times for a run that should "
        "have ended after 3. A correct answer is not evidence of a correct agent."
    )


def test_notes_are_filled_in():
    notes = (Path(__file__).parent / "NOTES.md").read_text()
    left = notes.count("_(your answer)_")
    assert left == 0, f"NOTES.md still has {left} unanswered row(s)."
