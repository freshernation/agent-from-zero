"""Week 4, Day 2 - conversation memory.

Run me:  pytest week-04/day-2 -v
"""

import pytest

from llm import FakeModel, ModelError, say


class TestSend:
    def test_returns_the_text(self, load):
        model = FakeModel([say("Hello, Sam.")])
        assert load("chat.py").send(model, [], "My name is Sam.") == "Hello, Sam."

    def test_history_grows_by_two(self, load):
        history = []
        load("chat.py").send(FakeModel([say("Hello, Sam.")]), history, "My name is Sam.")
        assert history == [
            {"role": "user", "content": "My name is Sam."},
            {"role": "assistant", "content": "Hello, Sam."},
        ]

    def test_second_turn_resends_everything(self, load):
        model = FakeModel([say("Hello, Sam."), say("Sam.")])
        history = []
        module = load("chat.py")
        module.send(model, history, "My name is Sam.")
        module.send(model, history, "What is my name?")
        sent = model.requests[1]["messages"]
        assert len(sent) == 3, (
            f"The second call sent {len(sent)} message(s). The model has no "
            "memory - it must be sent the whole conversation every time."
        )
        assert [message["role"] for message in sent] == ["user", "assistant", "user"]

    def test_appends_the_models_own_message(self, load):
        reply = say("Hello.")
        reply["message"]["_raw"] = "the provider's own copy"
        history = []
        load("chat.py").send(FakeModel([reply]), history, "Hi")
        assert history[-1].get("_raw") == "the provider's own copy", (
            "Append reply[\"message\"] itself. Do not build a new dict from "
            "reply[\"text\"] - the provider may have attached things it needs back."
        )

    def test_passes_the_system_prompt_every_time(self, load):
        model = FakeModel([say("a"), say("b")])
        history = []
        module = load("chat.py")
        module.send(model, history, "one", system="Be brief.")
        module.send(model, history, "two", system="Be brief.")
        assert [request["system"] for request in model.requests] == ["Be brief."] * 2

    def test_no_system_by_default(self, load):
        model = FakeModel([say("a")])
        load("chat.py").send(model, [], "one")
        assert model.requests[0]["system"] is None


class TestSendWhenTheModelFails:
    def test_the_error_is_passed_on(self, load):
        model = FakeModel([ModelError("down")])
        with pytest.raises(ModelError):
            load("chat.py").send(model, [], "Hi")

    def test_history_is_left_as_it_was(self, load):
        model = FakeModel([say("Hello."), ModelError("down"), say("Still here.")])
        history = []
        module = load("chat.py")
        module.send(model, history, "Hi")
        with pytest.raises(ModelError):
            module.send(model, history, "Are you there?")
        assert len(history) == 2, (
            "After a failed call the history still holds the message that never "
            "got an answer. Remove it before passing the error on."
        )
        assert module.send(model, history, "Are you there?") == "Still here."


class TestHelpers:
    def test_turns(self, load):
        history = [
            {"role": "user", "content": "a"}, {"role": "assistant", "content": "b"},
            {"role": "user", "content": "c"}, {"role": "assistant", "content": "d"},
        ]
        assert load("chat.py").turns(history) == 2
        assert load("chat.py").turns([]) == 0

    def test_reset_empties_the_same_list(self, load):
        history = [{"role": "user", "content": "a"}]
        assert load("chat.py").reset(history) is None
        assert history == [], (
            "reset() should empty the list it was given. `history = []` inside "
            "the function only re-points a local name."
        )
