"""
SOLID: 
  S — only handles Claude API calls
  I — exposes only what nodes need: complete() and complete_json()
  D — nodes depend on this abstraction, not on anthropic SDK directly
"""
from __future__ import annotations
import json, re
from abc import ABC, abstractmethod
import anthropic
from config import settings

# ── Abstract interface (Dependency Inversion) ─────────────────────────────────
class LLMClient(ABC):
    @abstractmethod
    def complete(self, prompt: str, max_tokens: int = 1500) -> str: ...

    @abstractmethod
    def complete_json(self, prompt: str, max_tokens: int = 1500) -> dict | list: ...


# ── Concrete implementation ───────────────────────────────────────────────────
class ClaudeClient(LLMClient):
    MODEL = "claude-sonnet-4-20250514"

    def __init__(self, api_key: str | None = None):
        self._client = anthropic.Anthropic(api_key=api_key or settings.anthropic_api_key)

    def complete(self, prompt: str, max_tokens: int = 1500) -> str:
        msg = self._client.messages.create(
            model=self.MODEL,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text.strip()

    def complete_json(self, prompt: str, max_tokens: int = 1500) -> dict | list:
        raw = self.complete(prompt, max_tokens)
        clean = re.sub(r"```json|```", "", raw).strip()
        return json.loads(clean)


# ── Singleton factory ─────────────────────────────────────────────────────────
_client: ClaudeClient | None = None

def get_claude_client() -> ClaudeClient:
    global _client
    if _client is None:
        _client = ClaudeClient()
    return _client
