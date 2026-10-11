"""Week 5 milestone - a chat assistant that can use tools, one step per turn.

Run me:  pytest week-05/milestone -v
"""

import json

import pytest

from llm import FakeModel, ModelError, say, use, use_many


@pytest.fixture
def module(load):
    return load("desk.py")


def roles(history):
    return [message["role"] for message in history]


def test_system_prompt_is_written(module):
    assert isinstance(module.SYSTEM, str) and len(module.SYSTEM.split()) >= 25, (
        "Write a real system prompt: who Desk is, what its tools are for, and a "
        "rule about being careful."
    )


class TestPlainTalk:
    def test_answers(self, module):
        history = []
        assert module.respond(FakeModel([say("Hello!")]), history, "hi") == "Hello!"
        assert roles(history) == ["user", "assistant"]

    def test_sends_system_and_tools(self, module, load):
        model = FakeModel([say("Hello!")])
        module.respond(model, [], "hi")
        assert model.requests[0]["system"] == module.SYSTEM
        assert model.requests[0]["tools"] == load("schemas.py").SCHEMAS


class TestUsingATool:
    def test_runs_it_and_answers(self, module, notes_file):
        model = FakeModel([
            use("add_note", {"title": "passport", "body": "renew by June"}),
            say("Saved."),
        ])
        history = []
        assert module.respond(model, history, "Remember my passport") == "Saved."
        assert json.loads(notes_file.read_text())[0]["title"] == "passport"

    def test_history_holds_the_whole_exchange(self, module):
        model = FakeModel([use("list_titles"), say("You have none.")])
        history = []
        module.respond(model, history, "What notes do I have?")
        assert roles(history) == ["user", "assistant", "tool", "assistant"]
        assert history[2]["content"] == "No notes yet."

    def test_several_calls(self, module):
        model = FakeModel([
            use_many([("add_note", {"title": "milk"}), ("add_note", {"title": "eggs"})]),
            say("Both saved."),
        ])
        history = []
        module.respond(model, history, "Add milk and eggs")
        assert roles(history) == ["user", "assistant", "tool", "tool", "assistant"]

    def test_the_next_turn_still_works(self, module):
        model = FakeModel([
            use("add_note", {"title": "milk"}), say("Saved."),
            use("list_titles"), say("Just milk."),
        ])
        history = []
        module.respond(model, history, "Add milk")
        assert module.respond(model, history, "What do I have?") == "Just milk."
        assert len(model.requests[2]["messages"]) == 5, (
            "The second turn should send the whole first turn - tool messages "
            "included - plus the new question."
        )


class TestTheOneStepLimit:
    def test_says_so(self, module):
        model = FakeModel([use("list_titles"), use("find_notes", {"word": "milk"})])
        assert module.respond(model, [], "Anything about milk?") == (
            "I could not finish that in one step."
        )

    def test_leaves_the_history_usable(self, module):
        model = FakeModel([
            use("list_titles"), use("find_notes", {"word": "milk"}),
            say("Hello again."),
        ])
        history = []
        module.respond(model, history, "Anything about milk?")
        assert module.respond(model, history, "hello") == "Hello again.", (
            "After giving up, the next turn must still work. Do not append the "
            "model's unfinished turn - its tool calls would never be answered."
        )


class TestWhenTheModelFails:
    def test_reports_it_and_forgets_the_message(self, module):
        history = []
        result = module.respond(FakeModel([ModelError("rate limited")]), history, "hi")
        assert result == "The model is unavailable: rate limited"
        assert history == []

    def test_recovers(self, module):
        model = FakeModel([ModelError("down"), say("Here now.")])
        history = []
        module.respond(model, history, "hi")
        assert module.respond(model, history, "hi") == "Here now."


class TestTheProgram:
    def test_runs_on_the_fake_provider(self, run, tmp_path):
        r = run("desk.py", answers=["hello", "quit"],
                env={"NOTES_FILE": tmp_path / "n.json"})
        r.expect("Desk: (fake model) You said: hello")
        r.expect("Bye.")

    def test_respond_does_not_print(self, module, capsys):
        module.respond(FakeModel([say("x")]), [], "hi")
        assert capsys.readouterr().out == ""
