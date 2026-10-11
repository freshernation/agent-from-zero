"""Week 6, Day 2 - traces and cost.

Run me:  pytest week-06/day-2 -v
"""

import pytest

from llm import FakeModel, say, use, use_many


@pytest.fixture
def run_agent(load):
    return load("agent.py").run_agent


@pytest.fixture
def kit(load):
    return load("kit.py")


class TestStillAnAgent:
    def test_yesterdays_behaviour(self, run_agent, kit):
        model = FakeModel([use("calculate", {"expression": "2 + 2"}), say("4.")])
        result = run_agent(model, "2 + 2?", kit.SCHEMAS, kit.TOOLS)
        assert result["answer"] == "4."
        assert result["stopped"] == "done"
        assert result["steps"] == 2


class TestUsage:
    def test_sums_every_call(self, run_agent, kit):
        model = FakeModel([
            use("list_titles", input=100, output=10),
            use("list_titles", id="call_2", input=200, output=10),
            say("Done.", input=300, output=40),
        ])
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS)
        assert result["usage"] == {"input": 600, "output": 60}

    def test_reported_when_the_cap_hits(self, run_agent, kit):
        model = FakeModel([use("list_titles", id=f"c{n}", input=10, output=5)
                           for n in range(9)])
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS, max_steps=3)
        assert result["usage"] == {"input": 30, "output": 15}


class TestTrace:
    def test_a_one_step_answer(self, run_agent, kit):
        result = run_agent(FakeModel([say("Paris.")]), "Capital?", kit.SCHEMAS, kit.TOOLS)
        assert result["trace"] == [{"step": 1, "kind": "answer", "text": "Paris."}]

    def test_a_tool_step(self, run_agent, kit):
        model = FakeModel([use("calculate", {"expression": "17 * 23"}), say("391.")])
        result = run_agent(model, "17 * 23?", kit.SCHEMAS, kit.TOOLS)
        assert result["trace"] == [
            {"step": 1, "kind": "call", "name": "calculate",
             "args": {"expression": "17 * 23"}},
            {"step": 1, "kind": "result", "name": "calculate", "content": "391"},
            {"step": 2, "kind": "answer", "text": "391."},
        ]

    def test_text_alongside_a_call_is_recorded(self, run_agent, kit):
        model = FakeModel([use("list_titles", text="Let me look."), say("None.")])
        trace = run_agent(model, "Notes?", kit.SCHEMAS, kit.TOOLS)["trace"]
        assert trace[0] == {"step": 1, "kind": "say", "text": "Let me look."}
        assert trace[1]["kind"] == "call"

    def test_no_say_event_when_there_is_no_text(self, run_agent, kit):
        model = FakeModel([use("list_titles"), say("None.")])
        trace = run_agent(model, "Notes?", kit.SCHEMAS, kit.TOOLS)["trace"]
        assert [event["kind"] for event in trace] == ["call", "result", "answer"]

    def test_several_calls_then_their_results(self, run_agent, kit):
        model = FakeModel([
            use_many([("add_note", {"title": "milk"}),
                      ("calculate", {"expression": "1 + 1"})]),
            say("Done."),
        ])
        trace = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS)["trace"]
        assert [(event["kind"], event.get("name")) for event in trace] == [
            ("call", "add_note"), ("call", "calculate"),
            ("result", "add_note"), ("result", "calculate"),
            ("answer", None),
        ]
        assert trace[3]["content"] == "2", "Each result belongs with its own call."

    def test_the_cap_leaves_a_stop_event(self, run_agent, kit):
        model = FakeModel([use("list_titles", id=f"c{n}") for n in range(9)])
        trace = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS, max_steps=2)["trace"]
        assert trace[-1] == {"step": 2, "kind": "stop", "reason": "max_steps"}


class TestShow:
    @pytest.mark.parametrize("event,line", [
        ({"step": 2, "kind": "say", "text": "Now the yearly figure."},
         "[2] say: Now the yearly figure."),
        ({"step": 2, "kind": "call", "name": "calculate",
          "args": {"expression": "1450 * 12"}},
         '[2] call calculate({"expression": "1450 * 12"})'),
        ({"step": 1, "kind": "call", "name": "list_titles", "args": {}},
         "[1] call list_titles({})"),
        ({"step": 2, "kind": "result", "name": "calculate", "content": "17400"},
         "[2] result calculate: 17400"),
        ({"step": 3, "kind": "answer", "text": "That is 17400 a year."},
         "[3] answer: That is 17400 a year."),
        ({"step": 4, "kind": "stop", "reason": "max_steps"}, "[4] stop: max_steps"),
    ])
    def test_format_event(self, load, event, line):
        assert load("show.py").format_event(event) == line

    def test_format_trace(self, load):
        trace = [
            {"step": 1, "kind": "call", "name": "list_titles", "args": {}},
            {"step": 1, "kind": "result", "name": "list_titles", "content": "No notes yet."},
            {"step": 2, "kind": "answer", "text": "You have none."},
        ]
        assert load("show.py").format_trace(trace) == (
            "[1] call list_titles({})\n"
            "[1] result list_titles: No notes yet.\n"
            "[2] answer: You have none."
        )

    def test_format_empty_trace(self, load):
        assert load("show.py").format_trace([]) == ""

    def test_summary(self, load):
        result = {"stopped": "done", "steps": 3, "usage": {"input": 300, "output": 60}}
        assert load("show.py").summary(result) == "done in 3 steps (300 tokens in, 60 out)"

    def test_summary_of_a_stopped_run(self, load):
        result = {"stopped": "max_steps", "steps": 10, "usage": {"input": 9, "output": 1}}
        assert load("show.py").summary(result) == (
            "max_steps in 10 steps (9 tokens in, 1 out)"
        )
