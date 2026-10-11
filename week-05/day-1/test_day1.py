"""Week 5, Day 1 - tool schemas.

Run me:  pytest week-05/day-1 -v
"""

import pytest

from llm import FakeModel, say

EXPECTED = {
    "add_note": ({"title", "body"}, ["title"]),
    "list_titles": (set(), []),
    "find_notes": ({"word"}, ["word"]),
    "delete_note": ({"title"}, ["title"]),
    "calculate": ({"expression"}, ["expression"]),
}


@pytest.fixture
def schemas(load):
    return {schema["name"]: schema for schema in load("schemas.py").SCHEMAS}


def test_text_param(load):
    assert load("schemas.py").text_param("the thing") == {
        "type": "string", "description": "the thing",
    }


def test_make_schema(load):
    module = load("schemas.py")
    schema = module.make_schema(
        "calculate", "Evaluate arithmetic.",
        {"expression": module.text_param("the sum")}, ["expression"],
    )
    assert schema == {
        "name": "calculate",
        "description": "Evaluate arithmetic.",
        "parameters": {
            "type": "object",
            "properties": {"expression": {"type": "string", "description": "the sum"}},
            "required": ["expression"],
        },
    }


class TestTheFive:
    def test_names_and_order(self, load):
        names = [schema["name"] for schema in load("schemas.py").SCHEMAS]
        assert names == list(EXPECTED)

    @pytest.mark.parametrize("name", list(EXPECTED))
    def test_arguments_match_the_function(self, schemas, name):
        properties, required = EXPECTED[name]
        parameters = schemas[name]["parameters"]
        assert set(parameters["properties"]) == properties, (
            f"{name} should declare exactly {sorted(properties) or 'no arguments'}. "
            "The names must match the function in toolbox.py."
        )
        assert parameters["required"] == required, (
            f"{name}: required should be {required}."
        )

    @pytest.mark.parametrize("name", list(EXPECTED))
    def test_description_is_written(self, schemas, name):
        description = schemas[name]["description"]
        assert len(description.split()) >= 10, (
            f"The description for {name} is {description!r}. That description IS "
            "the prompt - it is the only thing the model knows about your "
            "function. Say what it does and when to use it."
        )

    @pytest.mark.parametrize("name", list(EXPECTED))
    def test_every_argument_is_described(self, schemas, name):
        for argument, spec in schemas[name]["parameters"]["properties"].items():
            assert spec.get("type") == "string"
            assert len(spec.get("description", "").split()) >= 3, (
                f"{name}.{argument} has no real description. Tell the model what "
                "to put there, with an example if it helps."
            )

    def test_delete_warns(self, schemas):
        description = schemas["delete_note"]["description"].lower()
        assert any(phrase in description for phrase in
                   ["cannot be undone", "can't be undone", "permanent", "irreversible"]), (
            "delete_note destroys something. Its description should say so - the "
            "model decides how careful to be from your words and nothing else."
        )

    def test_a_model_accepts_them(self, load):
        model = FakeModel([say("ok")])
        model.chat([{"role": "user", "content": "hi"}], tools=load("schemas.py").SCHEMAS)
