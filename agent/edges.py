"""S — Single Responsibility: only defines routing logic between nodes."""
from agent.state import ContractState


def risk_router(state: ContractState) -> str:
    """
    After Node 3 (Risk Analyzer):
    - If score > 80 AND 3+ HIGH clauses → re-parse (loop back)
    - Otherwise → continue to Negotiation Advisor
    """
    if state.get("reparse_needed", False):
        return "reparse"
    return "continue"
