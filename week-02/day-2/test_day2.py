"""Week 2, Day 2 - lists and for loops.

Run me:  pytest week-02/day-2 -v
"""

import pytest


class TestTotal:
    @pytest.mark.parametrize("numbers,answer", [
        ([1, 2, 3], 6), ([], 0), ([10], 10), ([2.5, 2.5], 5.0), ([-1, 1], 0),
    ])
    def test_total(self, load, numbers, answer):
        assert load("lists.py").total(numbers) == answer

    def test_wrote_the_loop(self, load, source):
        load("lists.py").total
        code = source("lists.py", code_only=True)
        assert "sum(" not in code, "Write the loop yourself today - no sum()."


class TestLongest:
    @pytest.mark.parametrize("words,answer", [
        (["a", "abc", "ab"], "abc"), ([], ""), (["one"], "one"),
        (["cat", "dog"], "cat"),
    ])
    def test_longest(self, load, words, answer):
        assert load("lists.py").longest(words) == answer


class TestNumbered:
    def test_numbered(self, load):
        assert load("lists.py").numbered(["hello", "bye"]) == ["1. hello", "2. bye"]

    def test_empty(self, load):
        assert load("lists.py").numbered([]) == []

    def test_visits_every_line(self, load):
        result = load("lists.py").numbered(["a", "b", "c", "d"])
        assert len(result) == 4, (
            f"Four lines in, {len(result)} out. If you got 1, your `return` is "
            "inside the loop - it leaves after the first item."
        )
        assert result[-1] == "4. d"


class TestOnlyCommands:
    def test_filters(self, load):
        lines = ["hello", "/help", "bye", "/quit"]
        assert load("lists.py").only_commands(lines) == ["/help", "/quit"]

    def test_none_match(self, load):
        assert load("lists.py").only_commands(["a", "b"]) == []

    def test_leaves_the_original_alone(self, load):
        lines = ["hello", "/help"]
        load("lists.py").only_commands(lines)
        assert lines == ["hello", "/help"], (
            "The list that was passed in has changed. Build a new list and "
            "return that."
        )

    def test_gives_back_a_new_list(self, load):
        lines = ["/a", "/b"]
        assert load("lists.py").only_commands(lines) is not lines
