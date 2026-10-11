# read_notes(path) should return the list of notes stored in that JSON file.
import json


def read_notes(path):
    return json.loads(str(path))
