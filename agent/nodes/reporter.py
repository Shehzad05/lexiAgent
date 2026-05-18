"""S — Single Responsibility: only generates the final executive report."""
from agent.nodes.base import BaseNode
from agent.state import ContractState


class ReportGeneratorNode(BaseNode):

    PROMPT = """You are a senior legal analyst. Write a professional contract review report.

CONTRACT:
- Type: {contract_type}
- Parties: {parties}
- Dates: {effective_date} → {expiry_date}
- Risk Score: {score}/100

RISKS:
{risks}

SUGGESTIONS:
{suggestions}

Write a clear report with these sections:
1. Executive Summary (3-4 sentences)
2. Contract Overview
3. Risk Assessment (by severity)
4. Recommended Actions (numbered)
5. Negotiation Priorities

Tone: professional but accessible to non-lawyers. Max 500 words."""

    def run(self, state: ContractState) -> dict:
        risk_text = "\n".join(
            f"- [{r['risk_level']}] {r['clause_title']}: {r['reason']}"
            for r in state["risks"]
        )
        sugg_text = "\n".join(
            f"- {s['clause_title']}: {s['issue']} → {s['suggested_rewrite'][:150]}"
            for s in state["suggestions"]
        )
        report = self._llm.complete(
            self.PROMPT.format(
                contract_type=state["contract_type"],
                parties=", ".join(state["parties"]),
                effective_date=state["effective_date"],
                expiry_date=state["expiry_date"],
                score=state["overall_risk_score"],
                risks=risk_text,
                suggestions=sugg_text,
            ),
            max_tokens=1200
        )
        return {
            "final_report": report,
            "logs": ["📋 Executive report generated"]
        }
