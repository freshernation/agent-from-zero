"""Week 5, Day 2 - the dispatch table.

Run me:  pytest week-05/day-2 -v
"""

import json


class TestTable:
    def test_has_every_tool(self, load):
        assert set(load("dispatch.py").TOOLS) == {
            "add_note", "list_titles", "find_notes", "delete_note", "calculate",
        }

    def test_holds_functions_not_results(self, load):
        for name, function in load("dispatch.py").TOOLS.items():
            assert callable(function), (
                f"TOOLS[{name!r}] is {function!r}. Store the function itself - "
                "no brackets after the name."
            )


class TestRunTool:
    def test_returns_a_string(self, load):
        result = load("dispatch.py").run_tool("calculate", {"expression": "17 * 23"})
        assert result == "391"

    def test_really_runs_it(self, load, notes_file):
        result = load("dispatch.py").run_tool(
            "add_note", {"title": "milk", "body": "two litres"},
        )
        assert result == "Saved 'milk'."
        assert json.loads(notes_file.read_text()) == [
            {"title": "milk", "body": "two litres"},
        ]

    def test_a_tool_with_no_arguments(self, load):
        assert load("dispatch.py").run_tool("list_titles", {}) == "No notes yet."

    def test_an_optional_argument_left_out(self, load):
        assert load("dispatch.py").run_tool("add_note", {"title": "eggs"}) == (
            "Saved 'eggs'."
        )

    def test_unknown_tool(self, load):
        assert load("dispatch.py").run_tool("send_email", {}) == (
            "Error: unknown tool 'send_email'"
        ), "The model will sometimes invent a tool. That is normal, not a crash."

    def test_missing_argument(self, load):
        result = load("dispatch.py").run_tool("find_notes", {})
        assert result.startswith("Error: TypeError:"), (
            f"Got {result!r}. A missing argument raises TypeError - catch it and "
            "hand the message back, so the model can read it and try again."
        )
        assert "word" in result, "Keep Python's message - it names what was missing."

    def test_invented_argument(self, load):
        result = load("dispatch.py").run_tool(
            "calculate", {"expression": "1 + 1", "precision": "high"},
        )
        assert result.startswith("Error: TypeError:")

    def test_a_tool_that_blows_up(self, load):
        module = load("dispatch.py")

        def explode():
            raise RuntimeError("the disk is on fire")

        module.TOOLS["explode"] = explode
        assert module.run_tool("explode", {}) == "Error: RuntimeError: the disk is on fire"

    def test_a_result_that_is_not_text(self, load):
        module = load("dispatch.py")

        def count():
            return 3

        module.TOOLS["count"] = count
        assert module.run_tool("count", {}) == "3"


class TestRunCalls:
    def test_one_call(self, load):
        calls = [{"id": "call_7", "name": "calculate", "args": {"expression": "2 + 2"}}]
        assert load("dispatch.py").run_calls(calls) == [
            {"role": "tool", "tool_call_id": "call_7", "content": "4"},
        ]

    def test_several_calls_keep_their_ids_and_order(self, load):
        calls = [
            {"id": "a", "name": "add_note", "args": {"title": "milk"}},
            {"id": "b", "name": "calculate", "args": {"expression": "3 * 3"}},
            {"id": "c", "name": "list_titles", "args": {}},
        ]
        assert load("dispatch.py").run_calls(calls) == [
            {"role": "tool", "tool_call_id": "a", "content": "Saved 'milk'."},
            {"role": "tool", "tool_call_id": "b", "content": "9"},
            {"role": "tool", "tool_call_id": "c", "content": "1. milk"},
        ]

    def test_a_failure_still_gets_an_answer(self, load):
        calls = [
            {"id": "a", "name": "nonsense", "args": {}},
            {"id": "b", "name": "calculate", "args": {"expression": "1 + 1"}},
        ]
        results = load("dispatch.py").run_calls(calls)
        assert len(results) == 2, "One call in, one message out - always."
        assert results[0]["content"] == "Error: unknown tool 'nonsense'"
        assert results[1]["content"] == "2"

    def test_no_calls(self, load):
        assert load("dispatch.py").run_calls([]) == []
