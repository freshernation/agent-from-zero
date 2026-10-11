"""Keep every test's project data in its own throwaway files."""

import pytest


@pytest.fixture(autouse=True)
def data_file(tmp_path, monkeypatch):
    path = tmp_path / "data.json"
    monkeypatch.setenv("DATA_FILE", str(path))
    monkeypatch.setenv("NOTES_FILE", str(tmp_path / "notes.json"))
    monkeypatch.setenv("MEMORY_FILE", str(tmp_path / "memory.json"))
    return path
