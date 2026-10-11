"""Week 1, Day 2 - conversion, arithmetic, if/elif/else.

Run me:  pytest week-01/day-2 -v
"""

import pytest


class TestCost:
    @pytest.mark.parametrize("count,price,total", [
        ("3", "0.5", "Total: $1.50"),
        ("10", "0.25", "Total: $2.50"),
        ("0", "9.99", "Total: $0.00"),
        ("7", "1", "Total: $7.00"),
    ])
    def test_total(self, run, count, price, total):
        run("cost.py", answers=[count, price]).expect(total)


class TestLimit:
    @pytest.mark.parametrize("used,limit,line", [
        ("3", "10", "OK"),
        ("10", "10", "At the limit"),
        ("12", "10", "Over the limit by 2"),
        ("25", "10", "Over the limit by 15"),
    ])
    def test_messages(self, run, used, limit, line):
        run("limit.py", answers=[used, limit]).expect(line)

    def test_nine_is_less_than_ten(self, run):
        r = run("limit.py", answers=["9", "10"])
        assert "Over" not in r.text, (
            "9 steps against a limit of 10 printed 'Over'. If you compared the "
            "text '9' with the text '10', Python compared them alphabetically - "
            "and '9' comes after '1'. Convert both to int first."
        )
        r.expect("OK")

    def test_prints_only_one_verdict(self, run):
        r = run("limit.py", answers=["10", "10"]).require_output()
        assert "OK" not in r.text and "Over" not in r.text, (
            "At exactly the limit, only 'At the limit' should print."
        )


class TestReply:
    @pytest.mark.parametrize("typed,line", [
        ("hello", "Bot: Hi there!"),
        ("bye", "Bot: Goodbye!"),
        ("", "Bot: Say something."),
        ("pizza", 'Bot: I don\'t understand "pizza".'),
    ])
    def test_each_branch(self, run, typed, line):
        run("reply.py", answers=[typed]).expect(line)

    @pytest.mark.parametrize("typed", ["HELLO", "  hello  ", "Hello"])
    def test_capitals_and_spaces_do_not_matter(self, run, typed):
        run("reply.py", answers=[typed]).expect("Bot: Hi there!")

    def test_only_spaces_counts_as_nothing(self, run):
        run("reply.py", answers=["   "]).expect("Bot: Say something.")

    def test_echoes_the_tidy_version(self, run):
        run("reply.py", answers=["  PIZZA "]).expect('Bot: I don\'t understand "pizza".')
