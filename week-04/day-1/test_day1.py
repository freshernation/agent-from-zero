"""Week 4, Day 1 - one call, a system prompt, and reading the reply.

Run me:  pytest week-04/day-1 -v
"""

from llm import FakeModel, say


class TestAsk:
    def test_returns_the_text(self, load):
        model = FakeModel([say("Lima.")])
        assert load("ask.py").ask(model, "Capital of Peru?") == "Lima."

    def test_sends_one_user_message(self, load):
        model = FakeModel([say("Lima.")])
        load("ask.py").ask(model, "Capital of Peru?")
        assert model.requests[0]["messages"] == [
            {"role": "user", "content": "Capital of Peru?"},
        ]

    def test_calls_the_model_once(self, load):
        model = FakeModel([say("Lima.")])
        load("ask.py").ask(model, "Capital of Peru?")
        assert model.call_count == 1

    def test_uses_the_model_it_was_given(self, load, source):
        load("ask.py").ask
        assert "connect(" not in source("ask.py", code_only=True), (
            "ask.py calls connect(). Use the model that was passed in - that is "
            "what makes these functions testable."
        )


class TestAskAs:
    def test_passes_the_system_prompt(self, load):
        model = FakeModel([say("Lima")])
        result = load("ask.py").ask_as(model, "Answer in one word.", "Capital of Peru?")
        assert result == "Lima"
        assert model.requests[0]["system"] == "Answer in one word."

    def test_system_is_not_in_the_list(self, load):
        model = FakeModel([say("Lima")])
        load("ask.py").ask_as(model, "Answer in one word.", "Capital of Peru?")
        assert model.requests[0]["messages"] == [
            {"role": "user", "content": "Capital of Peru?"},
        ], "The system prompt is a separate argument, not a message."


class TestDescribe:
    def test_done(self, load):
        reply = say("Lima.", input=14, output=3)
        assert load("ask.py").describe(reply) == "done: 14 tokens in, 3 out"

    def test_cut_off(self, load):
        reply = say("Lima is", stop="length", input=14, output=100)
        assert load("ask.py").describe(reply) == "length: 14 tokens in, 100 out"


class TestShortAnswer:
    def test_returns_the_text(self, load):
        model = FakeModel([say("Lima.")])
        assert load("ask.py").short_answer(model, "Capital of Peru?") == "Lima."

    def test_sends_a_real_system_prompt(self, load):
        model = FakeModel([say("Lima.")])
        load("ask.py").short_answer(model, "Capital of Peru?")
        system = model.requests[0]["system"]
        assert isinstance(system, str) and len(system.split()) >= 5, (
            f"The system prompt was {system!r}. Write a real instruction that "
            "keeps answers to ten words or fewer."
        )
