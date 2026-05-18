"""
SOLID:
  O — Open for extension (new nodes), closed for modification
  L — Every node subclass is substitutable for BaseNode
  D — Nodes depend on LLMClient abstraction, not ClaudeClient directly
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from agent.state import ContractState
from services.claude_client import LLMClient, get_claude_client


class BaseNode(ABC):
    """All LangGraph nodes inherit from this. One job: implement `run()`."""

    def __init__(self, llm: LLMClient | None = None):
        self._llm = llm or get_claude_client()   # Dependency Injection

    @abstractmethod
    def run(self, state: ContractState) -> dict:
        """Process state and return a partial state update dict."""
        ...

    def __call__(self, state: ContractState, config: dict | None = None) -> dict:
        """LangGraph calls nodes as callables — this bridges to run()."""
        return self.run(state)
