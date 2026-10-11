"""Week 2 milestone - the notes toolkit.

Run me:  pytest week-02/milestone -v
"""

import pytest


@pytest.fixture
def notes():
    return [
        {"title": "milk", "body": "two litres, semi-skimmed"},
        {"title": "call the dentist", "body": "before Friday"},
    ]


class TestAddNote:
    def test_adds_and_confirms(self, load):
        notes = []
        assert load("notes.py").add_note(notes, "milk", "two litres") == "Saved 'milk'."
        assert notes == [{"title": "milk", "body": "two litres"}]

    @pytest.mark.parametrize("title", ["", "   "])
    def test_needs_a_title(self, load, title):
        notes = []
        assert load("notes.py").add_note(notes, title, "x") == "A note needs a title."
        assert notes == [], "A note with no title must not be added."

    @pytest.mark.parametrize("title", ["milk", "MILK", " Milk "])
    def test_refuses_a_duplicate(self, load, notes, title):
        result = load("notes.py").add_note(notes, title, "again")
        assert result == "There is already a note called 'milk'."
        assert len(notes) == 2

    def test_tidies_the_title(self, load):
        notes = []
        load("notes.py").add_note(notes, "  eggs ", "six")
        assert notes[0]["title"] == "eggs"


class TestListTitles:
    def test_numbered(self, load, notes):
        assert load("notes.py").list_titles(notes) == "1. milk\n2. call the dentist"

    def test_empty(self, load):
        assert load("notes.py").list_titles([]) == "No notes yet."


class TestFindNotes:
    def test_matches_the_title(self, load, notes):
        assert load("notes.py").find_notes(notes, "milk") == (
            "milk: two litres, semi-skimmed"
        )

    def test_matches_the_body(self, load, notes):
        assert load("notes.py").find_notes(notes, "friday") == (
            "call the dentist: before Friday"
        )

    def test_several_matches(self, load, notes):
        assert load("notes.py").find_notes(notes, "t") == (
            "milk: two litres, semi-skimmed\ncall the dentist: before Friday"
        )

    def test_nothing_matches(self, load, notes):
        assert load("notes.py").find_notes(notes, "cheese") == (
            "No notes mention 'cheese'."
        )


class TestDeleteNote:
    @pytest.mark.parametrize("title", ["milk", "Milk", "MILK"])
    def test_deletes(self, load, notes, title):
        assert load("notes.py").delete_note(notes, title) == "Deleted 'milk'."
        assert [note["title"] for note in notes] == ["call the dentist"]

    def test_no_such_note(self, load, notes):
        assert load("notes.py").delete_note(notes, "cheese") == (
            "No note called 'cheese'."
        )
        assert len(notes) == 2


class TestEveryAnswerIsASentence:
    def test_everything_returns_a_string(self, load, notes):
        module = load("notes.py")
        results = [
            module.add_note(notes, "eggs", "six"),
            module.add_note(notes, "", "x"),
            module.list_titles(notes),
            module.list_titles([]),
            module.find_notes(notes, "eggs"),
            module.find_notes(notes, "zzz"),
            module.delete_note(notes, "eggs"),
            module.delete_note(notes, "zzz"),
        ]
        for result in results:
            assert isinstance(result, str) and result, (
                f"A function returned {result!r}. Every function in this file "
                "returns a sentence - never a number, a list or None."
            )

    def test_nothing_prints(self, load, notes, capsys):
        module = load("notes.py")
        module.add_note(notes, "eggs", "six")
        module.list_titles(notes)
        module.find_notes(notes, "eggs")
        module.delete_note(notes, "eggs")
        assert capsys.readouterr().out == "", "Return the sentence; do not print it."
