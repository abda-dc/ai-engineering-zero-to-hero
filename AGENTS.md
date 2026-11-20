# AI Engineering: Zero to Hero — Agent Operations & Standards

This document establishes architectural standards, environment guidelines, and mandatory quality gates for the `ai-engineering-zero to hero` repository.

---

## 1. Environment & Path Handling (Strict Windows Rules)

- **Directory Path with Spaces**: The workspace is located at `C:\Users\Kiya\Documents\ai-engineering-zero to hero`.
- **Mandatory Quoting**: Every path reference, Docker volume mount, PowerShell argument, and script invocation **MUST** be wrapped in double quotes:
  ```powershell
  # Correct
  cd "C:\Users\Kiya\Documents\ai-engineering-zero to hero"
  docker run -v "${PWD}:/workspace" ...
  python "scripts/sync_notebooks_to_app.py"

  # Prohibited
  cd C:\Users\Kiya\Documents\ai-engineering-zero to hero
  ```
- **Line Endings & Encoding**: UTF-8 without BOM, LF or CRLF standard.

---

## 2. Architecture Overview

```
ai-engineering-zero to hero/
├── AGENTS.md                          # Repository rules & autonomous gates
├── README.md                          # Master project documentation
├── docker-compose.yml                 # Multi-container orchestration (Postgres, Redis, Qdrant, Backend, Frontend)
├── .env.example                       # Environment variable templates
├── book/                              # Jupyter Book 2 (MyST Markdown) source
│   ├── myst.yml                       # MyST project configuration
│   ├── intro.md                       # Book introduction & learning roadmap
│   └── chapters/
│       ├── part1-foundations/         # Ch 00 - 02 (Python, Math, Classical ML)
│       ├── part2-core-genai/          # Ch 03 - 05 (GenAI, LLM Internals, Prompt/Context)
│       ├── part3-rag-data/            # Ch 06 - 08 (Vector DBs, Data Pipelines, Production RAG)
│       └── part4-agents-prod/         # Ch 09 - 12 (Agents, MCP, MLOps, Evals/Observability)
├── scripts/
│   └── sync_notebooks_to_app.py       # Parser converting notebooks & myst.yml to curriculum.json
└── app/
    ├── backend/                       # Python FastAPI Backend
    │   ├── main.py                    # API entrypoint (REST, streaming, MCP inspector)
    │   ├── requirements.txt           # Python dependencies
    │   ├── tests/                     # Pytest suite
    │   └── ...
    └── frontend/                      # Next.js App Router + TypeScript + Tailwind CSS
        ├── src/
        │   ├── app/                   # Pages: /, /chapters/[id], /studio
        │   ├── components/            # UI components (Dashboard, Reader, Studio labs)
        │   └── data/curriculum.json   # Synced curriculum JSON
        ├── package.json
        └── ...
```

---

## 3. Autonomous Verification Gates (Definition of Done)

All four gates must pass with zero errors before project completion.

### Gate 1: Jupyter Book 2 & Curriculum Sync
- All 13 chapters (`ch00` through `ch12`) implemented as valid, runnable `.ipynb` files.
- All 140 required concepts covered with rich Markdown, Mermaid diagrams, code cells, capstone lab, and self-check quiz.
- Zero paid API dependencies for code cells (local-first with graceful mock/CPU fallbacks).
- Book build passes via MyST / Jupyter Book.
- `python "scripts/sync_notebooks_to_app.py"` produces a schema-valid `app/frontend/src/data/curriculum.json`.

### Gate 2: Companion App Architecture & Code Quality
- FastAPI backend runs with zero startup crashes.
- Database fallback: PostgreSQL + pgvector primary, SQLite fallback for zero-Docker execution.
- Cache fallback: Redis primary, in-memory dict fallback.
- LLM inference: Local Ollama primary (`http://localhost:11434`), deterministic educational simulator fallback.
- MCP Server & Inspector endpoint operational.
- Frontend builds cleanly (`npm run build`) with zero TypeScript or ESLint errors.

### Gate 3: Interactive Studio & Verification
- Split-Screen AI Engineering Studio (`/studio`) features 4 functioning live tabs:
  1. Tokenizer & Embedding Explorer
  2. RAG Chunking & Hybrid Retrieval Debugger
  3. LangGraph Agent Flow Visualizer
  4. Live MCP Tool & JSON-RPC Inspector
- Automated unit tests pass (`pytest`).
- Browser verification confirms dashboard rendering, chapter navigation, and studio interactions without 500s or uncaught errors.

### Gate 4: Git Delivery & Release
- Clean Git history on branch `main`.
- Remote origin configured (GitHub `ai-engineering-zero-to-hero`).
- Final commits pushed to remote repository.
