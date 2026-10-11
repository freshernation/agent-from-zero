"""Week 6 milestone - Project 2.

Run me:  pytest week-06/milestone -v
"""

from pathlib import Path

import pytest

from llm import FakeModel, ModelError, say, use, use_many


@pytest.fixture
def run_agent(load):
    return load("agent.py").run_agent


@pytest.fixture
def kit(load):
    return load("kit.py")


@pytest.fixture
def cli(load):
    return load("cli.py")


class TestTheAgent:
    def test_a_multi_step_task(self, run_agent, kit):
        model = FakeModel([
            use_many([("add_note", {"title": "milk"}), ("add_note", {"title": "eggs"})]),
            use("delete_note", {"title": "eggs"}, id="c3"),
            use("list_titles", id="c4"),
            say("Only milk is left."),
        ])
        result = run_agent(model, "Add milk and eggs, delete eggs, what is left?",
                           kit.SCHEMAS, kit.TOOLS)
        assert result["answer"] == "Only milk is left."
        assert result["stopped"] == "done"
        assert result["steps"] == 4
        assert result["messages"][-2]["content"] == "1. milk"

    def test_has_every_key(self, run_agent, kit):
        result = run_agent(FakeModel([say("Hi.")]), "Hello", kit.SCHEMAS, kit.TOOLS)
        assert set(result) == {"answer", "stopped", "steps", "usage", "trace", "messages"}

    @pytest.mark.parametrize("script,stopped", [
        ([say("Hi.")], "done"),
        ([use("calculate", {"expression": f"{n} + 1"}, id=f"c{n}") for n in range(20)],
         "max_steps"),
        ([use("list_titles", id=f"c{n}") for n in range(20)], "repeating"),
        ([say("Half a", stop="length")], "length"),
        ([say("", stop="refused")], "refused"),
        ([ModelError("down")], "error"),
    ])
    def test_all_six_endings(self, run_agent, kit, script, stopped):
        result = run_agent(FakeModel(script), "Go.", kit.SCHEMAS, kit.TOOLS)
        assert result["stopped"] == stopped

    def test_a_tool_error_is_recovered_from(self, run_agent, kit):
        model = FakeModel([
            use("delete_note", {"title": "car"}),
            say("There is no note about your car."),
        ])
        result = run_agent(model, "Delete the car note.", kit.SCHEMAS, kit.TOOLS)
        assert result["stopped"] == "done"
        assert result["trace"][1]["content"] == "No note called 'car'."


class TestTheCommandLine:
    def test_system_prompt_is_written(self, cli):
        assert isinstance(cli.SYSTEM, str) and len(cli.SYSTEM.split()) >= 30

    def test_answer_and_summary(self, cli, monkeypatch):
        monkeypatch.delenv("AGENT_TRACE", raising=False)
        model = FakeModel([
            use("calculate", {"expression": "1450 * 12"}, input=100, output=10),
            say("That is 17400 a year.", input=200, output=50),
        ])
        assert cli.answer_task(model, "Rent for a year?") == (
            "That is 17400 a year.\n(done in 2 steps (300 tokens in, 60 out))"
        )

    def test_uses_the_system_prompt_and_the_kit(self, cli, kit, monkeypatch):
        monkeypatch.delenv("AGENT_TRACE", raising=False)
        model = FakeModel([say("Hi.")])
        cli.answer_task(model, "Hello")
        assert model.requests[0]["system"] == cli.SYSTEM
        assert model.requests[0]["tools"] == kit.SCHEMAS

    def test_trace_on_request(self, cli, monkeypatch):
        monkeypatch.setenv("AGENT_TRACE", "1")
        model = FakeModel([use("list_titles"), say("None.")])
        assert cli.answer_task(model, "Notes?") == (
            "[1] call list_titles({})\n"
            "[1] result list_titles: No notes yet.\n"
            "[2] answer: None.\n"
            "\n"
            "None.\n"
            "(done in 2 steps (20 tokens in, 40 out))"
        )

    def test_no_trace_otherwise(self, cli, monkeypatch):
        monkeypatch.setenv("AGENT_TRACE", "0")
        model = FakeModel([use("list_titles"), say("None.")])
        assert "[1]" not in cli.answer_task(model, "Notes?")

    def test_the_program(self, run, tmp_path):
        r = run("cli.py", answers=["hello", "quit"],
                env={"NOTES_FILE": tmp_path / "n.json", "AGENT_TRACE": "0"})
        r.expect("(fake model) You said: hello")
        r.expect("(done in 1 steps (10 tokens in, 20 out))")
        r.expect("Bye.")


class TestTheWriteup:
    def test_every_section_is_answered(self):
        text = (Path(__file__).parent / "WRITEUP.md").read_text()
        left = text.count("_(your answer")
        assert left == 0, f"WRITEUP.md still has {left} unanswered section(s)."

    def test_it_is_a_real_explanation(self):
        text = (Path(__file__).parent / "WRITEUP.md").read_text()
        assert len(text.split()) >= 350, (
            f"WRITEUP.md is {len(text.split())} words. Explaining the loop properly "
            "takes at least a page."
        )

    def test_it_includes_a_real_trace(self):
        text = (Path(__file__).parent / "WRITEUP.md").read_text()
        assert "(paste your trace here)" not in text
        assert "] call " in text and "] result " in text, (
            "Paste a real trace - one where the model used at least one tool."
        )
