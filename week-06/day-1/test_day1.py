"""Week 6, Day 1 - the agent loop.

Run me:  pytest week-06/day-1 -v
"""

import json

import pytest

from llm import FakeModel, say, use, use_many


@pytest.fixture
def run_agent(load):
    return load("agent.py").run_agent


@pytest.fixture
def kit(load):
    return load("kit.py")


def roles(messages):
    return [message["role"] for message in messages]


class TestNoTools:
    def test_answers_in_one_step(self, run_agent, kit):
        model = FakeModel([say("Paris.")])
        result = run_agent(model, "Capital of France?", kit.SCHEMAS, kit.TOOLS)
        assert result["answer"] == "Paris."
        assert result["stopped"] == "done"
        assert result["steps"] == 1
        assert roles(result["messages"]) == ["user", "assistant"]

    def test_sends_system_and_tools(self, run_agent, kit):
        model = FakeModel([say("Paris.")])
        run_agent(model, "Capital of France?", kit.SCHEMAS, kit.TOOLS, system="You are Desk.")
        assert model.requests[0]["system"] == "You are Desk."
        assert model.requests[0]["tools"] == kit.SCHEMAS


class TestManySteps:
    def test_three_steps(self, run_agent, kit, notes_file):
        model = FakeModel([
            use("add_note", {"title": "rent", "body": "1450 a month"}),
            use("calculate", {"expression": "1450 * 12"}),
            say("Saved. That is 17400 a year."),
        ])
        result = run_agent(model, "Save the rent and work out the year.", kit.SCHEMAS, kit.TOOLS)
        assert result["answer"] == "Saved. That is 17400 a year."
        assert result["steps"] == 3, "A step is one call to the model."
        assert result["stopped"] == "done"
        assert json.loads(notes_file.read_text())[0]["title"] == "rent"

    def test_the_list_grows_in_the_right_order(self, run_agent, kit):
        model = FakeModel([
            use("list_titles"), use("calculate", {"expression": "2 + 2"}), say("Done."),
        ])
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS)
        assert roles(result["messages"]) == [
            "user", "assistant", "tool", "assistant", "tool", "assistant",
        ]

    def test_every_call_sends_the_whole_history(self, run_agent, kit):
        model = FakeModel([use("list_titles"), use("list_titles", id="call_2"), say("Done.")])
        run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS)
        assert [len(request["messages"]) for request in model.requests] == [1, 3, 5]

    def test_several_tools_in_one_step(self, run_agent, kit):
        model = FakeModel([
            use_many([("add_note", {"title": "milk"}), ("add_note", {"title": "eggs"})]),
            say("Both saved."),
        ])
        result = run_agent(model, "Add milk and eggs.", kit.SCHEMAS, kit.TOOLS)
        assert result["steps"] == 2
        assert roles(result["messages"]) == ["user", "assistant", "tool", "tool", "assistant"]

    def test_uses_the_tools_it_was_given(self, run_agent, kit):
        def shout(text):
            return text.upper()

        model = FakeModel([use("shout", {"text": "hi"}), say("HI")])
        result = run_agent(model, "Shout hi.", [], {"shout": shout})
        assert result["messages"][2]["content"] == "HI", (
            "Use the `tools` argument, not kit.TOOLS - the agent must work with "
            "any dispatch table it is handed."
        )


class TestTheCap:
    def test_stops_at_max_steps(self, run_agent, kit):
        model = FakeModel([use("list_titles", id=f"call_{n}") for n in range(20)])
        result = run_agent(model, "Loop forever.", kit.SCHEMAS, kit.TOOLS, max_steps=4)
        assert model.call_count == 4, (
            f"With max_steps=4 the model was called {model.call_count} times."
        )
        assert result["stopped"] == "max_steps"
        assert result["steps"] == 4
        assert result["answer"] == "I ran out of steps before finishing."

    def test_default_cap_is_ten(self, run_agent, kit):
        model = FakeModel([use("list_titles", id=f"call_{n}") for n in range(30)])
        run_agent(model, "Loop forever.", kit.SCHEMAS, kit.TOOLS)
        assert model.call_count == 10

    def test_finishing_on_the_last_allowed_step_is_done(self, run_agent, kit):
        model = FakeModel([use("list_titles"), say("Finished.")])
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS, max_steps=2)
        assert result["stopped"] == "done"
        assert result["answer"] == "Finished."

    def test_a_cap_of_one(self, run_agent, kit):
        model = FakeModel([use("list_titles"), say("never reached")])
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS, max_steps=1)
        assert model.call_count == 1
        assert result["stopped"] == "max_steps"
