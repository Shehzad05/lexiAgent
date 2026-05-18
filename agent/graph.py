"""
Builds and runs the LangGraph pipeline.
S — only wires the graph together, execution is separate.
"""
from langgraph.graph import StateGraph, END
from agent.state import ContractState
from agent.nodes import (
    DocumentLoaderNode,
    ContractParserNode,
    RiskAnalyzerNode,
    NegotiationAdvisorNode,
    ReportGeneratorNode,
)
from agent.edges import risk_router

# ── Instantiate nodes (Dependency Injection ready) ────────────────────────────
_loader   = DocumentLoaderNode()
_parser   = ContractParserNode()
_risk     = RiskAnalyzerNode()
_advisor  = NegotiationAdvisorNode()
_reporter = ReportGeneratorNode()


def build_graph():
    g = StateGraph(ContractState)

    g.add_node("loader",   _loader)
    g.add_node("parser",   _parser)
    g.add_node("risk",     _risk)
    g.add_node("advisor",  _advisor)
    g.add_node("reporter", _reporter)

    g.set_entry_point("loader")
    g.add_edge("loader",  "parser")
    g.add_edge("parser",  "risk")
    g.add_edge("advisor", "reporter")
    g.add_edge("reporter", END)

    g.add_conditional_edges(
        "risk", risk_router,
        {"reparse": "parser", "continue": "advisor"}
    )
    return g.compile()


_graph = build_graph()

EMPTY_STATE: ContractState = {
    "raw_text": "", "filename": "",
    "parties": [], "contract_type": "",
    "effective_date": "", "expiry_date": "",
    "clauses": [], "risks": [],
    "overall_risk_score": 0, "reparse_needed": False,
    "suggestions": [], "final_report": "",
    "report_path": None, "logs": [],
}


def run_agent(raw_text: str, filename: str) -> ContractState:
    """Run the full pipeline and return final state."""
    state = {**EMPTY_STATE, "raw_text": raw_text, "filename": filename}
    return _graph.invoke(state)
