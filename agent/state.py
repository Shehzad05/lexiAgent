from typing import TypedDict, List, Optional, Annotated
import operator

class ContractState(TypedDict):
    # Input
    raw_text:           str
    filename:           str
    # Node 2
    parties:            List[str]
    contract_type:      str
    effective_date:     str
    expiry_date:        str
    clauses:            List[dict]
    # Node 3
    risks:              List[dict]
    overall_risk_score: int
    reparse_needed:     bool
    # Node 4
    suggestions:        List[dict]
    # Node 5
    final_report:       str
    report_path:        Optional[str]
    # Logging
    logs:               Annotated[List[str], operator.add]
