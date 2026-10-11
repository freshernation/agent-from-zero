"""Week 3 milestone - Project 1.

Run me:  pytest week-03/milestone -v
"""

import json

import pytest

HELP = "Commands: add, list, find, delete, calc, quit"


class TestStore:
    def test_round_trip(self, load, tmp_path):
        module = load("store.py")
        notes = [{"title": "milk", "body": "two litres"}]
        module.save_notes(tmp_path / "n.json", notes)
        assert module.load_notes(tmp_path / "n.json") == notes

    def test_saves_real_json(self, load, tmp_path):
        load("store.py").save_notes(tmp_path / "n.json", [{"title": "a", "body": "b"}])
        assert json.loads((tmp_path / "n.json").read_text()) == [
            {"title": "a", "body": "b"},
        ]

    def test_missing_file(self, load, tmp_path):
        assert load("store.py").load_notes(tmp_path / "nope.json") == []

    def test_damaged_file(self, load, tmp_path):
        (tmp_path / "n.json").write_text("{oops")
        assert load("store.py").load_notes(tmp_path / "n.json") == []


class TestHandle:
    def test_add_with_a_body(self, load):
        notes = []
        assert load("app.py").handle(notes, "add milk | two litres") == "Saved 'milk'."
        assert notes == [{"title": "milk", "body": "two litres"}]

    def test_add_without_a_body(self, load):
        notes = []
        load("app.py").handle(notes, "add milk")
        assert notes == [{"title": "milk", "body": ""}]

    def test_add_tidies_spaces(self, load):
        notes = []
        load("app.py").handle(notes, "add   call the dentist  |  before Friday  ")
        assert notes == [{"title": "call the dentist", "body": "before Friday"}]

    def test_add_with_nothing_after_it(self, load):
        assert load("app.py").handle([], "add") == "A note needs a title."

    def test_list(self, load):
        notes = [{"title": "milk", "body": ""}, {"title": "eggs", "body": ""}]
        assert load("app.py").handle(notes, "list") == "1. milk\n2. eggs"

    def test_find(self, load):
        notes = [{"title": "milk", "body": "two litres"}]
        assert load("app.py").handle(notes, "find litres") == "milk: two litres"

    def test_delete(self, load):
        notes = [{"title": "milk", "body": ""}]
        assert load("app.py").handle(notes, "delete milk") == "Deleted 'milk'."
        assert notes == []

    def test_delete_a_title_with_spaces(self, load):
        notes = [{"title": "call the dentist", "body": ""}]
        load("app.py").handle(notes, "delete call the dentist")
        assert notes == []

    def test_calc(self, load):
        assert load("app.py").handle([], "calc 17 * 23") == "391"

    def test_calc_reports_errors(self, load):
        assert load("app.py").handle([], "calc 1 / 0") == "Error: Cannot divide by zero"

    @pytest.mark.parametrize("line", ["LIST", "List", "  list  "])
    def test_command_in_any_capitals(self, load, line):
        assert load("app.py").handle([], line) == "No notes yet."

    @pytest.mark.parametrize("line", ["", "   ", "dance", "help", "listen"])
    def test_anything_else_is_help(self, load, line):
        assert load("app.py").handle([], line) == HELP

    def test_handle_does_not_print(self, load, capsys):
        load("app.py").handle([], "list")
        assert capsys.readouterr().out == "", "handle() returns the reply; main() prints it."


class TestTheProgram:
    def test_a_session(self, run, tmp_path):
        r = run("app.py", answers=["add milk | two litres", "list", "quit"],
                env={"NOTES_FILE": tmp_path / "n.json"})
        r.expect("Saved 'milk'.")
        r.expect("1. milk")
        r.expect("Bye.")

    def test_it_remembers_between_runs(self, run, tmp_path):
        env = {"NOTES_FILE": tmp_path / "n.json"}
        run("app.py", answers=["add milk | two litres", "add eggs", "quit"], env=env)
        r = run("app.py", answers=["list", "quit"], env=env)
        r.expect("1. milk")
        r.expect("2. eggs")

    def test_it_saved_json(self, run, tmp_path):
        path = tmp_path / "n.json"
        run("app.py", answers=["add milk | two litres", "quit"],
            env={"NOTES_FILE": path})
        assert json.loads(path.read_text()) == [{"title": "milk", "body": "two litres"}]

    def test_a_damaged_file_does_not_stop_it(self, run, tmp_path):
        path = tmp_path / "n.json"
        path.write_text("{oops")
        r = run("app.py", answers=["list", "quit"], env={"NOTES_FILE": path})
        r.expect("No notes yet.")

    def test_bad_input_does_not_stop_it(self, run, tmp_path):
        r = run("app.py", answers=["calc rm -rf /", "calc 2 +", "delete nothing",
                                   "", "list", "quit"],
                env={"NOTES_FILE": tmp_path / "n.json"})
        r.expect("Error: Unsafe expression")
        r.expect("Error: Not a calculation")
        r.expect("No note called 'nothing'.")
        r.expect("Bye.")

    def test_quit_in_capitals(self, run, tmp_path):
        run("app.py", answers=["QUIT"], env={"NOTES_FILE": tmp_path / "n.json"}).expect("Bye.")


class TestTheShape:
    def test_importing_app_does_not_start_the_loop(self, load, capsys):
        load("app.py").handle
        assert capsys.readouterr().out == ""

    def test_only_the_store_knows_about_json(self, load, source):
        load("app.py").handle
        code = source("app.py", code_only=True)
        assert "import json" not in code and "json." not in code, (
            "app.py uses the json module. Loading and saving belong in store.py - app.py "
            "should just call load_notes and save_notes."
        )
