"""Week 3, Day 1 - JSON and files.

Run me:  pytest week-03/day-1 -v
"""

import json

NOTES = [{"title": "milk", "body": "two litres"}, {"title": "eggs", "body": "six"}]


class TestJson:
    def test_to_json_is_a_string(self, load):
        text = load("storage.py").to_json(NOTES)
        assert isinstance(text, str)
        assert json.loads(text) == NOTES

    def test_to_json_is_indented(self, load):
        text = load("storage.py").to_json({"title": "milk"})
        assert text == '{\n  "title": "milk"\n}', (
            f"Expected two-space indentation. Got:\n{text}"
        )

    def test_from_json(self, load):
        assert load("storage.py").from_json('[{"title": "milk"}]') == [{"title": "milk"}]

    def test_round_trip(self, load):
        module = load("storage.py")
        assert module.from_json(module.to_json(NOTES)) == NOTES


class TestFiles:
    def test_save_writes_json(self, load, tmp_path):
        path = tmp_path / "notes.json"
        load("storage.py").save(path, NOTES)
        assert path.exists(), "save() did not create the file."
        assert json.loads(path.read_text()) == NOTES, (
            "The file is there but does not contain the data as JSON."
        )

    def test_load_reads_it_back(self, load, tmp_path):
        path = tmp_path / "notes.json"
        path.write_text(json.dumps(NOTES))
        assert load("storage.py").load(path) == NOTES

    def test_load_with_no_file_gives_an_empty_list(self, load, tmp_path):
        result = load("storage.py").load(tmp_path / "never_saved.json")
        assert result == [], (
            "The first time a program runs there is no file yet. That is not an "
            "error - it means there is nothing saved, which is []."
        )

    def test_save_replaces_what_was_there(self, load, tmp_path):
        module = load("storage.py")
        path = tmp_path / "notes.json"
        module.save(path, NOTES)
        module.save(path, [])
        assert module.load(path) == []

    def test_accepts_a_plain_string_path(self, load, tmp_path):
        module = load("storage.py")
        path = str(tmp_path / "notes.json")
        module.save(path, NOTES)
        assert module.load(path) == NOTES
