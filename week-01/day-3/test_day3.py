"""Week 1, Day 3 - while, break, loops that stop themselves.

Run me:  pytest week-01/day-3 -v
"""


class TestCountdown:
    def test_counts_down_from_three(self, run):
        r = run("countdown.py", answers=["3"])
        text = r.text.replace("Start: ", "")
        assert text.split() == ["3", "2", "1", "Liftoff!"], (
            f"From 3, expected 3, 2, 1, Liftoff! on separate lines. Got:\n{r.text}"
        )

    def test_zero_goes_straight_to_liftoff(self, run):
        r = run("countdown.py", answers=["0"])
        assert r.text.replace("Start: ", "").split() == ["Liftoff!"]

    def test_a_longer_one(self, run):
        r = run("countdown.py", answers=["12"])
        numbers = r.text.replace("Start: ", "").split()[:-1]
        assert numbers == [str(n) for n in range(12, 0, -1)]


class TestEcho:
    def test_echoes_each_line(self, run):
        r = run("echo.py", answers=["one", "two", "quit"])
        r.expect("Bot: one")
        r.expect("Bot: two")

    def test_says_goodbye(self, run):
        run("echo.py", answers=["quit"]).expect("Bot: Bye!")

    def test_does_not_echo_quit(self, run):
        r = run("echo.py", answers=["hi", "quit"]).require_output()
        assert "Bot: quit" not in r.text, (
            "The word quit was echoed back. Check for it BEFORE you print."
        )

    def test_quit_in_capitals(self, run):
        r = run("echo.py", answers=["hi", "QUIT"])
        r.expect("Bot: Bye!")
        assert "Bot: QUIT" not in r.text

    def test_stops_asking_after_quit(self, run):
        r = run("echo.py", answers=["quit", "still here?"]).require_output()
        assert "still here?" not in r.text, "The loop kept going after quit."


class TestBudget:
    def test_three_steps(self, run):
        run("budget.py", answers=["10", "4", "4", "4"]).expect(
            "Out of budget after 3 steps."
        )

    def test_exactly_zero_stops(self, run):
        run("budget.py", answers=["10", "5", "5"]).expect(
            "Out of budget after 2 steps."
        )

    def test_one_big_cost(self, run):
        run("budget.py", answers=["3", "100"]).expect("Out of budget after 1 steps.")

    def test_stops_asking_once_spent(self, run):
        r = run("budget.py", answers=["5", "5", "1", "1"])
        assert r.text.count("Cost: ") == 1, (
            "The budget was gone after the first cost, but the program asked "
            f"{r.text.count('Cost: ')} times."
        )
