"""Keep every test's notes and memory in their own throwaway files."""

import pytest


@pytest.fixture(autouse=True)
def notes_file(tmp_path, monkeypatch):
    path = tmp_path / "notes.json"
    monkeypatch.setenv("NOTES_FILE", str(path))
    return path


@pytest.fixture(autouse=True)
def memory_file(tmp_path, monkeypatch):
    path = tmp_path / "memory.json"
    monkeypatch.setenv("MEMORY_FILE", str(path))
    return path
