"""Keep every test's notes in its own throwaway file."""

import pytest


@pytest.fixture(autouse=True)
def notes_file(tmp_path, monkeypatch):
    path = tmp_path / "notes.json"
    monkeypatch.setenv("NOTES_FILE", str(path))
    return path
