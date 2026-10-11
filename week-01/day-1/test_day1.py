"""Week 1, Day 1 - print, variables, f-strings, input.

Run me:  pytest week-01/day-1 -v
"""


class TestHello:
    def test_first_line_is_exact(self, run):
        r = run("hello.py")
        assert r.line(0) == "Hello, world!", (
            f"Line 1 should be exactly 'Hello, world!' but was {r.line(0)!r}. "
            "Check the capital H, the comma, and the exclamation mark."
        )

    def test_prints_three_lines(self, run):
        r = run("hello.py")
        assert len(r.lines) == 3, f"Expected exactly 3 lines, got {len(r.lines)}."

    def test_name_and_reason_are_not_empty(self, run):
        r = run("hello.py")
        assert r.line(1).strip(), "Line 2 should be your name."
        assert r.line(2).strip(), "Line 3 should be why you are doing this course."


class TestCard:
    def test_the_given_values(self, run):
        run("card.py").expect("Ada (tutor) has spoken 3 times.")

    def test_follows_the_variables(self, run_variant):
        r = run_variant("card.py", {
            'name = "Ada"': 'name = "Grace"',
            'role = "tutor"': 'role = "editor"',
            "turns = 3": "turns = 12",
        })
        assert "Grace (editor) has spoken 12 times." in r.text, (
            "With different values in the variables the sentence did not change. "
            "Build it from name, role and turns with an f-string - do not type "
            "the words Ada, tutor and 3 into the print."
        )


class TestGreet:
    def test_greets_by_name(self, run):
        run("greet.py", answers=["Sam"]).expect("Hello, Sam!")

    def test_counts_the_letters(self, run):
        run("greet.py", answers=["Sam"]).expect("Your name has 3 letters.")

    def test_a_different_name(self, run):
        r = run("greet.py", answers=["Priyanka"])
        r.expect("Hello, Priyanka!")
        r.expect("Your name has 8 letters.")

    def test_prompt_text(self, run):
        run("greet.py", answers=["Sam"]).expect("What is your name? ")
