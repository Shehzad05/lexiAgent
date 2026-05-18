"""
S — only handles HTTP: parse request, call agent, stream response.
  Business logic lives in agent/, not here.
"""
import asyncio, json, io
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from agent.graph import run_agent, EMPTY_STATE
from agent.nodes import (
    DocumentLoaderNode, ContractParserNode,
    RiskAnalyzerNode, NegotiationAdvisorNode, ReportGeneratorNode,
)
from agent.edges import risk_router
from services.document_loader import load_document

router = APIRouter()

ALLOWED_EXT = {".pdf", ".docx", ".xlsx", ".pptx", ".html", ".txt"}
NODE_NAMES  = {1:"Document Loader", 2:"Contract Parser", 3:"Risk Analyzer",
               4:"Negotiation Advisor", 5:"Report Generator"}

def sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


@router.get("/health")
async def health():
    return {"status": "ok", "agent": "LexiAgent v1"}


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """Stream LangGraph pipeline progress via Server-Sent Events."""
    import os
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(400, f"Unsupported format: {ext}")

    contents = await file.read()
    loop = asyncio.get_event_loop()

    # Instantiate nodes fresh per request (thread-safe)
    loader  = DocumentLoaderNode()
    parser  = ContractParserNode()
    risk    = RiskAnalyzerNode()
    advisor = NegotiationAdvisorNode()
    reporter = ReportGeneratorNode()

    async def stream():
        state = {**EMPTY_STATE, "filename": file.filename}

        try:
            # Node 1
            yield sse("node_start", {"node": 1, "name": NODE_NAMES[1]})
            raw = await loop.run_in_executor(None, load_document, contents, file.filename)
            state["raw_text"] = raw
            await loop.run_in_executor(None, loader.run, state)
            yield sse("node_done",  {"node": 1, "chars": len(raw), "raw_text": raw[:50000]})
            yield sse("log", {"type":"ok","msg":f"Loaded {len(raw):,} chars via Docling"})

            # Node 2
            yield sse("node_start", {"node": 2, "name": NODE_NAMES[2]})
            parsed = await loop.run_in_executor(None, parser.run, state)
            state.update(parsed)
            yield sse("node_done", {"node": 2,
                "contract_type": state["contract_type"],
                "parties":       state["parties"],
                "effective_date":state["effective_date"],
                "expiry_date":   state["expiry_date"],
                "clause_count":  len(state["clauses"])})
            yield sse("log", {"type":"ok","msg":f"Parsed {len(state['clauses'])} clauses"})

            # Node 3
            yield sse("node_start", {"node": 3, "name": NODE_NAMES[3]})
            risks = await loop.run_in_executor(None, risk.run, state)
            state.update(risks)
            yield sse("node_done", {"node": 3,
                "overall_risk_score": state["overall_risk_score"],
                "risks": state["risks"],
                "reparse_needed": state["reparse_needed"]})
            yield sse("log", {"type":"warn" if state["overall_risk_score"]>60 else "ok",
                               "msg":f"Risk score: {state['overall_risk_score']}/100"})

            # Conditional edge
            route = risk_router(state)
            if route == "reparse":
                yield sse("conditional_edge", {"msg": "HIGH risk — re-parsing contract"})
                yield sse("log", {"type":"warn","msg":"↩ Conditional edge: deepening parse"})
                parsed2 = await loop.run_in_executor(None, parser.run, state)
                state.update(parsed2)
                risks2 = await loop.run_in_executor(None, risk.run, state)
                state.update(risks2)

            # Node 4
            yield sse("node_start", {"node": 4, "name": NODE_NAMES[4]})
            sugg = await loop.run_in_executor(None, advisor.run, state)
            state.update(sugg)
            yield sse("node_done", {"node": 4, "suggestions": state["suggestions"]})
            yield sse("log", {"type":"ok","msg":f"{len(state['suggestions'])} suggestions generated"})

            # Node 5
            yield sse("node_start", {"node": 5, "name": NODE_NAMES[5]})
            rep = await loop.run_in_executor(None, reporter.run, state)
            state.update(rep)
            yield sse("node_done", {"node": 5, "final_report": state["final_report"]})
            yield sse("log", {"type":"ok","msg":"Report generated"})

            # Done
            yield sse("complete", {
                "contract_type":      state["contract_type"],
                "parties":            state["parties"],
                "effective_date":     state["effective_date"],
                "expiry_date":        state["expiry_date"],
                "clauses":            state["clauses"],
                "risks":              state["risks"],
                "overall_risk_score": state["overall_risk_score"],
                "suggestions":        state["suggestions"],
                "final_report":       state["final_report"],
            })

        except Exception as e:
            yield sse("error", {"msg": str(e)})

    return StreamingResponse(stream(), media_type="text/event-stream")


# ── Chat endpoint ─────────────────────────────────────────────────────────────
from pydantic import BaseModel
from typing import List, Optional
from services.claude_client import get_claude_client

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    context: str
    history: List[ChatMessage] = []
    question: str

@router.post("/chat")
async def chat_with_contract(req: ChatRequest):
    """Chat with the analyzed contract using Claude."""
    loop = asyncio.get_event_loop()
    client = get_claude_client()

    # Build messages with history
    messages = []
    for msg in req.history[-6:]:  # last 6 messages for context
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": req.question})

    system_prompt = req.context

    def call_claude():
        import anthropic
        from config import settings
        c = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        resp = c.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            system=system_prompt,
            messages=messages
        )
        return resp.content[0].text.strip()

    answer = await loop.run_in_executor(None, call_claude)
    return {"answer": answer}