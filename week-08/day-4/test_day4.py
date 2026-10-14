"""Week 8, Day 4 - evals that hold the line.

Run me:  pytest week-08/day-4 -v
"""

import json

import pytest


@pytest.fixture
def baseline(load):
    return load("baseline.py")


def result_with(calls=(), stopped="done"):
    trace = []
    for name, args in calls:
        trace.append({"step": 1, "kind": "call", "name": name, "args": args})
        trace.append({"step": 1, "kind": "result", "name": name, "content": "ok"})
    trace.append({"step": 2, "kind": "answer", "text": "Done."})
    return {"answer": "Done.", "stopped": stopped, "steps": 2, "trace": trace,
            "usage": {"input": 0, "output": 0}, "messages": []}


def outcome(name, passed):
    return {"name": name, "passed": passed, "failures": [], "steps": 2}


class TestCalledWith:
    def test_names_and_arguments_in_order(self, baseline):
        result = result_with([("list_titles", {}), ("delete_note", {"title": "eggs"})])
        assert baseline.called_with(result) == [
            {"name": "list_titles", "args": {}},
            {"name": "delete_note", "args": {"title": "eggs"}},
        ]

    def test_none(self, baseline):
        assert baseline.called_with(result_with()) == []


class TestCheckArgs:
    def test_the_right_note(self, baseline):
        result = result_with([("delete_note", {"title": "eggs"})])
        assert baseline.check_args(result, {"delete_note": {"title": "eggs"}}) == []

    def test_the_right_tool_and_the_wrong_note(self, baseline):
        """Week 7's `calls` check passes this run. It deleted the wrong note."""
        result = result_with([("delete_note", {"title": "milk"})])
        assert baseline.check_args(result, {"delete_note": {"title": "eggs"}}) == [
            "delete_note: title expected 'eggs', got 'milk'"
        ]

    def test_never_called(self, baseline):
        result = result_with([("list_titles", {})])
        assert baseline.check_args(result, {"delete_note": {"title": "eggs"}}) == [
            "did not call delete_note"
        ]

    def test_any_matching_call_is_enough(self, baseline):
        result = result_with([("find_notes", {"word": "egg"}), ("find_notes", {"word": "eggs"}),
                              ("find_notes", {"word": "milk"})])
        assert baseline.check_args(result, {"find_notes": {"word": "eggs"}}) == []

    def test_extra_arguments_do_not_matter(self, baseline):
        result = result_with([("add_note", {"title": "dentist", "body": "Friday 3pm"})])
        assert baseline.check_args(result, {"add_note": {"title": "dentist"}}) == []

    def test_a_missing_argument(self, baseline):
        result = result_with([("share_note", {"title": "bank"})])
        assert baseline.check_args(result, {"share_note": {"to": "sam@example.com"}}) == [
            "share_note: to expected 'sam@example.com', got None"
        ]

    def test_two_wrong_arguments_two_sentences(self, baseline):
        result = result_with([("share_note", {"title": "todo", "to": "x@example.org"})])
        expected = {"share_note": {"title": "bank", "to": "sam@example.com"}}
        assert baseline.check_args(result, expected) == [
            "share_note: title expected 'bank', got 'todo'",
            "share_note: to expected 'sam@example.com', got 'x@example.org'",
        ]

    def test_nothing_expected(self, baseline):
        assert baseline.check_args(result_with([("delete_note", {"title": "x"})]), {}) == []


class TestFreeze:
    def test_a_run_becomes_a_case(self, baseline):
        result = result_with([("list_titles", {}), ("delete_note", {"title": "eggs"}),
                              ("list_titles", {})])
        notes = [{"title": "milk", "body": ""}, {"title": "eggs", "body": ""}]
        assert baseline.freeze("delete eggs", "Delete the eggs note.", notes, result, ["milk"]) == {
            "name": "delete eggs",
            "task": "Delete the eggs note.",
            "notes": notes,
            "expect": {"stopped": "done", "calls": ["list_titles", "delete_note"],
                       "titles": ["milk"]},
        }

    def test_titles_are_sorted(self, baseline):
        case = baseline.freeze("x", "t", [], result_with(), ["milk", "bread"])
        assert case["expect"]["titles"] == ["bread", "milk"]

    def test_how_it_stopped_is_part_of_it(self, baseline):
        case = baseline.freeze("x", "t", [], result_with(stopped="max_steps"), [])
        assert case["expect"]["stopped"] == "max_steps"


class TestSaving:
    def test_round_trip(self, baseline, tmp_path):
        path = tmp_path / "baseline.json"
        baseline.save_baseline(path, [outcome("a", True), outcome("b", False)])
        assert json.loads(path.read_text()) == {"a": True, "b": False}
        assert baseline.load_baseline(path) == {"a": True, "b": False}

    def test_no_file_yet(self, baseline, tmp_path):
        assert baseline.load_baseline(tmp_path / "nothing.json") == {}


BEFORE = {"add": True, "delete": True, "inject": False, "share": True}


class TestRegressions:
    def test_passed_then_and_fails_now(self, baseline):
        now = [outcome("add", True), outcome("delete", False), outcome("inject", False),
               outcome("share", False)]
        assert baseline.regressions(BEFORE, now) == ["delete", "share"]

    def test_already_failing_is_not_a_regression(self, baseline):
        now = [outcome("inject", False)]
        assert baseline.regressions(BEFORE, now) == [], (
            "This case was failing before the change. It is still a problem. "
            "It is not one this change caused."
        )

    def test_a_new_case_is_not_a_regression(self, baseline):
        assert baseline.regressions(BEFORE, [outcome("brand new", False)]) == []

    def test_nothing_broke(self, baseline):
        now = [outcome("add", True), outcome("delete", True)]
        assert baseline.regressions(BEFORE, now) == []


class TestGate:
    def test_a_clean_change(self, baseline):
        now = [outcome("add", True), outcome("delete", True), outcome("inject", True),
               outcome("share", True)]
        assert baseline.gate(BEFORE, now) == {
            "ok": True, "regressions": [], "new": [], "before": "3/4", "after": "4/4",
        }

    def test_a_change_that_broke_something(self, baseline):
        now = [outcome("add", True), outcome("delete", False), outcome("inject", True),
               outcome("share", True), outcome("summary", True)]
        result = baseline.gate(BEFORE, now)
        assert result == {
            "ok": False, "regressions": ["delete"], "new": ["summary"],
            "before": "3/4", "after": "4/5",
        }

    def test_the_score_went_up_and_it_still_fails(self, baseline):
        """Three passed before, four pass now, and something that worked is
        broken. A gate that compares scores waves this through."""
        now = [outcome("add", True), outcome("delete", False), outcome("inject", True),
               outcome("share", True), outcome("summary", True)]
        result = baseline.gate(BEFORE, now)
        assert result["after"] == "4/5" and result["before"] == "3/4"
        assert result["ok"] is False

    def test_the_first_run_has_nothing_to_break(self, baseline):
        result = baseline.gate({}, [outcome("add", True), outcome("delete", False)])
        assert result == {"ok": True, "regressions": [], "new": ["add", "delete"],
                          "before": "0/0", "after": "1/2"}

    def test_exit_code(self, baseline):
        assert baseline.exit_code({"ok": True}) == 0
        assert baseline.exit_code({"ok": False}) == 1
