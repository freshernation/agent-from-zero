"""Week 2, Day 1 - functions, return, defaults.

Run me:  pytest week-02/day-1 -v
"""

import pytest


class TestShout:
    def test_shout(self, load):
        assert load("text_tools.py").shout("hello") == "HELLO!"

    def test_returns_rather_than_prints(self, load, capsys):
        result = load("text_tools.py").shout("hi")
        printed = capsys.readouterr().out
        assert result is not None, (
            "shout() handed back None. A function with no `return` gives None - "
            "you probably printed the answer instead of returning it."
        )
        assert printed == "", "shout() should return its answer, not print it."


class TestWordCount:
    @pytest.mark.parametrize("text,count", [
        ("one two three", 3), ("hello", 1), ("", 0), ("  spaced   out  ", 2),
    ])
    def test_word_count(self, load, text, count):
        assert load("text_tools.py").word_count(text) == count

    def test_gives_a_number(self, load):
        assert isinstance(load("text_tools.py").word_count("a b"), int)


class TestIsCommand:
    @pytest.mark.parametrize("text,answer", [
        ("/help", True), ("  /quit", True), ("help", False),
        ("", False), ("not /a command", False),
    ])
    def test_is_command(self, load, text, answer):
        result = load("text_tools.py").is_command(text)
        assert result is answer, (
            f"is_command({text!r}) gave {result!r}; expected {answer!r}. Return a "
            "real True or False."
        )


class TestGreeting:
    def test_calm_by_default(self, load):
        assert load("text_tools.py").greeting("Sam") == "Hello, Sam."

    def test_excited(self, load):
        assert load("text_tools.py").greeting("Sam", excited=True) == "Hello, Sam!"

    def test_explicitly_calm(self, load):
        assert load("text_tools.py").greeting("Ada", excited=False) == "Hello, Ada."
