"""Week 1 milestone - the rule-based chatbot.

Run me:  pytest week-01/milestone -v
"""

import pytest


class TestCommands:
    def test_hello(self, run):
        run("bot.py", answers=["hello", "quit"]).expect("Bot: Hi! I am Desk.")

    def test_help(self, run):
        run("bot.py", answers=["help", "quit"]).expect(
            "Bot: I know: hello, help, count, quit."
        )

    def test_unknown(self, run):
        run("bot.py", answers=["pizza", "quit"]).expect('Bot: I don\'t know "pizza" yet.')

    @pytest.mark.parametrize("typed", ["HELLO", "  hello ", "Hello"])
    def test_capitals_and_spaces(self, run, typed):
        run("bot.py", answers=[typed, "quit"]).expect("Bot: Hi! I am Desk.")


class TestCounting:
    def test_count_includes_itself(self, run):
        run("bot.py", answers=["hello", "pizza", "count", "quit"]).expect(
            "Bot: You have sent 3 messages."
        )

    def test_count_as_the_first_message(self, run):
        run("bot.py", answers=["count", "quit"]).expect("Bot: You have sent 1 messages.")

    def test_goodbye_includes_quit(self, run):
        run("bot.py", answers=["hello", "help", "quit"]).expect(
            "Bot: Bye! We exchanged 3 messages."
        )

    def test_quit_straight_away(self, run):
        run("bot.py", answers=["quit"]).expect("Bot: Bye! We exchanged 1 messages.")

    def test_empty_lines_are_not_counted(self, run):
        r = run("bot.py", answers=["hello", "", "   ", "count", "quit"])
        r.expect("Bot: Say something.")
        r.expect("Bot: You have sent 2 messages.")
        r.expect("Bot: Bye! We exchanged 3 messages.")


class TestTheLoop:
    def test_the_worked_example(self, run):
        r = run("bot.py", answers=["hello", "pizza", "", "count", "quit"])
        for line in [
            "Bot: Hi! I am Desk.",
            'Bot: I don\'t know "pizza" yet.',
            "Bot: Say something.",
            "Bot: You have sent 3 messages.",
            "Bot: Bye! We exchanged 4 messages.",
        ]:
            r.expect(line)

    def test_stops_after_quit(self, run):
        r = run("bot.py", answers=["QUIT", "hello"]).require_output()
        assert "Hi! I am Desk." not in r.text, "The loop kept going after quit."

    def test_keeps_going_for_a_long_time(self, run):
        r = run("bot.py", answers=["hello"] * 30 + ["quit"])
        assert r.text.count("Bot: Hi! I am Desk.") == 30
        r.expect("Bot: Bye! We exchanged 31 messages.")
