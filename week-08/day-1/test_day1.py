"""Week 8, Day 1 - what is in the window.

Run me:  pytest week-08/day-1 -v
"""

import pytest

from llm import FakeModel, say


@pytest.fixture
def context(load):
    return load("context.py")


def conversation():
    """Three turns. The middle one has a large tool result in it."""
    return [
        {"role": "user", "content": "Add a note about the dentist."},
        {"role": "assistant", "content": "", "tool_calls": [
            {"id": "c1", "name": "add_note", "args": {"title": "dentist"}}], "_raw": "x"},
        {"role": "tool", "tool_call_id": "c1", "content": "Saved 'dentist'."},
        {"role": "assistant", "content": "Saved."},
        {"role": "user", "content": "What have I saved about work?"},
        {"role": "assistant", "content": "", "tool_calls": [
            {"id": "c2", "name": "find_notes", "args": {"word": "work"}}]},
        {"role": "tool", "tool_call_id": "c2", "content": "w" * 2000},
        {"role": "assistant", "content": "A long list about work."},
        {"role": "user", "content": "Delete the dentist note."},
        {"role": "assistant", "content": "", "tool_calls": [
            {"id": "c3", "name": "delete_note", "args": {"title": "dentist"}}]},
        {"role": "tool", "tool_call_id": "c3", "content": "Deleted 'dentist'."},
        {"role": "assistant", "content": "Deleted."},
    ]


class TestSizes:
    def test_tokens(self, context):
        assert context.tokens("a" * 400) == 100
        assert context.tokens("abc") == 0

    def test_by_role(self, context):
        found = context.sizes(conversation())
        assert found["tool"] == 508
        assert found["user"] == 20
        assert found["total"] == found["user"] + found["assistant"] + found["tool"]

    def test_the_window_is_mostly_tool_results(self, context):
        found = context.sizes(conversation())
        assert found["tool"] > 0.9 * found["total"], (
            "One search result is over nine tenths of this conversation. What "
            "fills a window is almost never what the user typed."
        )

    def test_empty(self, context):
        assert context.sizes([]) == {"user": 0, "assistant": 0, "tool": 0, "total": 0}


class TestShortenOldResults:
    def test_an_old_result_is_cut(self, context):
        shorter = context.shorten_old_results(conversation(), keep_last=1, limit=200)
        assert shorter[6]["content"] == "w" * 200 + " [shortened: 1800 characters removed]"

    def test_recent_results_are_left_alone(self, context):
        shorter = context.shorten_old_results(conversation(), keep_last=2, limit=10)
        assert shorter[6]["content"] == "w" * 2000
        assert shorter[10]["content"] == "Deleted 'dentist'."
        assert shorter[2]["content"].startswith("Saved 'den [shortened")

    def test_short_results_are_not_touched(self, context):
        shorter = context.shorten_old_results(conversation(), keep_last=0, limit=200)
        assert shorter[2]["content"] == "Saved 'dentist'."

    def test_nothing_is_dropped(self, context):
        before = conversation()
        shorter = context.shorten_old_results(before, keep_last=0, limit=5)
        assert len(shorter) == len(before)
        roles = []
        for message in shorter:
            roles.append(message["role"])
        assert roles.count("tool") == 3, (
            "A tool result was removed. The model asked for it, so the API "
            "insists on an answer. Shorten it; never drop it."
        )
        assert shorter[6]["tool_call_id"] == "c2"

    def test_the_original_is_not_changed(self, context):
        before = conversation()
        context.shorten_old_results(before, keep_last=0, limit=5)
        assert before[6]["content"] == "w" * 2000

    def test_the_result_is_still_a_legal_conversation(self, context):
        shorter = context.shorten_old_results(conversation(), keep_last=0, limit=5)
        shorter.append({"role": "user", "content": "And now?"})
        FakeModel([say("ok")]).chat(shorter)


class TestSplitTurns:
    def test_three_turns(self, context):
        turns = context.split_turns(conversation())
        assert len(turns) == 3
        assert turns[0][0]["content"] == "Add a note about the dentist."
        assert len(turns[1]) == 4
        assert turns[2][-1]["content"] == "Deleted."

    def test_nothing(self, context):
        assert context.split_turns([]) == []


class TestSummarise:
    def test_transcript(self, context):
        text = context.transcript(conversation()[:4])
        assert text.splitlines()[0] == "user: Add a note about the dentist."
        assert text.splitlines()[2] == "tool: Saved 'dentist'."

    def test_the_instructions_say_what_must_survive(self, context):
        system = context.SUMMARY_SYSTEM
        assert len(system.split()) >= 30
        assert "title" in system.lower()

    def test_one_call_with_its_own_instructions(self, context):
        model = FakeModel([say("The user saved a dentist note.")])
        text = context.summarise(model, conversation()[:4])
        assert text == "The user saved a dentist note."
        assert model.call_count == 1
        request = model.last_request
        assert request["system"] == context.SUMMARY_SYSTEM
        assert not request["tools"], "The summariser needs no tools."
        assert len(request["messages"]) == 1
        assert "Saved 'dentist'." in request["messages"][0]["content"]


class TestCompact:
    def test_a_short_conversation_costs_nothing(self, context):
        model = FakeModel([])
        kept = context.compact(model, conversation(), keep_turns=3)
        assert kept == conversation()
        assert model.call_count == 0, (
            "Three turns, keep three: there is nothing to summarise, and a "
            "summary is a model call you pay for."
        )

    def test_old_turns_become_a_summary(self, context):
        model = FakeModel([say("A dentist note was saved, then work was searched.")])
        kept = context.compact(model, conversation(), keep_turns=1)
        assert len(kept) == 4
        assert kept[0]["role"] == "user"
        assert kept[0]["content"] == (
            "Summary of the conversation so far: A dentist note was saved, then "
            "work was searched.\n\nDelete the dentist note."
        )
        assert kept[-1]["content"] == "Deleted."

    def test_only_the_old_turns_are_sent_to_be_summarised(self, context):
        model = FakeModel([say("summary")])
        context.compact(model, conversation(), keep_turns=1)
        sent = model.last_request["messages"][0]["content"]
        assert "Add a note about the dentist." in sent
        assert "Delete the dentist note." not in sent

    def test_private_keys_do_not_survive(self, context):
        model = FakeModel([say("summary")])
        kept = context.compact(model, conversation(), keep_turns=2)
        for message in kept:
            for key in message:
                assert not key.startswith("_")

    def test_the_original_is_not_changed(self, context):
        before = conversation()
        context.compact(FakeModel([say("summary")]), before, keep_turns=1)
        assert before[8]["content"] == "Delete the dentist note."
        assert len(before) == 12

    def test_the_result_is_a_legal_conversation(self, context):
        kept = context.compact(FakeModel([say("summary")]), conversation(), keep_turns=1)
        kept.append({"role": "user", "content": "And now?"})
        FakeModel([say("ok")]).chat(kept)

    def test_it_is_much_smaller(self, context):
        kept = context.compact(FakeModel([say("summary")]), conversation(), keep_turns=1)
        assert context.sizes(kept)["total"] < 0.1 * context.sizes(conversation())["total"]


class TestShouldCompact:
    def test_threshold(self, context):
        assert context.should_compact(600, 1000) is True
        assert context.should_compact(500, 1000) is True
        assert context.should_compact(499, 1000) is False
        assert context.should_compact(700, 1000, fraction=0.8) is False
