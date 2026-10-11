"""Week 2, Day 3 - dictionaries and the message list.

Run me:  pytest week-02/day-3 -v
"""

import pytest


@pytest.fixture
def history():
    return [
        {"role": "user", "content": "Remember to buy milk"},
        {"role": "assistant", "content": "Saved."},
        {"role": "user", "content": "What did I ask?"},
    ]


def test_make_message(load):
    assert load("messages.py").make_message("user", "hi") == {
        "role": "user", "content": "hi",
    }


class TestAddMessage:
    def test_appends_to_the_same_list(self, load, history):
        load("messages.py").add_message(history, "assistant", "Milk.")
        assert history[-1] == {"role": "assistant", "content": "Milk."}, (
            "add_message should append to the list it was given - that is its job."
        )

    def test_returns_the_new_length(self, load, history):
        assert load("messages.py").add_message(history, "assistant", "Milk.") == 4

    def test_onto_an_empty_history(self, load):
        empty = []
        assert load("messages.py").add_message(empty, "user", "hi") == 1
        assert empty == [{"role": "user", "content": "hi"}]


class TestCountByRole:
    def test_counts(self, load, history):
        assert load("messages.py").count_by_role(history) == {
            "user": 2, "assistant": 1,
        }

    def test_empty(self, load):
        assert load("messages.py").count_by_role([]) == {}

    def test_any_role_at_all(self, load):
        result = load("messages.py").count_by_role([
            {"role": "tool", "content": "42"}, {"role": "tool", "content": "43"},
        ])
        assert result == {"tool": 2}, (
            "Do not assume the only roles are user and assistant. In week 5 a "
            "third one turns up."
        )


class TestLastFrom:
    def test_latest_user_message(self, load, history):
        assert load("messages.py").last_from(history, "user") == "What did I ask?"

    def test_latest_assistant_message(self, load, history):
        assert load("messages.py").last_from(history, "assistant") == "Saved."

    def test_role_that_never_spoke(self, load, history):
        assert load("messages.py").last_from(history, "tool") is None

    def test_empty(self, load):
        assert load("messages.py").last_from([], "user") is None


class TestTranscript:
    def test_transcript(self, load, history):
        assert load("messages.py").transcript(history) == (
            "user: Remember to buy milk\nassistant: Saved.\nuser: What did I ask?"
        )

    def test_empty(self, load):
        assert load("messages.py").transcript([]) == ""

    def test_does_not_change_the_history(self, load, history):
        before = [dict(message) for message in history]
        load("messages.py").transcript(history)
        assert history == before
