"""OpenAI, behind the course's neutral chat() interface.

Needs OPENAI_API_KEY in your environment (or .env). Set AGENT_OPENAI_MODEL to
choose the model.
"""

import os

from llm.fake import ModelError
from llm.wire import openai_input, openai_messages, openai_reply, openai_tool

DEFAULT_MODEL = "gpt-5-mini"


class OpenAIModel:
    def __init__(self, model=None, client=None):
        if client is None:
            import openai
            client = openai.OpenAI()
        self._client = client
        self.name = model or os.environ.get("AGENT_OPENAI_MODEL") or DEFAULT_MODEL

    def chat(self, messages, system=None, tools=None, max_tokens=None):
        request = {
            "model": self.name,
            "messages": openai_messages(messages, system),
        }
        if tools:
            request["tools"] = [openai_tool(schema) for schema in tools]
        if max_tokens:
            request["max_completion_tokens"] = max_tokens

        return openai_reply(self._send(request))

    def count_tokens(self, messages, system=None, tools=None):
        """How many input tokens this exact request would be, counted by OpenAI.

        OpenAI's counter speaks its Responses API, so the conversation is sent in
        that shape (llm/wire.py, openai_input) - the count is for the same content.
        """
        import openai

        request = {"model": self.name, "input": openai_input(messages)}
        if system:
            request["instructions"] = system
        if tools:
            request["tools"] = [{"type": "function", "name": s["name"], "description": s["description"],
                                 "parameters": s["parameters"]} for s in tools]
        try:
            return self._client.responses.input_tokens.count(**request).input_tokens
        except openai.APIError as error:
            raise ModelError(f"OpenAI could not count the tokens: {error}") from error

    def _send(self, request):
        import openai

        try:
            return self._client.chat.completions.create(**request)
        except openai.AuthenticationError as error:
            raise ModelError(
                "OpenAI rejected the API key. Check OPENAI_API_KEY in .env."
            ) from error
        except openai.RateLimitError as error:
            raise ModelError("OpenAI is rate-limiting you.", retryable=True) from error
        except openai.BadRequestError as error:
            raise ModelError(f"OpenAI rejected the request: {error.message}") from error
        except openai.APIStatusError as error:
            raise ModelError(
                f"OpenAI returned an error ({error.status_code}): {error.message}",
                retryable=error.status_code >= 500,
            ) from error
        except openai.APIConnectionError as error:
            raise ModelError("Could not reach OpenAI.", retryable=True) from error
