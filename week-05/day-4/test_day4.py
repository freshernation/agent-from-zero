"""Week 5, Day 4 - tool calls in two dialects.

Run me:  pytest week-05/day-4 -v
"""

SCHEMA = {
    "name": "calculate",
    "description": "Evaluate arithmetic.",
    "parameters": {
        "type": "object",
        "properties": {"expression": {"type": "string", "description": "the sum"}},
        "required": ["expression"],
    },
}

CLAUDE_RAW = {
    "content": [
        {"type": "thinking", "thinking": "", "signature": "x"},
        {"type": "text", "text": "Let me work that out."},
        {"type": "tool_use", "id": "toolu_01A", "name": "calculate",
         "input": {"expression": "17 * 23"}},
        {"type": "tool_use", "id": "toolu_01B", "name": "list_titles", "input": {}},
    ],
    "stop_reason": "tool_use",
}

OPENAI_RAW = {
    "choices": [{
        "message": {
            "content": None,
            "tool_calls": [
                {"id": "call_a", "type": "function",
                 "function": {"name": "calculate",
                              "arguments": '{"expression": "17 * 23"}'}},
                {"id": "call_b", "type": "function",
                 "function": {"name": "list_titles", "arguments": "{}"}},
            ],
        },
        "finish_reason": "tool_calls",
    }],
}

TOOL_MESSAGES = [
    {"role": "tool", "tool_call_id": "id_1", "content": "391"},
    {"role": "tool", "tool_call_id": "id_2", "content": "No notes yet."},
]


class TestSchemas:
    def test_claude(self, load):
        assert load("tool_dialects.py").claude_tool(SCHEMA) == {
            "name": "calculate",
            "description": "Evaluate arithmetic.",
            "input_schema": SCHEMA["parameters"],
        }

    def test_openai(self, load):
        assert load("tool_dialects.py").openai_tool(SCHEMA) == {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Evaluate arithmetic.",
                "parameters": SCHEMA["parameters"],
            },
        }


class TestCalls:
    def test_claude(self, load):
        assert load("tool_dialects.py").claude_calls(CLAUDE_RAW) == [
            {"id": "toolu_01A", "name": "calculate", "args": {"expression": "17 * 23"}},
            {"id": "toolu_01B", "name": "list_titles", "args": {}},
        ]

    def test_claude_with_no_calls(self, load):
        raw = {"content": [{"type": "text", "text": "Paris."}], "stop_reason": "end_turn"}
        assert load("tool_dialects.py").claude_calls(raw) == []

    def test_openai_parses_the_argument_string(self, load):
        calls = load("tool_dialects.py").openai_calls(OPENAI_RAW)
        assert calls == [
            {"id": "call_a", "name": "calculate", "args": {"expression": "17 * 23"}},
            {"id": "call_b", "name": "list_titles", "args": {}},
        ], (
            "OpenAI sends arguments as a STRING of JSON. args must be the parsed "
            "dictionary."
        )

    def test_openai_with_no_calls(self, load):
        module = load("tool_dialects.py")
        none = {"choices": [{"message": {"content": "Paris.", "tool_calls": None}}]}
        missing = {"choices": [{"message": {"content": "Paris."}}]}
        assert module.openai_calls(none) == []
        assert module.openai_calls(missing) == []

    def test_openai_arguments_that_do_not_parse(self, load):
        raw = {"choices": [{"message": {"content": None, "tool_calls": [
            {"id": "call_a", "type": "function",
             "function": {"name": "calculate", "arguments": '{"expression": "17'}},
        ]}}]}
        assert load("tool_dialects.py").openai_calls(raw) == [
            {"id": "call_a", "name": "calculate", "args": {}},
        ]


class TestResults:
    def test_claude_shares_one_user_message(self, load):
        assert load("tool_dialects.py").claude_results(TOOL_MESSAGES) == {
            "role": "user",
            "content": [
                {"type": "tool_result", "tool_use_id": "id_1", "content": "391"},
                {"type": "tool_result", "tool_use_id": "id_2", "content": "No notes yet."},
            ],
        }

    def test_openai_sends_one_each(self, load):
        assert load("tool_dialects.py").openai_results(TOOL_MESSAGES) == [
            {"role": "tool", "tool_call_id": "id_1", "content": "391"},
            {"role": "tool", "tool_call_id": "id_2", "content": "No notes yet."},
        ]
