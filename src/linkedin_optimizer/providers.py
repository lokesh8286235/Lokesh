from os import getenv
from typing import Protocol


class RecommendationProvider(Protocol):
    def recommend(self, prompt: str) -> str: ...


class OpenAIProvider:
    """Optional OpenAI adapter; credentials stay in the environment."""

    def __init__(self, model: str = "gpt-5.6-luna") -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install the openai extra first.") from exc
        self._client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        self._model = model

    def recommend(self, prompt: str) -> str:
        response = self._client.responses.create(model=self._model, input=prompt)
        return response.output_text


class AnthropicProvider:
    """Optional Anthropic adapter; credentials stay in the environment."""

    def __init__(self, model: str = "claude-3-5-haiku-latest") -> None:
        try:
            from anthropic import Anthropic
        except ImportError as exc:
            raise RuntimeError("Install the anthropic extra first.") from exc
        self._client = Anthropic(api_key=getenv("ANTHROPIC_API_KEY"))
        self._model = model

    def recommend(self, prompt: str) -> str:
        message = self._client.messages.create(
            model=self._model,
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in message.content if hasattr(block, "text"))
