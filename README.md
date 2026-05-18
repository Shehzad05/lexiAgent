# ⚖️ LexiAgent — AI Legal Expert

> **Autonomous AI agent that reads, analyzes, and advises on legal contracts — end to end. No lawyer needed.**

Built for **Milan AI Week 2026 — AI Agent Olympics Hackathon**

---

## 🎬 Demo

> Upload any contract → Watch the AI pipeline run → Get risk score, clause analysis, negotiation tips, and chat with your contract.

---

## ✨ What It Does

Most businesses sign contracts without fully understanding the risks. Lawyers are expensive ($200–500/hr). LexiAgent solves this:

1. **Upload** any contract (PDF, DOCX, and more)
2. **Agent pipeline** automatically extracts all clauses, parties, and dates
3. **Risk scoring** — every clause gets HIGH / MEDIUM / LOW risk rating
4. **Negotiation advice** — professional rewrites for risky clauses
5. **Executive report** — download as PDF or TXT
6. **Chat** — ask "Should I sign this?" and get a direct answer

**Fully autonomous. Zero human intervention required.**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     LexiAgent                           │
│                                                         │
│  Contract Upload (PDF/DOCX/XLSX/PPTX/HTML/TXT)         │
│         │                                               │
│         ▼                                               │
│  ┌─────────────┐                                        │
│  │  Node 01    │  Document Loader                       │
│  │             │  Multi-format reader                   │
│  └──────┬──────┘                                        │
│         │                                               │
│         ▼                                               │
│  ┌─────────────┐                                        │
│  │  Node 02    │  Contract Parser                       │
│  │             │  Extracts clauses · parties · dates    │
│  └──────┬──────┘                                        │
│         │                                               │
│         ▼                                               │
│  ┌─────────────┐                                        │
│  │  Node 03    │  Risk Analyzer                         │
│  │             │  Scores each clause 0–100              │
│  └──────┬──────┘                                        │
│         │                                               │
│    ┌────┴────┐  Conditional Edge                        │
│    │         │                                          │
│  score>80  score ok                                     │
│    │         │                                          │
│    └──► Re-parse ──► continue                           │
│                       │                                 │
│                       ▼                                 │
│              ┌─────────────┐                            │
│              │  Node 04    │  Negotiation Advisor        │
│              │             │  Rewrites risky clauses    │
│              └──────┬──────┘                            │
│                     │                                   │
│                     ▼                                   │
│              ┌─────────────┐                            │
│              │  Node 05    │  Report Generator          │
│              │             │  Full executive summary    │
│              └──────┬──────┘                            │
│                     │                                   │
│                     ▼                                   │
│         PDF Report + Chat Interface                     │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
lexiAgent/
│
├── main.py                     # Entry point — FastAPI app
├── config.py                   # Settings from .env
├── requirements.txt
├── .env.example                # Copy to .env and add your key
├── .gitignore
│
├── agent/                      # LangGraph pipeline
│   ├── graph.py                # Pipeline builder & runner
│   ├── state.py                # Shared ContractState TypedDict
│   ├── edges.py                # Conditional edge logic
│   └── nodes/
│       ├── base.py             # Abstract BaseNode (SOLID)
│       ├── loader.py           # Node 01: Document Loader
│       ├── parser.py           # Node 02: Contract Parser
│       ├── risk.py             # Node 03: Risk Analyzer
│       ├── advisor.py          # Node 04: Negotiation Advisor
│       └── reporter.py         # Node 05: Report Generator
│
├── services/                   # Business logic
│   ├── claude_client.py        # Claude API wrapper
│   └── document_loader.py      # Docling multi-format reader
│
├── api/                        # FastAPI layer
│   ├── routes.py               # SSE streaming + chat endpoints
│   └── schemas.py              # Pydantic models
│
└── ui/
    └── index.html              # Complete frontend (no framework needed)
```

---

## 🎯 Hackathon Criteria

| Criteria | How LexiAgent covers it |
|---|---|
| **Intelligent Reasoning** | AI independently evaluates every clause for legal risk — no human guidance |
| **Agentic Workflows** | LangGraph 5-node pipeline with conditional re-parse loop |
| **Enterprise Utility** | Saves businesses hours of expensive lawyer time |
| **Multimodal Intelligence** | Reads PDF, DOCX, XLSX, PPTX, HTML, TXT via Docling |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Reasoning | Claude Sonnet (Anthropic) |
| Agent Framework | LangGraph |
| Document Parsing | Docling |
| Backend | FastAPI + Python |
| Streaming | Server-Sent Events (SSE) |
| Frontend | Vanilla HTML/CSS/JS |

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/YOUR_USERNAME/lexiAgent.git
cd lexiAgent
pip install -r requirements.txt
```

### 2. Setup Environment
```bash
cp .env.example .env
# Open .env and add your Anthropic API key
```

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 3. Run
```bash
python main.py
```

### 4. Open Browser
```
http://localhost:8000
```

---

## 💡 SOLID Principles Applied

| Principle | Where |
|---|---|
| **S** — Single Responsibility | Each node does exactly one job |
| **O** — Open/Closed | `BaseNode` — extend without modifying |
| **L** — Liskov Substitution | Any node is substitutable for `BaseNode` |
| **I** — Interface Segregation | `LLMClient` exposes only what nodes need |
| **D** — Dependency Inversion | Nodes depend on `LLMClient` abstraction, not Claude SDK directly |

---

## 📄 Supported Formats

| Format | Extension |
|---|---|
| PDF | `.pdf` |
| Word Document | `.docx` |
| Excel | `.xlsx` |
| PowerPoint | `.pptx` |
| HTML | `.html` |
| Plain Text | `.txt` |

---

## 🏆 Built At

**Milan AI Week 2026 — AI Agent Olympics Hackathon**
Lablab.ai · May 2026

---

<div align="center">
  <b>⚖️ LexiAgent — Read contracts like a lawyer. For free.</b>
</div>
