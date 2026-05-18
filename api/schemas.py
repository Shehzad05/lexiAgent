from pydantic import BaseModel
from typing import List, Optional

class RiskItem(BaseModel):
    clause_title: str
    risk_level:   str
    reason:       str

class Suggestion(BaseModel):
    clause_title:      str
    issue:             str
    suggested_rewrite: str
    negotiation_tip:   str

class ClauseItem(BaseModel):
    title:    str
    text:     str
    category: str

class AnalysisResult(BaseModel):
    filename:           str
    contract_type:      str
    parties:            List[str]
    effective_date:     str
    expiry_date:        str
    clauses:            List[ClauseItem]
    risks:              List[RiskItem]
    overall_risk_score: int
    suggestions:        List[Suggestion]
    final_report:       str

class SSEEvent(BaseModel):
    event: str
    data:  dict
