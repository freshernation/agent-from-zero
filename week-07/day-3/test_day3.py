"""Week 7, Day 3 - evals.

Run me:  pytest week-07/day-3 -v
"""

import json

import pytest

from llm import FakeModel, say, use


@pytest.fixture
def evals(load):
    return load("evals.py")


@pytest.fixture
def kit(load):
    return load("kit.py")


def result_with(calls=(), answer="Done.", stopped="done", steps=2):
    trace = []
    for name in calls:
        trace.append({"step": 1, "kind": "call", "name": name, "args": {}})
        trace.append({"step": 1, "kind": "result", "name": name, "content": "ok"})
    trace.append({"step": steps, "kind": "answer", "text": answer})
    return {"answer": answer, "stopped": stopped, "steps": steps, "trace": trace,
            "usage": {"input": 0, "output": 0}, "messages": []}


class TestToolsCalled:
    def test_in_order(self, evals):
        result = result_with(["list_titles", "delete_note", "list_titles"])
        assert evals.tools_called(result) == ["list_titles", "delete_note", "list_titles"]

    def test_none(self, evals):
        assert evals.tools_called(result_with()) == []


class TestCheck:
    def test_nothing_expected_always_passes(self, evals):
        assert evals.check(result_with(), {}, []) == []

    def test_everything_right(self, evals):
        result = result_with(["calculate"], answer="It is 17400.", steps=2)
        expect = {"stopped": "done", "answer_contains": "17400", "calls": ["calculate"],
                  "never_calls": ["delete_note"], "max_steps": 3, "titles": ["milk"]}
        assert evals.check(result, expect, ["milk"]) == []

    @pytest.mark.parametrize("result,expect,titles,failure", [
        (result_with(stopped="max_steps"), {"stopped": "done"}, [],
         "stopped: expected 'done', got 'max_steps'"),
        (result_with(answer="No idea."), {"answer_contains": "17400"}, [],
         "answer does not contain '17400'"),
        (result_with(["list_titles"]), {"calls": ["calculate"]}, [],
         "did not call calculate"),
        (result_with(["delete_note"]), {"never_calls": ["delete_note"]}, [],
         "called delete_note"),
        (result_with(steps=7), {"max_steps": 4}, [],
         "took 7 steps, more than 4"),
        (result_with(), {"titles": ["milk"]}, ["milk", "eggs"],
         "notes: expected ['milk'], got ['eggs', 'milk']"),
    ])
    def test_each_failure(self, evals, result, expect, titles, failure):
        assert evals.check(result, expect, titles) == [failure]

    def test_answer_contains_ignores_capitals(self, evals):
        assert evals.check(result_with(answer="EGGS deleted"),
                           {"answer_contains": "eggs"}, []) == []

    def test_titles_ignore_order(self, evals):
        assert evals.check(result_with(), {"titles": ["a", "b"]}, ["b", "a"]) == []

    def test_exactly_at_the_step_limit_is_fine(self, evals):
        assert evals.check(result_with(steps=4), {"max_steps": 4}, []) == []

    def test_several_failures_in_order(self, evals):
        result = result_with(["add_note"], answer="Hm.", stopped="repeating", steps=9)
        expect = {"stopped": "done", "calls": ["calculate", "list_titles"],
                  "never_calls": ["add_note"], "max_steps": 3}
        assert evals.check(result, expect, []) == [
            "stopped: expected 'done', got 'repeating'",
            "did not call calculate",
            "did not call list_titles",
            "called add_note",
            "took 9 steps, more than 3",
        ]


class TestRunCase:
    def test_a_passing_case(self, evals, kit):
        case = {
            "name": "delete one of two",
            "notes": [{"title": "milk", "body": ""}, {"title": "eggs", "body": ""}],
            "task": "Delete the eggs note.",
            "expect": {"titles": ["milk"], "calls": ["delete_note"]},
        }
        model = FakeModel([use("delete_note", {"title": "eggs"}), say("Deleted eggs.")])
        assert evals.run_case(model, case, kit.SCHEMAS, kit.TOOLS) == {
            "name": "delete one of two", "passed": True, "failures": [], "steps": 2,
        }

    def test_a_failing_case(self, evals, kit):
        case = {
            "name": "delete one of two",
            "notes": [{"title": "milk", "body": ""}, {"title": "eggs", "body": ""}],
            "task": "Delete the eggs note.",
            "expect": {"titles": ["milk"], "calls": ["delete_note"]},
        }
        lazy = FakeModel([say("I have deleted it.")])
        outcome = evals.run_case(lazy, case, kit.SCHEMAS, kit.TOOLS)
        assert outcome["passed"] is False
        assert outcome["failures"] == [
            "did not call delete_note",
            "notes: expected ['milk'], got ['eggs', 'milk']",
        ], "The model SAID it deleted the note. Check the file, not the sentence."

    def test_every_case_starts_clean(self, evals, kit, notes_file):
        notes_file.write_text(json.dumps([{"title": "left over", "body": ""}]))
        case = {"name": "add", "task": "Add milk.", "expect": {"titles": ["milk"]}}
        model = FakeModel([use("add_note", {"title": "milk"}), say("Added.")])
        assert evals.run_case(model, case, kit.SCHEMAS, kit.TOOLS)["passed"] is True

    def test_passes_the_system_prompt_and_the_gate(self, evals, kit):
        case = {"name": "gate", "notes": [{"title": "milk", "body": ""}],
                "task": "Delete milk.", "expect": {"titles": ["milk"]}}
        model = FakeModel([use("delete_note", {"title": "milk"}), say("Not allowed.")])
        outcome = evals.run_case(model, case, kit.SCHEMAS, kit.TOOLS, system="You are Desk.",
                                 dangerous={"delete_note"}, approve=None)
        assert outcome["passed"] is True
        assert model.requests[0]["system"] == "You are Desk."


class TestReport:
    def test_report(self, evals):
        outcomes = [
            {"name": "add a note", "passed": True, "failures": [], "steps": 2},
            {"name": "delete one", "passed": False, "steps": 1,
             "failures": ["did not call delete_note", "called add_note"]},
        ]
        assert evals.report(outcomes) == (
            "PASS add a note\n"
            "FAIL delete one: did not call delete_note; called add_note\n"
            "1/2 passed"
        )

    def test_all_passing(self, evals):
        outcomes = [{"name": "a", "passed": True, "failures": [], "steps": 1}]
        assert evals.report(outcomes) == "PASS a\n1/1 passed"
