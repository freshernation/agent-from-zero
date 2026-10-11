"""Week 4, Day 4 - two providers, one idea.

Run me:  pytest week-04/day-4 -v
"""

import pytest

MESSAGES = [{"role": "user", "content": "Capital of Peru?"}]

CLAUDE_RAW = {
    "content": [
        {"type": "thinking", "thinking": "", "signature": "EqQB"},
        {"type": "text", "text": "Lima."},
    ],
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 14, "output_tokens": 3},
}

OPENAI_RAW = {
    "choices": [
        {"message": {"role": "assistant", "content": "Lima."}, "finish_reason": "stop"},
    ],
    "usage": {"prompt_tokens": 14, "completion_tokens": 3},
}


class TestRequests:
    def test_claude_with_a_system_prompt(self, load):
        body = load("dialects.py").claude_request("claude-opus-5-5", MESSAGES, "One word.")
        assert body == {
            "model": "claude-opus-5-5",
            "max_tokens": 1024,
            "system": "One word.",
            "messages": MESSAGES,
        }

    def test_claude_without_one(self, load):
        body = load("dialects.py").claude_request("claude-opus-5-5", MESSAGES)
        assert "system" not in body, "With no system prompt, leave the key out."

    def test_claude_max_tokens(self, load):
        body = load("dialects.py").claude_request("m", MESSAGES, max_tokens=50)
        assert body["max_tokens"] == 50

    def test_openai_puts_the_system_prompt_first(self, load):
        body = load("dialects.py").openai_request("gpt-5-mini", MESSAGES, "One word.")
        assert body == {
            "model": "gpt-5-mini",
            "messages": [
                {"role": "system", "content": "One word."},
                {"role": "user", "content": "Capital of Peru?"},
            ],
        }

    def test_openai_without_one(self, load):
        body = load("dialects.py").openai_request("gpt-5-mini", MESSAGES)
        assert body["messages"] == MESSAGES

    def test_openai_leaves_your_list_alone(self, load):
        messages = [{"role": "user", "content": "hi"}]
        load("dialects.py").openai_request("gpt-5-mini", messages, "One word.")
        assert messages == [{"role": "user", "content": "hi"}], (
            "The caller's list now starts with a system message. Build a new list."
        )


class TestText:
    def test_claude_skips_blocks_that_are_not_text(self, load):
        assert load("dialects.py").claude_text(CLAUDE_RAW) == "Lima."

    def test_claude_joins_several_text_blocks(self, load):
        raw = {"content": [{"type": "text", "text": "Li"}, {"type": "text", "text": "ma."}]}
        assert load("dialects.py").claude_text(raw) == "Lima."

    def test_claude_with_no_text_at_all(self, load):
        raw = {"content": [{"type": "thinking", "thinking": "", "signature": "x"}]}
        assert load("dialects.py").claude_text(raw) == ""

    def test_openai(self, load):
        assert load("dialects.py").openai_text(OPENAI_RAW) == "Lima."

    def test_openai_content_can_be_none(self, load):
        raw = {"choices": [{"message": {"content": None}, "finish_reason": "stop"}]}
        assert load("dialects.py").openai_text(raw) == ""


class TestStop:
    @pytest.mark.parametrize("theirs,ours", [
        ("end_turn", "done"), ("max_tokens", "length"), ("refusal", "refused"),
        ("stop_sequence", "done"),
    ])
    def test_claude(self, load, theirs, ours):
        raw = {**CLAUDE_RAW, "stop_reason": theirs}
        assert load("dialects.py").neutral_stop("claude", raw) == ours

    @pytest.mark.parametrize("theirs,ours", [
        ("stop", "done"), ("length", "length"), ("content_filter", "refused"),
    ])
    def test_openai(self, load, theirs, ours):
        raw = {"choices": [{"message": {"content": "x"}, "finish_reason": theirs}]}
        assert load("dialects.py").neutral_stop("openai", raw) == ours


class TestUsage:
    def test_claude(self, load):
        assert load("dialects.py").neutral_usage("claude", CLAUDE_RAW) == {
            "input": 14, "output": 3,
        }

    def test_openai(self, load):
        assert load("dialects.py").neutral_usage("openai", OPENAI_RAW) == {
            "input": 14, "output": 3,
        }
