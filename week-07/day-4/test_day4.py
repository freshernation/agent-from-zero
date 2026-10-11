"""Week 7, Day 4 - retries and budgets.

Run me:  pytest week-07/day-4 -v
"""

import pytest

from llm import FakeModel, ModelError, say, use

ASK = [{"role": "user", "content": "hi"}]


def busy():
    return ModelError("rate limited", retryable=True)


@pytest.fixture
def waits():
    return []


@pytest.fixture
def wait(waits):
    def record(seconds):
        waits.append(seconds)
    return record


@pytest.fixture
def retry(load):
    return load("retry.py").call_with_retry


@pytest.fixture
def run_agent(load):
    return load("agent.py").run_agent


@pytest.fixture
def kit(load):
    return load("kit.py")


class TestRetry:
    def test_no_failure_no_waiting(self, retry, wait, waits):
        model = FakeModel([say("Hi.")])
        assert retry(model, ASK, wait=wait)["text"] == "Hi."
        assert waits == []

    def test_passes_everything_through(self, retry, wait):
        model = FakeModel([say("Hi.")])
        retry(model, ASK, system="Be brief.", tools=[], wait=wait)
        assert model.requests[0]["system"] == "Be brief."
        assert model.requests[0]["tools"] == []

    def test_one_blip(self, retry, wait, waits):
        model = FakeModel([busy(), say("Hi.")])
        assert retry(model, ASK, wait=wait)["text"] == "Hi."
        assert waits == [1]

    def test_backs_off(self, retry, wait, waits):
        model = FakeModel([busy(), busy(), busy(), say("Hi.")])
        assert retry(model, ASK, retries=3, wait=wait)["text"] == "Hi."
        assert waits == [1, 2, 4], "Wait longer each time: 2 ** attempt."

    def test_gives_up_after_the_retries(self, retry, wait, waits):
        model = FakeModel([busy(), busy(), busy(), say("never reached")])
        with pytest.raises(ModelError):
            retry(model, ASK, retries=2, wait=wait)
        assert model.call_count == 3, "retries=2 means three attempts in all."
        assert waits == [1, 2], "Do not wait after the last attempt."

    def test_a_permanent_failure_is_not_retried(self, retry, wait, waits):
        model = FakeModel([ModelError("bad key"), say("never reached")])
        with pytest.raises(ModelError):
            retry(model, ASK, wait=wait)
        assert model.call_count == 1
        assert waits == []

    def test_no_retries_at_all(self, retry, wait):
        model = FakeModel([busy(), say("never reached")])
        with pytest.raises(ModelError):
            retry(model, ASK, retries=0, wait=wait)
        assert model.call_count == 1


class TestAgentRetries:
    def test_a_blip_does_not_end_the_run(self, run_agent, kit, wait, waits):
        model = FakeModel([use("list_titles"), busy(), say("None.")])
        result = run_agent(model, "Notes?", kit.SCHEMAS, kit.TOOLS, wait=wait)
        assert result["stopped"] == "done"
        assert result["steps"] == 2, "A failed attempt is not a step."
        assert waits == [1]

    def test_a_long_outage_does(self, run_agent, kit, wait):
        model = FakeModel([busy(), busy(), busy()])
        result = run_agent(model, "Notes?", kit.SCHEMAS, kit.TOOLS, retries=2, wait=wait)
        assert result["stopped"] == "error"
        assert result["answer"] == "The model is unavailable: rate limited"

    def test_a_permanent_failure_ends_it_at_once(self, run_agent, kit, wait, waits):
        model = FakeModel([ModelError("bad key")])
        result = run_agent(model, "Notes?", kit.SCHEMAS, kit.TOOLS, wait=wait)
        assert result["stopped"] == "error"
        assert waits == []


class TestBudget:
    def script(self):
        return [use("calculate", {"expression": f"{n} + 1"}, id=f"c{n}",
                    input=100, output=20) for n in range(8)]

    def test_stops_when_over(self, run_agent, kit, wait):
        model = FakeModel(self.script())
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS, token_budget=300, wait=wait)
        assert result["stopped"] == "budget"
        assert result["answer"] == "I reached my token budget before finishing."
        assert model.call_count == 3, (
            "120 tokens a step: after 3 steps the total is 360, which is over 300."
        )
        assert result["trace"][-1] == {"step": 3, "kind": "stop", "reason": "budget"}

    def test_does_not_run_the_tools_of_the_step_that_broke_it(self, run_agent, kit, wait):
        model = FakeModel(self.script())
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS, token_budget=300, wait=wait)
        ran = [m for m in result["messages"] if m["role"] == "tool"]
        assert len(ran) == 2

    def test_an_answer_already_paid_for_is_returned(self, run_agent, kit, wait):
        model = FakeModel([say("Paris.", input=900, output=100)])
        result = run_agent(model, "Capital?", kit.SCHEMAS, kit.TOOLS, token_budget=50, wait=wait)
        assert result["stopped"] == "done"
        assert result["answer"] == "Paris."

    def test_exactly_on_budget_carries_on(self, run_agent, kit, wait):
        model = FakeModel([use("list_titles", input=100, output=20), say("None.", input=1, output=1)])
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS, token_budget=120, wait=wait)
        assert result["stopped"] == "done"

    def test_no_budget_means_no_limit(self, run_agent, kit, wait):
        model = FakeModel(self.script())
        result = run_agent(model, "Go.", kit.SCHEMAS, kit.TOOLS, max_steps=5, wait=wait)
        assert result["stopped"] == "max_steps"
