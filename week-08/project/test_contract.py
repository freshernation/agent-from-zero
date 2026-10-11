"""Week 8 - the contract every capstone agent meets, whatever it is about.

Run me:  pytest week-08/project -v
Or one part:  pytest week-08/project -k Tools -v      (Spec, Tools, Agent, Evals, Docs)
"""

import inspect
from pathlib import Path

import pytest

from llm import FakeModel, say, use

HERE = Path(__file__).parent
TYPES = {"string": "", "number": 0, "integer": 0, "boolean": False}
KNOWN = {"stopped", "answer_contains", "calls", "never_calls", "max_steps", "state"}


def filled(name, minimum_words):
    text = (HERE / name).read_text()
    left = text.count("_(your answer")
    assert left == 0, f"{name} still has {left} unanswered section(s)."
    assert len(text.split()) >= minimum_words, (
        f"{name} is {len(text.split())} words. It needs at least {minimum_words}."
    )
    return text


def blank_args(schema):
    """The dullest legal arguments for a tool: '' for strings, 0 for numbers."""
    args = {}
    properties = schema["parameters"]["properties"]
    for name in schema["parameters"]["required"]:
        args[name] = TYPES[properties[name]["type"]]
    return args


def nothing(seconds):
    pass


@pytest.fixture
def tools(load):
    return load("tools.py")


@pytest.fixture
def app(load):
    return load("app.py")


class TestSpec:
    def test_the_spec_is_written(self):
        filled("SPEC.md", 150)


class TestTools:
    def test_at_least_four(self, tools):
        assert len(tools.SCHEMAS) >= 4

    def test_schemas_and_table_agree(self, tools):
        names = [schema["name"] for schema in tools.SCHEMAS]
        assert sorted(names) == sorted(tools.TOOLS), (
            "Every schema needs a function in TOOLS under the same name, and "
            "every function in TOOLS needs a schema."
        )
        for function in tools.TOOLS.values():
            assert callable(function)

    def test_a_model_accepts_the_schemas(self, tools):
        FakeModel(say("ok")).chat([{"role": "user", "content": "hi"}], tools=tools.SCHEMAS)

    def test_descriptions_are_written(self, tools):
        for schema in tools.SCHEMAS:
            assert len(schema["description"].split()) >= 12, (
                f"The description of {schema['name']} is too thin. Say what it "
                "does, when to use it, and when not to."
            )
            for name, spec in schema["parameters"]["properties"].items():
                assert spec.get("type") in TYPES, (
                    f"{schema['name']}.{name}: type must be one of {sorted(TYPES)}."
                )
                assert len(spec.get("description", "").split()) >= 3, (
                    f"{schema['name']}.{name} has no real description."
                )

    def test_schemas_match_the_functions(self, tools):
        for schema in tools.SCHEMAS:
            parameters = inspect.signature(tools.TOOLS[schema["name"]]).parameters
            declared = schema["parameters"]["properties"]
            assert set(declared) == set(parameters), (
                f"{schema['name']}: the schema declares {sorted(declared)} but the "
                f"function takes {sorted(parameters)}."
            )
            needed = [name for name, parameter in parameters.items()
                      if parameter.default is inspect.Parameter.empty]
            assert sorted(schema["parameters"]["required"]) == sorted(needed), (
                f"{schema['name']}: `required` should be exactly the arguments "
                f"with no default: {sorted(needed)}."
            )

    def test_reset_and_snapshot(self, tools, data_file):
        tools.reset(tools.EMPTY)
        assert tools.snapshot() == tools.EMPTY
        assert data_file.exists(), (
            "reset() did not write the file named by DATA_FILE. Read the "
            "environment variable inside the function, not at the top of the file."
        )

    def test_nonsense_never_crashes_a_tool(self, tools):
        tools.reset(tools.EMPTY)
        for schema in tools.SCHEMAS:
            result = tools.TOOLS[schema["name"]](**blank_args(schema))
            assert isinstance(result, str) and result.strip(), (
                f"{schema['name']} returned {result!r} for empty arguments. A tool "
                "returns a sentence, always."
            )

    def test_run_tool_never_raises(self, tools):
        def explode():
            raise RuntimeError("boom")

        assert tools.run_tool(tools.TOOLS, "no_such_tool", {}) == (
            "Error: unknown tool 'no_such_tool'"
        )
        assert tools.run_tool({"explode": explode}, "explode", {}) == (
            "Error: RuntimeError: boom"
        )
        first = tools.SCHEMAS[0]["name"]
        result = tools.run_tool(tools.TOOLS, first, {"no_such_argument": 1})
        assert result.startswith("Error: TypeError:")

    def test_dangerous_is_decided(self, tools):
        assert isinstance(tools.DANGEROUS, (set, frozenset))
        assert tools.DANGEROUS <= set(tools.TOOLS), (
            "DANGEROUS names a tool that is not in TOOLS."
        )

    def test_data_stays_in_the_data_file(self, tools):
        before = sorted(path.name for path in HERE.iterdir())
        tools.reset(tools.EMPTY)
        for schema in tools.SCHEMAS:
            tools.TOOLS[schema["name"]](**blank_args(schema))
        after = sorted(path.name for path in HERE.iterdir()
                       if path.name != "__pycache__")
        before = [name for name in before if name != "__pycache__"]
        assert after == before, (
            f"Running the tools created {sorted(set(after) - set(before))} in the "
            "project folder. All data belongs in the file named by DATA_FILE."
        )

    def test_you_wrote_your_own_tests(self, tools, source, run_tests_against):
        count = source("test_tools.py", code_only=True).count("def test_")
        assert count >= 6, f"test_tools.py has {count} test(s). Write at least six."
        outcome = run_tests_against("test_tools.py", {}, also_copy=["tools.py"])
        assert outcome.passed, "Your own tests fail:\n" + outcome.output


class TestAgent:
    def test_system_prompt(self, app):
        assert isinstance(app.SYSTEM, str) and len(app.SYSTEM.split()) >= 40

    def test_a_plain_turn(self, app):
        turn = app.take_turn(FakeModel([say("Hi.")]), [], "Hello", wait=nothing)
        assert turn["text"] == "Hi.\n(done, 1 steps)"
        assert [m["role"] for m in turn["history"]] == ["user", "assistant"]

    def test_offers_your_tools(self, app, tools):
        model = FakeModel([say("Hi.")])
        app.take_turn(model, [], "Hello", wait=nothing)
        offered = [schema["name"] for schema in model.requests[0]["tools"]]
        for schema in tools.SCHEMAS:
            assert schema["name"] in offered
        assert model.requests[0]["system"] == app.SYSTEM

    def test_a_tool_runs_end_to_end(self, app, tools):
        tools.reset(tools.EMPTY)
        safe = [s for s in tools.SCHEMAS if s["name"] not in tools.DANGEROUS][0]
        model = FakeModel([use(safe["name"], blank_args(safe)), say("Done.")])
        turn = app.take_turn(model, [], "Go.", wait=nothing)
        assert [m["role"] for m in turn["history"]] == [
            "user", "assistant", "tool", "assistant",
        ]

    def test_dangerous_tools_are_refused_without_a_yes(self, app, tools):
        if not tools.DANGEROUS:
            pytest.skip("No dangerous tools - SPEC.md must justify that.")
        tools.reset(tools.EMPTY)
        for schema in tools.SCHEMAS:
            if schema["name"] not in tools.DANGEROUS:
                continue
            model = FakeModel([use(schema["name"], blank_args(schema)), say("Not allowed.")])
            turn = app.take_turn(model, [], "Go.", wait=nothing)
            assert turn["history"][2]["content"].startswith("Refused:"), (
                f"{schema['name']} is in DANGEROUS but ran without approval."
            )

    def test_the_conversation_continues(self, app):
        model = FakeModel([say("One."), say("Two.")])
        first = app.take_turn(model, [], "first", wait=nothing)
        app.take_turn(model, first["history"], "second", wait=nothing)
        assert len(model.requests[1]["messages"]) == 3

    def test_the_program(self, run, tmp_path):
        r = run("app.py", answers=["hello", "quit"], env={"DATA_FILE": tmp_path / "d.json"})
        r.expect("(fake model) You said: hello")
        r.expect("Bye.")


class TestEvals:
    @pytest.fixture
    def cases(self, load):
        return load("cases.py").CASES

    def test_at_least_eight(self, cases):
        assert len(cases) >= 8

    def test_each_is_well_formed(self, cases):
        names = [case["name"] for case in cases]
        assert len(set(names)) == len(names), "Every case needs its own name."
        for case in cases:
            assert isinstance(case["task"], str) and case["task"].strip()
            assert case["expect"], f"{case['name']} expects nothing, so it cannot fail."
            unknown = set(case["expect"]) - KNOWN
            assert not unknown, f"{case['name']} uses unknown checks: {unknown}"

    def test_the_required_kinds(self, cases, tools):
        def start(case):
            return case.get("state", tools.EMPTY)

        with_state = [case for case in cases if "state" in case["expect"]]
        assert any(case["expect"]["state"] != start(case) for case in with_state), (
            "No case expects the data to CHANGE. Check the end state of at least "
            "one request that should alter something."
        )
        assert any(case["expect"]["state"] == start(case) and start(case) != tools.EMPTY
                   for case in with_state), (
            "No case starts from real data and expects it UNCHANGED - an "
            "impossible request, an injection, or an unapproved dangerous action."
        )
        assert any(case["expect"].get("never_calls") for case in cases), (
            "No case says what the agent must NOT do."
        )

    def test_check_understands_state(self, load):
        evals = load("evals.py")
        result = {"answer": "x", "stopped": "done", "steps": 1, "trace": []}
        assert evals.check(result, {"state": ["a"]}, ["a"]) == []
        assert evals.check(result, {"state": ["a"]}, ["b"]) == [
            "state: expected ['a'], got ['b']",
        ]

    def test_run_case_uses_your_data(self, load, tools):
        evals = load("evals.py")
        clean = {"name": "nothing happens", "task": "Hello.",
                 "expect": {"state": tools.EMPTY, "stopped": "done"}}
        outcome = evals.run_case(FakeModel(say("Hi.")), clean, tools.SCHEMAS, tools.TOOLS)
        assert outcome == {"name": "nothing happens", "passed": True,
                           "failures": [], "steps": 1}

        wrong = {"name": "impossible", "task": "Hello.",
                 "expect": {"state": "not what the data will be"}}
        outcome = evals.run_case(FakeModel(say("Hi.")), wrong, tools.SCHEMAS, tools.TOOLS)
        assert outcome["passed"] is False
        assert outcome["failures"][0].startswith("state: expected")

    def test_every_case_runs(self, cases, load, tools):
        evals = load("evals.py")
        for case in cases:
            outcome = evals.run_case(FakeModel(say("ok")), case, tools.SCHEMAS,
                                     tools.TOOLS, dangerous=tools.DANGEROUS)
            assert set(outcome) == {"name", "passed", "failures", "steps"}


class TestDocs:
    def test_the_eval_report(self):
        text = filled("EVAL_REPORT.md", 200)
        assert "(paste" not in text, "Paste the real output of run_evals.py."
        assert " passed" in text and ("PASS " in text or "FAIL " in text)

    def test_the_readme(self):
        text = filled("README.md", 250)
        assert "python" in text.lower(), "The README must show how to run it."
