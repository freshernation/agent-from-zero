"""Week 7, Day 2 - history, trimming, long-term memory.

Run me:  pytest week-07/day-2 -v
"""

import json

import pytest

from llm import FakeModel, say, use
from llm.fake import check_messages


@pytest.fixture
def run_agent(load):
    return load("agent.py").run_agent


@pytest.fixture
def kit(load):
    return load("kit.py")


@pytest.fixture
def memory(load):
    return load("memory.py")


def user(text):
    return {"role": "user", "content": text}


def assistant(text, calls=None, raw=False):
    message = {"role": "assistant", "content": text}
    if calls:
        message["tool_calls"] = [{"id": c, "name": "list_titles", "args": {}} for c in calls]
    if raw:
        message["_raw"] = "private"
    return message


def tool(call_id):
    return {"role": "tool", "tool_call_id": call_id, "content": "ok"}


@pytest.fixture
def conversation():
    return [
        user("one"), assistant("", ["a"], raw=True), tool("a"), assistant("first", raw=True),
        user("two"), assistant("second", raw=True),
        user("three"), assistant("", ["b", "c"], raw=True), tool("b"), tool("c"),
        assistant("third", raw=True),
    ]


class TestHistory:
    def test_a_run_can_continue_a_conversation(self, run_agent, kit):
        model = FakeModel([say("Hello, Sam."), say("Sam.")])
        first = run_agent(model, "My name is Sam.", kit.SCHEMAS, kit.TOOLS)
        second = run_agent(model, "What is my name?", kit.SCHEMAS, kit.TOOLS,
                           history=first["messages"])
        assert len(model.requests[1]["messages"]) == 3
        assert second["answer"] == "Sam."
        assert len(second["messages"]) == 4

    def test_the_callers_history_is_not_changed(self, run_agent, kit):
        history = [user("hi"), assistant("hello")]
        run_agent(FakeModel([say("again")]), "hi again", kit.SCHEMAS, kit.TOOLS,
                  history=history)
        assert len(history) == 2, "Start from a copy of the history, not the list itself."

    def test_no_history_is_a_fresh_run(self, run_agent, kit):
        result = run_agent(FakeModel([say("Hi.")]), "Hello", kit.SCHEMAS, kit.TOOLS)
        assert len(result["messages"]) == 2


class TestEstimate:
    def test_four_characters_a_token(self, memory):
        messages = [user("x" * 40), assistant("y" * 41), tool("a")]
        assert memory.estimate_tokens(messages) == 20

    def test_empty(self, memory):
        assert memory.estimate_tokens([]) == 0


class TestTrim:
    def test_keeps_the_last_turns(self, memory, conversation):
        kept = memory.trim(conversation, 2)
        assert [m["content"] for m in kept if m["role"] == "user"] == ["two", "three"]
        assert len(kept) == 7

    def test_one_turn(self, memory, conversation):
        kept = memory.trim(conversation, 1)
        assert kept[0] == user("three")
        assert len(kept) == 5

    def test_the_result_is_a_legal_conversation(self, memory, conversation):
        for max_turns in (1, 2, 3, 9):
            kept = memory.trim(conversation, max_turns)
            check_messages(kept + [user("next")])

    def test_private_keys_are_dropped_when_something_is_cut(self, memory, conversation):
        kept = memory.trim(conversation, 2)
        assert not any("_raw" in message for message in kept), (
            "After a cut, the provider's private copies no longer match the "
            "conversation. Return copies without any key starting with '_'."
        )

    def test_the_originals_are_not_changed(self, memory, conversation):
        memory.trim(conversation, 1)
        assert len(conversation) == 11
        assert conversation[-1].get("_raw") == "private"

    def test_nothing_to_cut_changes_nothing(self, memory, conversation):
        kept = memory.trim(conversation, 3)
        assert kept == conversation
        assert kept[1].get("_raw") == "private", (
            "When no turn is cut, the private keys are still valid - keep them."
        )

    def test_more_room_than_turns(self, memory, conversation):
        assert memory.trim(conversation, 50) == conversation

    def test_empty(self, memory):
        assert memory.trim([], 5) == []


class TestCarry:
    def test_a_finished_run_is_carried(self, memory):
        result = {"stopped": "done", "messages": [user("a"), assistant("b")]}
        assert memory.carry([], result) == [user("a"), assistant("b")]

    def test_and_trimmed(self, memory, conversation):
        result = {"stopped": "done", "messages": conversation}
        assert len(memory.carry([], result, max_turns=1)) == 5

    @pytest.mark.parametrize("stopped", ["max_steps", "repeating", "error", "length"])
    def test_a_stopped_run_is_not(self, memory, stopped):
        history = [user("a"), assistant("b")]
        result = {"stopped": stopped,
                  "messages": history + [user("c"), assistant("", ["x"])]}
        assert memory.carry(history, result) == history, (
            "A run that was stopped early can end with unanswered tool calls. "
            "Keep the previous history instead."
        )


class TestLongTerm:
    def test_remember_then_recall(self, memory):
        assert memory.remember("Sam is vegetarian") == "Remembered."
        assert memory.remember("Sam's dentist is Dr Rao") == "Remembered."
        assert memory.recall("dentist") == "Sam's dentist is Dr Rao"
        assert memory.recall() == "Sam is vegetarian\nSam's dentist is Dr Rao"

    def test_it_is_a_json_file(self, memory, memory_file):
        memory.remember("Sam is vegetarian")
        assert json.loads(memory_file.read_text()) == ["Sam is vegetarian"]

    def test_no_duplicates(self, memory, memory_file):
        memory.remember("Sam is vegetarian")
        assert memory.remember("Sam is vegetarian") == "I already know that."
        assert len(json.loads(memory_file.read_text())) == 1

    def test_recall_ignores_capitals(self, memory):
        memory.remember("Sam is Vegetarian")
        assert memory.recall("VEGETARIAN") == "Sam is Vegetarian"

    def test_nothing_yet(self, memory):
        assert memory.recall() == "Nothing remembered yet."

    def test_nothing_about_that(self, memory):
        memory.remember("Sam is vegetarian")
        assert memory.recall("car") == "Nothing remembered about 'car'."

    def test_schemas_and_table(self, memory):
        names = [schema["name"] for schema in memory.MEMORY_SCHEMAS]
        assert names == ["remember", "recall"]
        assert set(memory.MEMORY_TOOLS) == {"remember", "recall"}
        for schema in memory.MEMORY_SCHEMAS:
            assert len(schema["description"].split()) >= 10
        assert memory.MEMORY_SCHEMAS[0]["parameters"]["required"] == ["fact"]
        assert memory.MEMORY_SCHEMAS[1]["parameters"]["required"] == []
        FakeModel([say("ok")]).chat([user("hi")], tools=memory.MEMORY_SCHEMAS)

    def test_a_fact_outlives_the_conversation(self, run_agent, kit, memory):
        schemas = kit.SCHEMAS + memory.MEMORY_SCHEMAS
        tools = dict(kit.TOOLS)
        tools.update(memory.MEMORY_TOOLS)

        first = FakeModel([use("remember", {"fact": "Sam is vegetarian"}), say("Noted.")])
        run_agent(first, "I'm vegetarian, by the way.", schemas, tools)

        second = FakeModel([use("recall", {"word": "vegetarian"}), say("You are vegetarian.")])
        result = run_agent(second, "What do I eat?", schemas, tools)
        assert result["messages"][2]["content"] == "Sam is vegetarian"
