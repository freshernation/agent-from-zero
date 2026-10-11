"""Week 7 milestone - a gated, remembering, budgeted, measured agent.

Run me:  pytest week-07/milestone -v
"""

import json
from pathlib import Path

import pytest

from llm import FakeModel, say, use

KNOWN = {"stopped", "answer_contains", "calls", "never_calls", "max_steps", "titles"}


@pytest.fixture
def desk(load):
    return load("desk.py")


@pytest.fixture
def kit(load):
    return load("kit.py")


def nothing(seconds):
    pass


def yes(call):
    return True


def titles(notes_file):
    if not notes_file.exists():
        return []
    return [note["title"] for note in json.loads(notes_file.read_text())]


class TestSetup:
    def test_system_prompt(self, desk):
        assert isinstance(desk.SYSTEM, str) and len(desk.SYSTEM.split()) >= 40

    def test_delete_is_dangerous(self, desk):
        assert "delete_note" in desk.DANGEROUS

    def test_budget_is_a_number(self, desk):
        assert isinstance(desk.TOKEN_BUDGET, int) and desk.TOKEN_BUDGET > 0

    def test_all_seven_tools(self, desk):
        names = [schema["name"] for schema in desk.ALL_SCHEMAS]
        assert names == ["add_note", "list_titles", "find_notes", "delete_note",
                         "calculate", "remember", "recall"]
        assert set(desk.ALL_TOOLS) == set(names)

    def test_the_kit_was_not_changed(self, desk, kit):
        assert len(kit.SCHEMAS) == 5 and len(kit.TOOLS) == 5, (
            "Build ALL_SCHEMAS and ALL_TOOLS as new objects. Adding to the kit's "
            "own list or table changes it for everyone who imports it."
        )


class TestTakeTurn:
    def test_text_and_history(self, desk):
        model = FakeModel([use("add_note", {"title": "milk"}), say("Saved.")])
        turn = desk.take_turn(model, [], "Add milk.", wait=nothing)
        assert turn["text"] == "Saved.\n(done, 2 steps)"
        assert [m["role"] for m in turn["history"]] == [
            "user", "assistant", "tool", "assistant",
        ]

    def test_everything_is_switched_on(self, desk):
        model = FakeModel([say("Hi.")])
        desk.take_turn(model, [], "Hello", wait=nothing)
        assert model.requests[0]["system"] == desk.SYSTEM
        assert model.requests[0]["tools"] == desk.ALL_SCHEMAS

    def test_the_conversation_continues(self, desk):
        model = FakeModel([say("Hello, Sam."), say("Sam.")])
        first = desk.take_turn(model, [], "My name is Sam.", wait=nothing)
        desk.take_turn(model, first["history"], "What is my name?", wait=nothing)
        assert len(model.requests[1]["messages"]) == 3

    def test_a_stopped_turn_does_not_poison_the_next(self, desk):
        stuck = FakeModel([use("list_titles", id=f"c{n}") for n in range(9)])
        history = [{"role": "user", "content": "hi"},
                   {"role": "assistant", "content": "hello"}]
        turn = desk.take_turn(stuck, history, "Loop.", wait=nothing)
        assert turn["text"].endswith("(repeating, 3 steps)")
        assert turn["history"] == history
        after = desk.take_turn(FakeModel([say("Fine.")]), turn["history"], "ok?", wait=nothing)
        assert after["text"] == "Fine.\n(done, 1 steps)"

    def test_delete_is_refused_without_a_yes(self, desk, kit, notes_file):
        kit.add_note("milk")
        model = FakeModel([use("delete_note", {"title": "milk"}), say("I was not allowed.")])
        desk.take_turn(model, [], "Delete milk.", wait=nothing)
        assert titles(notes_file) == ["milk"]

    def test_delete_runs_with_a_yes(self, desk, kit, notes_file):
        kit.add_note("milk")
        model = FakeModel([use("delete_note", {"title": "milk"}), say("Deleted.")])
        desk.take_turn(model, [], "Delete milk.", approve=yes, wait=nothing)
        assert titles(notes_file) == []

    def test_memory_outlives_the_history(self, desk):
        first = FakeModel([use("remember", {"fact": "Sam is vegetarian"}), say("Noted.")])
        desk.take_turn(first, [], "I'm vegetarian.", wait=nothing)
        second = FakeModel([use("recall", {}), say("You are vegetarian.")])
        turn = desk.take_turn(second, [], "What do I eat?", wait=nothing)
        assert turn["history"][2]["content"] == "Sam is vegetarian"

    def test_the_budget_is_enforced(self, desk):
        greedy = FakeModel([
            use("calculate", {"expression": f"{n} + 1"}, id=f"c{n}",
                input=desk.TOKEN_BUDGET, output=1) for n in range(5)
        ])
        turn = desk.take_turn(greedy, [], "Go.", wait=nothing)
        assert turn["text"].endswith("(budget, 1 steps)")

    def test_the_program(self, run, tmp_path):
        r = run("desk.py", answers=["hello", "quit"],
                env={"NOTES_FILE": tmp_path / "n.json", "MEMORY_FILE": tmp_path / "m.json"})
        r.expect("Desk: (fake model) You said: hello")
        r.expect("(done, 1 steps)")
        r.expect("Bye.")


class TestYourCases:
    @pytest.fixture
    def cases(self, load):
        return load("cases.py").CASES

    def test_at_least_six(self, cases):
        assert len(cases) >= 6

    def test_each_is_well_formed(self, cases):
        names = [case["name"] for case in cases]
        assert len(set(names)) == len(names), "Every case needs its own name."
        for case in cases:
            assert isinstance(case["task"], str) and case["task"].strip()
            assert case["expect"], f"{case['name']} expects nothing, so it cannot fail."
            unknown = set(case["expect"]) - KNOWN
            assert not unknown, f"{case['name']} uses unknown checks: {unknown}"

    def test_the_required_kinds(self, cases):
        assert any(case.get("notes") for case in cases), "No case has starting notes."
        assert any("titles" in case["expect"] for case in cases), (
            "No case checks the notes afterwards. That is the strongest check you have."
        )
        assert any(case["expect"].get("never_calls") for case in cases), (
            "No case says what the agent must NOT do."
        )

    def test_one_case_where_nothing_should_change(self, cases):
        def unchanged(case):
            if "titles" not in case["expect"] or not case.get("notes"):
                return False
            start = sorted(note["title"] for note in case["notes"])
            return start == sorted(case["expect"]["titles"])

        assert any(unchanged(case) for case in cases), (
            "Include a case after which the notes should be exactly as they "
            "started - an impossible request, or an injected instruction."
        )

    def test_they_run(self, cases, load, kit):
        evals = load("evals.py")
        desk = load("desk.py")
        for case in cases:
            outcome = evals.run_case(FakeModel(say("ok")), case, desk.ALL_SCHEMAS,
                                     desk.ALL_TOOLS, dangerous=desk.DANGEROUS)
            assert set(outcome) == {"name", "passed", "failures", "steps"}


class TestTheReport:
    def text(self):
        return (Path(__file__).parent / "EVAL_REPORT.md").read_text()

    def test_every_question_is_answered(self):
        left = self.text().count("_(your answer")
        assert left == 0, f"EVAL_REPORT.md still has {left} unanswered section(s)."

    def test_real_output_is_pasted(self):
        text = self.text()
        assert "(paste the output" not in text
        assert " passed" in text and ("PASS " in text or "FAIL " in text), (
            "Paste what run_evals.py printed against a real model."
        )
