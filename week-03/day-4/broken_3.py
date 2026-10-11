# write_notes(path, notes) should save the notes so that json.loads can read
# the file back.
from pathlib import Path


def write_notes(path, notes):
    Path(path).write_text(str(notes))
