"""S — Single Responsibility: only scores risk for each clause."""
from agent.nodes.base import BaseNode
from agent.state import ContractState


class RiskAnalyzerNode(BaseNode):

    PROMPT = """You are a contract risk specialist. Score each clause for legal and business risk.

CONTRACT TYPE: {contract_type}
PARTIES: {parties}

CLAUSES:
{clauses}

Return ONLY valid JSON:
{{
  "overall_risk_score": <0-100>,
  "risks": [
    {{
      "clause_title": "exact title",
      "risk_level": "HIGH" | "MEDIUM" | "LOW",
      "reason": "one sentence explanation"
    }}
  ]
}}

Flag HIGH: unlimited liability, broad IP assignment, non-compete over 1yr,
auto-renewal with short notice, missing dispute resolution."""

    def run(self, state: ContractState) -> dict:
        clauses_text = "\n".join(
            f"[{c['title']}] ({c['category']}): {c['text'][:250]}"
            for c in state["clauses"]
        )
        try:
            data = self._llm.complete_json(
                self.PROMPT.format(
                    contract_type=state["contract_type"],
                    parties=", ".join(state["parties"]),
                    clauses=clauses_text
                ),
                max_tokens=1500
            )
            score = max(0, min(100, int(data.get("overall_risk_score", 50))))
            risks = data.get("risks", [])
            high_count = sum(1 for r in risks if r.get("risk_level") == "HIGH")
            reparse = score > 80 and high_count >= 3

            return {
                "risks":              risks,
                "overall_risk_score": score,
                "reparse_needed":     reparse,
                "logs": [
                    f"⚠️ Risk score: {score}/100 | HIGH: {high_count}",
                    "🔄 Re-parse triggered" if reparse else "✅ Risk analysis done"
                ]
            }
        except Exception as e:
            return {
                "risks": [], "overall_risk_score": 50, "reparse_needed": False,
                "logs": [f"⚠️ Risk analyzer error: {e}"]
            }
