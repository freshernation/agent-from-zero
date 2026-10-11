"""Week 4 milestone - a chat assistant with memory and a meter.

Run me:  pytest week-04/milestone -v
"""

import pytest

from llm import FakeModel, ModelError, say


@pytest.fixture
def module(load):
    return load("assistant.py")


@pytest.fixture
def session(module):
    return module.new_session("You are Desk.")


def test_new_session(module):
    assert module.new_session("You are Desk.") == {
        "system": "You are Desk.",
        "history": [],
        "usage": {"input": 0, "output": 0},
    }


def test_sessions_do_not_share_state(module):
    first = module.new_session("a")
    second = module.new_session("b")
    first["history"].append("x")
    first["usage"]["input"] = 99
    assert second["history"] == [] and second["usage"]["input"] == 0


class TestTalking:
    def test_returns_the_models_text(self, module, session):
        assert module.handle(FakeModel([say("Hello!")]), session, "hi") == "Hello!"

    def test_sends_the_system_prompt(self, module, session):
        model = FakeModel([say("Hello!")])
        module.handle(model, session, "hi")
        assert model.requests[0]["system"] == "You are Desk."

    def test_remembers(self, module, session):
        model = FakeModel([say("Hello, Sam."), say("Sam.")])
        module.handle(model, session, "My name is Sam.")
        module.handle(model, session, "What is my name?")
        assert len(model.requests[1]["messages"]) == 3
        assert len(session["history"]) == 4

    def test_counts_tokens(self, module, session):
        model = FakeModel([say("a", input=10, output=5), say("b", input=30, output=7)])
        module.handle(model, session, "one")
        module.handle(model, session, "two")
        assert session["usage"] == {"input": 40, "output": 12}

    def test_marks_a_cut_off_reply(self, module, session):
        model = FakeModel([say("Lima is the", stop="length")])
        assert module.handle(model, session, "Tell me about Lima") == (
            "Lima is the [cut off]"
        )

    def test_empty_line_does_not_reach_the_model(self, module, session):
        model = FakeModel([])
        assert module.handle(model, session, "   ") == "Say something."
        assert model.call_count == 0


class TestWhenTheModelFails:
    def test_reports_it(self, module, session):
        model = FakeModel([ModelError("rate limited")])
        assert module.handle(model, session, "hi") == (
            "The model is unavailable: rate limited"
        )

    def test_the_conversation_survives(self, module, session):
        model = FakeModel([say("Hello."), ModelError("down"), say("Back.")])
        module.handle(model, session, "hi")
        module.handle(model, session, "still there?")
        assert len(session["history"]) == 2
        assert module.handle(model, session, "still there?") == "Back."


class TestCommands:
    def test_turns(self, module, session):
        model = FakeModel([say("a"), say("b")])
        module.handle(model, session, "one")
        module.handle(model, session, "two")
        assert module.handle(model, session, "/turns") == "2 turns so far."

    def test_cost(self, module, session):
        session["usage"] = {"input": 40, "output": 12}
        expected = 40 / 1_000_000 * module.PRICE_IN + 12 / 1_000_000 * module.PRICE_OUT
        assert module.handle(FakeModel([]), session, "/cost") == (
            f"Tokens: 40 in, 12 out. Cost: ${expected:.4f}"
        )

    def test_cost_before_anything(self, module, session):
        assert module.handle(FakeModel([]), session, "/cost") == (
            "Tokens: 0 in, 0 out. Cost: $0.0000"
        )

    def test_reset_clears_history_but_keeps_usage(self, module, session):
        model = FakeModel([say("Hello.", input=10, output=5)])
        module.handle(model, session, "hi")
        assert module.handle(model, session, "/reset") == "Conversation cleared."
        assert session["history"] == []
        assert session["usage"] == {"input": 10, "output": 5}, (
            "/reset forgets the conversation. It does not refund the money."
        )

    @pytest.mark.parametrize("line", ["/TURNS", "  /turns  ", "/Turns"])
    def test_commands_in_any_capitals(self, module, session, line):
        assert module.handle(FakeModel([]), session, line) == "0 turns so far."

    def test_commands_do_not_reach_the_model(self, module, session):
        model = FakeModel([])
        for line in ["/turns", "/cost", "/reset"]:
            module.handle(model, session, line)
        assert model.call_count == 0

    def test_handle_does_not_print(self, module, session, capsys):
        module.handle(FakeModel([say("x")]), session, "hi")
        assert capsys.readouterr().out == ""


class TestTheProgram:
    def test_a_session_on_the_fake_provider(self, run):
        r = run("assistant.py", answers=["hello", "/turns", "quit"])
        r.expect("Desk: (fake model) You said: hello")
        r.expect("Desk: 1 turns so far.")
        r.expect("Tokens: 10 in, 20 out.")
        r.expect("Bye.")

    def test_importing_does_not_start_it(self, load, capsys):
        load("assistant.py").handle
        assert capsys.readouterr().out == ""
