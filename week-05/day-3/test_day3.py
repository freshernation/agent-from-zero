"""Week 5, Day 3 - ask, run, answer.

Run me:  pytest week-05/day-3 -v
"""

import json

import pytest

from llm import FakeModel, say, use, use_many


@pytest.fixture
def module(load):
    return load("round_trip.py")


@pytest.fixture
def schemas(load):
    return load("schemas.py").SCHEMAS


class TestNoToolNeeded:
    def test_returns_the_answer(self, module, schemas):
        model = FakeModel([say("Paris.")])
        assert module.answer(model, schemas, "Capital of France?") == "Paris."
        assert model.call_count == 1

    def test_still_offers_the_tools(self, module, schemas):
        model = FakeModel([say("Paris.")])
        module.answer(model, schemas, "Capital of France?")
        assert model.requests[0]["tools"] == schemas


class TestOneTool:
    def test_returns_the_final_answer(self, module, schemas):
        model = FakeModel([
            use("calculate", {"expression": "17 * 23"}),
            say("17 times 23 is 391."),
        ])
        assert module.answer(model, schemas, "What is 17 times 23?") == (
            "17 times 23 is 391."
        )
        assert model.call_count == 2

    def test_the_second_call_carries_the_whole_exchange(self, module, schemas):
        model = FakeModel([
            use("calculate", {"expression": "17 * 23"}, id="call_9"),
            say("391."),
        ])
        module.answer(model, schemas, "What is 17 times 23?")
        sent = model.requests[1]["messages"]
        assert [message["role"] for message in sent] == ["user", "assistant", "tool"]
        assert sent[1]["tool_calls"][0]["name"] == "calculate"
        assert sent[2] == {"role": "tool", "tool_call_id": "call_9", "content": "391"}

    def test_the_tool_really_ran(self, module, schemas, notes_file):
        model = FakeModel([
            use("add_note", {"title": "dentist", "body": "Friday 3pm"}),
            say("Saved."),
        ])
        module.answer(model, schemas, "Remember the dentist on Friday at 3pm")
        assert json.loads(notes_file.read_text()) == [
            {"title": "dentist", "body": "Friday 3pm"},
        ], "The model asked for add_note, but nothing was saved. YOU run the tool."

    def test_tools_are_offered_both_times(self, module, schemas):
        model = FakeModel([use("list_titles"), say("None.")])
        module.answer(model, schemas, "What notes do I have?")
        assert model.requests[1]["tools"] == schemas

    def test_system_prompt_goes_on_both_calls(self, module, schemas):
        model = FakeModel([use("list_titles"), say("None.")])
        module.answer(model, schemas, "What notes do I have?", system="You are Desk.")
        assert [request["system"] for request in model.requests] == ["You are Desk."] * 2


class TestSeveralTools:
    def test_every_call_gets_its_own_result(self, module, schemas):
        model = FakeModel([
            use_many([
                ("add_note", {"title": "milk"}),
                ("add_note", {"title": "eggs"}),
                ("calculate", {"expression": "2 + 2"}),
            ]),
            say("Done."),
        ])
        assert module.answer(model, schemas, "Add milk and eggs, and what is 2+2?") == "Done."
        results = model.requests[1]["messages"][2:]
        assert [message["tool_call_id"] for message in results] == [
            "call_1", "call_2", "call_3",
        ]
        assert results[2]["content"] == "4"


class TestWhenItGoesWrong:
    def test_an_invented_tool_is_reported_to_the_model(self, module, schemas):
        model = FakeModel([use("send_email", {"to": "sam"}), say("I cannot do that.")])
        assert module.answer(model, schemas, "Email Sam") == "I cannot do that."
        result = model.requests[1]["messages"][2]
        assert result["content"] == "Error: unknown tool 'send_email'"

    def test_a_second_request_for_tools_ends_it(self, module, schemas):
        model = FakeModel([use("list_titles"), use("find_notes", {"word": "milk"})])
        assert module.answer(model, schemas, "Anything about milk?") == (
            "I could not finish that in one step."
        )
        assert model.call_count == 2, "One round of tools only. The loop is next week."
