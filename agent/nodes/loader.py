"""S — Single Responsibility: only loads and validates the document."""
from agent.nodes.base import BaseNode
from agent.state import ContractState
from services.document_loader import load_document


class DocumentLoaderNode(BaseNode):

    def run(self, state: ContractState) -> dict:
        raw = state.get("raw_text", "")
        if not raw:
            raise ValueError("raw_text is empty — document could not be loaded")

        return {
            "logs": [f"📄 Loaded: {state['filename']} ({len(raw):,} chars)"]
        }
