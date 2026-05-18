"""S — Single Responsibility: only generates negotiation suggestions."""
from agent.nodes.base import BaseNode
from agent.state import ContractState


class NegotiationAdvisorNode(BaseNode):

    PROMPT = """You are an expert contract negotiator. Suggest professional rewrites for risky clauses.

CONTRACT TYPE: {contract_type}

RISKY CLAUSES:
{risks}

Return ONLY valid JSON:
{{
  "suggestions": [
    {{
      "clause_title": "exact title",
      "issue": "what is problematic (1 sentence)",
      "suggested_rewrite": "improved clause text (2-4 sentences)",
      "negotiation_tip": "practical tip (1 sentence)"
    }}
  ]
}}"""

    def run(self, state: ContractState) -> dict:
        targets = [r for r in state["risks"] if r.get("risk_level") in ("HIGH", "MEDIUM")][:6]
        if not targets:
            return {"suggestions": [], "logs": ["✅ No risky clauses to renegotiate"]}

        risk_text = "\n".join(
            f"[{r['clause_title']}] ({r['risk_level']}): {r['reason']}"
            for r in targets
        )
        try:
            data = self._llm.complete_json(
                self.PROMPT.format(
                    contract_type=state["contract_type"],
                    risks=risk_text
                ),
                max_tokens=2000
            )
            suggestions = data.get("suggestions", [])
            return {
                "suggestions": suggestions,
                "logs": [f"💡 {len(suggestions)} negotiation suggestions generated"]
            }
        except Exception as e:
            return {"suggestions": [], "logs": [f"⚠️ Advisor error: {e}"]}
