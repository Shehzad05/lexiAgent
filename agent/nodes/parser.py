"""S — Single Responsibility: only extracts structured info from contract text."""
from agent.nodes.base import BaseNode
from agent.state import ContractState


class ContractParserNode(BaseNode):

    PROMPT = """You are a legal expert. Extract structured info from this contract.
Return ONLY valid JSON — no markdown, no explanation:
{{
  "parties": ["Party A", "Party B"],
  "contract_type": "NDA | Service Agreement | Employment | etc.",
  "effective_date": "YYYY-MM-DD or null",
  "expiry_date": "YYYY-MM-DD or null",
  "clauses": [
    {{
      "title": "Clause name",
      "text": "First 300 chars of clause",
      "category": "payment|liability|termination|confidentiality|ip|dispute|other"
    }}
  ]
}}
Extract ALL significant clauses (min 5, max 15).

CONTRACT:
{text}"""

    def run(self, state: ContractState) -> dict:
        try:
            data = self._llm.complete_json(
                self.PROMPT.format(text=state["raw_text"][:6000]),
                max_tokens=2000
            )
            clauses = data.get("clauses", [])
            return {
                "parties":        data.get("parties", []),
                "contract_type":  data.get("contract_type", "Unknown"),
                "effective_date": data.get("effective_date") or "",
                "expiry_date":    data.get("expiry_date") or "",
                "clauses":        clauses,
                "logs": [f"✅ Parsed {len(clauses)} clauses — Type: {data.get('contract_type')}"]
            }
        except Exception as e:
            return {
                "parties": [], "contract_type": "Unknown",
                "effective_date": "", "expiry_date": "", "clauses": [],
                "logs": [f"⚠️ Parser error: {e}"]
            }
