"""Week 6, Day 3 - an agent that survives.

Run me:  pytest week-06/day-3 -v
"""

import pytest

from llm import FakeModel, ModelError, say, use


@pytest.fixture
def run_agent(load):
    return load("agent.py").run_agent


@pytest.fixture
def kit(load):
    return load("kit.py")


def call(name, args):
    return {"id": "x", "name": name, "args": args}


class TestGuards:
    def test_same_call_same_signature(self, load):
        module = load("guards.py")
        assert module.signature(call("add_note", {"title": "a", "body": "b"})) == (
            module.signature(call("add_note", {"body": "b", "title": "a"}))
        ), "The same arguments in a different order are the same call. sort_keys=True."

    def test_signature_ignores_the_id(self, load):
        module = load("guards.py")
        first = {"id": "call_1", "name": "list_titles", "args": {}}
        second = {"id": "call_2", "name": "list_titles", "args": {}}
        assert module.signature(first) == module.signature(second)

    def test_different_calls_differ(self, load):
        module = load("guards.py")
        base = module.signature(call("calculate", {"expression": "1 + 1"}))
        assert base != module.signature(call("calculate", {"expression": "2 + 2"}))
        assert base != module.signature(call("find_notes", {"expression": "1 + 1"}))
        assert isinstance(base, str)

    @pytest.mark.parametrize("signatures,limit,answer", [
        ([], 3, False),
        (["a"], 3, False),
        (["a", "a"], 3, False),
        (["a", "a", "a"], 3, True),
        (["a", "b", "a", "c", "a"], 3, True),
        (["a", "a", "a", "b"], 3, False),
        (["a", "a"], 2, True),
    ])
    def test_is_repeating(self, load, signatures, limit, answer):
        assert load("guards.py").is_repeating(signatures, limit) is answer

    def test_clip_leaves_short_text_alone(self, load):
        module = load("guards.py")
        assert module.clip("hello") == "hello"
        assert module.clip("x" * 2000) == "x" * 2000

    def test_clip_cuts_and_says_so(self, load):
        result = load("guards.py").clip("x" * 5000)
        assert result == "x" * 2000 + "... [3000 more characters cut]"

    def test_clip_with_its_own_limit(self, load):
        assert load("guards.py").clip("abcdefghij", limit=4) == (
            "abcd... [6 more characters cut]"
        )


class TestToolFailuresAreInformation:
    def test_the_model_sees_the_error_and_carries_on(self, run_agent, kit):
        model = FakeModel([
            use("find_notes", {}),
            use("find_notes", {"word": "rent"}, id="call_2"),
            say("You have no note about rent."),
        ])
        result = run_agent(model, "Anything about rent?", kit.SCHEMAS, kit.TOOLS)
        assert result["stopped"] == "done"
        assert result["messages"][2]["content"].startswith("Error: TypeError:")
        assert result["steps"] == 3

    def test_an_invented_tool(self, run_agent, kit):
        model = FakeModel([use("send_email", {"to": "sam"}), say("I cannot email.")])
        result = run_agent(model, "Email Sam.", kit.SCHEMAS, kit.TOOLS)
        assert result["answer"] == "I cannot email."


class TestRepeating:
    def test_stops_on_the_third_identical_call(self, run_agent, kit):
        model = FakeModel([use("list_titles", id=f"c{n}") for n in range(12)])
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS)
        assert result["stopped"] == "repeating"
        assert result["answer"] == "I kept repeating the same step, so I stopped."
        assert model.call_count == 3, (
            f"The model was called {model.call_count} times. With repeat_limit=3 "
            "the run should end the third time the same call arrives."
        )

    def test_does_not_run_the_tool_a_third_time(self, run_agent, kit):
        model = FakeModel([use("list_titles", id=f"c{n}") for n in range(12)])
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS)
        ran = [m for m in result["messages"] if m["role"] == "tool"]
        assert len(ran) == 2, "Check for repeating BEFORE running the tools."

    def test_argument_order_does_not_hide_a_repeat(self, run_agent, kit):
        model = FakeModel([
            use("add_note", {"title": "a", "body": "b"}, id="c1"),
            use("add_note", {"body": "b", "title": "a"}, id="c2"),
            use("add_note", {"title": "a", "body": "b"}, id="c3"),
            say("never reached"),
        ])
        assert run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS)["stopped"] == "repeating"

    def test_different_arguments_are_not_a_repeat(self, run_agent, kit):
        model = FakeModel(
            [use("calculate", {"expression": f"{n} + 1"}, id=f"c{n}") for n in range(5)]
            + [say("Done.")]
        )
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS)
        assert result["stopped"] == "done"
        assert result["steps"] == 6

    def test_its_own_limit(self, run_agent, kit):
        model = FakeModel([use("list_titles", id=f"c{n}") for n in range(12)])
        run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS, repeat_limit=5)
        assert model.call_count == 5

    def test_the_cap_still_works(self, run_agent, kit):
        model = FakeModel(
            [use("calculate", {"expression": f"{n} + 1"}, id=f"c{n}") for n in range(30)]
        )
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS, max_steps=4)
        assert result["stopped"] == "max_steps"
        assert model.call_count == 4


class TestBigResults:
    def test_clipped_before_the_model_sees_them(self, run_agent):
        def read_file():
            return "x" * 5000

        model = FakeModel([use("read_file"), say("Read it.")])
        result = run_agent(model, "Read.", [], {"read_file": read_file}, result_limit=100)
        content = result["messages"][2]["content"]
        assert content == "x" * 100 + "... [4900 more characters cut]"
        assert model.requests[1]["messages"][2]["content"] == content

    def test_clipped_in_the_trace_too(self, run_agent):
        def read_file():
            return "x" * 5000

        model = FakeModel([use("read_file"), say("Read it.")])
        result = run_agent(model, "Read.", [], {"read_file": read_file}, result_limit=100)
        assert len(result["trace"][1]["content"]) < 200


class TestOtherStops:
    def test_cut_off(self, run_agent, kit):
        model = FakeModel([say("The capital of France is", stop="length")])
        result = run_agent(model, "Capital?", kit.SCHEMAS, kit.TOOLS)
        assert result["stopped"] == "length"
        assert result["answer"] == "The capital of France is [cut off]"

    def test_refused(self, run_agent, kit):
        model = FakeModel([say("", stop="refused")])
        result = run_agent(model, "Something.", kit.SCHEMAS, kit.TOOLS)
        assert result["stopped"] == "refused"
        assert result["answer"] == "The model declined this request."

    def test_model_fails_on_the_first_call(self, run_agent, kit):
        model = FakeModel([ModelError("rate limited")])
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS)
        assert result["stopped"] == "error"
        assert result["answer"] == "The model is unavailable: rate limited"
        assert result["steps"] == 0

    def test_model_fails_mid_run(self, run_agent, kit):
        model = FakeModel([use("list_titles"), ModelError("down")])
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS)
        assert result["stopped"] == "error"
        assert result["steps"] == 1, "The failed call is not a step."
        assert len(result["messages"]) == 3, "Keep the work done before the failure."


class TestTheRecord:
    @pytest.mark.parametrize("script,reason", [
        ([say("x", stop="length")], "length"),
        ([say("", stop="refused")], "refused"),
        ([ModelError("down")], "error"),
        ([use("list_titles", id=f"c{n}") for n in range(5)], "repeating"),
    ])
    def test_every_early_ending_leaves_a_stop_event(self, run_agent, kit, script, reason):
        result = run_agent(FakeModel(script), "Go.", kit.SCHEMAS, kit.TOOLS)
        last = result["trace"][-1]
        assert last["kind"] == "stop" and last["reason"] == reason
        assert last["step"] == result["steps"]

    def test_a_normal_ending_does_not(self, run_agent, kit):
        result = run_agent(FakeModel([say("Hi.")]), "Go.", kit.SCHEMAS, kit.TOOLS)
        assert result["trace"][-1]["kind"] == "answer"

    def test_usage_survives_an_early_ending(self, run_agent, kit):
        model = FakeModel([use("list_titles", input=50, output=5), ModelError("down")])
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS)
        assert result["usage"] == {"input": 50, "output": 5}
