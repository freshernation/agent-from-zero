"""Week 4, Day 3 - cost, cut-offs, structured output.

Run me:  pytest week-04/day-3 -v
"""

import pytest

from llm import FakeModel, say

GOOD = '{"title": "milk", "body": "two litres"}'
NOTE = {"title": "milk", "body": "two litres"}


class TestMeter:
    def test_cost(self, load):
        usage = {"input": 1200, "output": 300}
        assert load("meter.py").cost(usage, 4.00, 20.00) == pytest.approx(0.0108)

    def test_cost_of_nothing(self, load):
        assert load("meter.py").cost({"input": 0, "output": 0}, 4.00, 20.00) == 0

    def test_output_is_priced_separately(self, load):
        module = load("meter.py")
        cheap = module.cost({"input": 1000, "output": 0}, 1.00, 10.00)
        dear = module.cost({"input": 0, "output": 1000}, 1.00, 10.00)
        assert dear == pytest.approx(cheap * 10)

    def test_total_usage(self, load):
        replies = [say("a", input=10, output=5), say("b", input=30, output=7)]
        assert load("meter.py").total_usage(replies) == {"input": 40, "output": 12}

    def test_total_of_nothing(self, load):
        assert load("meter.py").total_usage([]) == {"input": 0, "output": 0}

    def test_was_cut_off(self, load):
        module = load("meter.py")
        assert module.was_cut_off(say("Lima is", stop="length")) is True
        assert module.was_cut_off(say("Lima.")) is False


class TestParseJson:
    @pytest.mark.parametrize("text", [
        GOOD,
        "Sure! Here is the note:\n" + GOOD,
        "```json\n" + GOOD + "\n```",
        GOOD + "\nLet me know if you need anything else.",
        "  " + GOOD + "  ",
    ])
    def test_finds_the_object(self, load, text):
        assert load("extract.py").parse_json(text) == NOTE

    @pytest.mark.parametrize("text", [
        "I'm not sure what you mean.", "", "{not json at all}", "} backwards {",
    ])
    def test_gives_none_when_there_is_no_json(self, load, text):
        assert load("extract.py").parse_json(text) is None

    def test_a_list_is_not_an_object(self, load):
        assert load("extract.py").parse_json('["milk", "eggs"]') is None


class TestIsNote:
    @pytest.mark.parametrize("data,answer", [
        (NOTE, True),
        ({"title": "milk", "body": ""}, True),
        ({"title": "milk"}, False),
        ({"title": "", "body": "x"}, False),
        ({"title": 3, "body": "x"}, False),
        ({"title": "milk", "body": None}, False),
        (None, False),
        (["title", "body"], False),
    ])
    def test_is_note(self, load, data, answer):
        assert load("extract.py").is_note(data) is answer


class TestExtractNote:
    def test_good_first_time(self, load):
        model = FakeModel([say(GOOD)])
        assert load("extract.py").extract_note(model, "buy two litres of milk") == NOTE
        assert model.call_count == 1

    def test_sends_instructions_and_the_sentence(self, load):
        model = FakeModel([say(GOOD)])
        load("extract.py").extract_note(model, "buy two litres of milk")
        request = model.requests[0]
        assert "json" in (request["system"] or "").lower(), (
            "Ask for JSON in the system prompt."
        )
        assert request["messages"] == [
            {"role": "user", "content": "buy two litres of milk"},
        ]

    def test_wrapped_in_chat_still_counts(self, load):
        model = FakeModel([say("Of course!\n" + GOOD)])
        assert load("extract.py").extract_note(model, "x") == NOTE
        assert model.call_count == 1, "That answer was usable. Do not retry it."

    def test_retries_once_after_a_bad_answer(self, load):
        model = FakeModel([say("I'm not sure what you mean."), say(GOOD)])
        assert load("extract.py").extract_note(model, "x") == NOTE
        assert model.call_count == 2

    def test_the_retry_shows_the_model_its_own_answer(self, load):
        model = FakeModel([say('{"title": "milk"}'), say(GOOD)])
        load("extract.py").extract_note(model, "x")
        sent = model.requests[1]["messages"]
        assert [message["role"] for message in sent] == ["user", "assistant", "user"], (
            "Retry in the SAME conversation: the sentence, the model's bad "
            "answer, then your message saying what was wrong."
        )
        assert sent[1]["content"] == '{"title": "milk"}'
        assert len(sent[2]["content"].split()) >= 4, (
            "Tell the model what was wrong with its answer."
        )

    def test_gives_up_after_two_tries(self, load):
        model = FakeModel([say("no"), say("still no")])
        assert load("extract.py").extract_note(model, "x") is None
        assert model.call_count == 2

    def test_a_missing_key_is_a_bad_answer(self, load):
        model = FakeModel([say('{"title": "milk"}'), say('{"body": "x"}')])
        assert load("extract.py").extract_note(model, "x") is None
