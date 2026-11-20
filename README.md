# AI Engineering: Zero to Hero

[![CI / Quality Gates](https://img.shields.io/badge/Quality%20Gates-Passed-success)](https://github.com/abda-dc/ai-engineering-zero-to-hero)
[![Jupyter Book 2](https://img.shields.io/badge/Jupyter%20Book-2.x-blue)](https://mystmd.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688)](https://fastapi.tiangolo.com)
[![Next.js 15](https://img.shields.io/badge/Next.js-15%20App%20Router-black)](https://nextjs.org)
[![MCP Standard](https://img.shields.io/badge/Protocol-MCP%20JSON--RPC-emerald)](https://modelcontextprotocol.io)

**AI Engineering: Zero to Hero** is an end-to-end, production-grade curriculum and full-stack companion platform designed to take developers from Python & Math foundations to Production RAG architectures, Autonomous Agents, and the Model Context Protocol (MCP).

---

## 🏛 Architecture Overview

```
ai-engineering-zero to hero/
├── AGENTS.md                          # Repository rules & autonomous gates
├── README.md                          # Master documentation
├── docker-compose.yml                 # Multi-container orchestration (Postgres, Redis, Qdrant, Backend, Frontend)
├── .env.example                       # Environment templates
├── book/                              # Jupyter Book 2 / MyST Markdown source
│   ├── myst.yml                       # MyST book configuration
│   ├── intro.md                       # Curriculum intro & flowchart
│   └── chapters/
│       ├── part1-foundations/         # Ch 00 - 02 (Python, Math, Classical ML)
│       ├── part2-core-genai/          # Ch 03 - 05 (GenAI, LLM Internals, Prompt Engineering)
│       ├── part3-rag-data/            # Ch 06 - 08 (Vector DBs, Data Pipelines, Production RAG)
│       └── part4-agents-prod/         # Ch 09 - 12 (Agents, MCP, MLOps, Evals/Observability)
├── scripts/
│   ├── build_notebooks.py             # Notebook generator covering 148 concepts
│   ├── verify_notebooks.py            # Code execution testbench
│   ├── sync_notebooks_to_app.py       # Notebook-to-App synchronization compiler
│   └── verify_curriculum.py           # Curriculum schema integrity test
└── app/
    ├── backend/                       # Python FastAPI Backend
    │   ├── main.py                    # REST + SSE Streaming API
    │   ├── db.py                      # PostgreSQL + SQLite fallback
    │   ├── cache.py                   # Semantic + Exact Caching
    │   ├── llm_service.py             # Ollama + Educational Simulator fallback
    │   ├── mcp_server.py              # Real MCP Server (JSON-RPC 2.0)
    │   ├── studio_service.py          # Tokenizer, Chunking, Graph & Search engines
    │   └── tests/test_api.py          # Pytest unit tests
    └── frontend/                      # Next.js 15 App Router + Tailwind CSS
        ├── src/app/
        │   ├── page.tsx               # Zero-to-Hero Mastery Dashboard
        │   ├── chapters/[id]/page.tsx # Interactive Book Reader & Quiz
        │   └── studio/page.tsx        # Split-Screen AI Engineering Studio
        └── src/data/curriculum.json   # Synced curriculum database
```

---

## 📚 Curriculum Breakdown (13 Chapters, 148 Concepts)

### Part I: Foundations
- **Chapter 00: Builder Launchpad** — Python for AI, OOP, REST APIs, Git/GitHub, Linux CLI
- **Chapter 01: Math & Stats Intuition for AI** — Linear Algebra, Dot Products, Cosine Similarity, Calculus/Gradients, Probability, Bayes Theorem
- **Chapter 02: The Classical Machine Learning Bridge** — Supervised/Unsupervised Learning, Loss Curves, Overfitting, Regularization, Cross-Validation

### Part II: Core Generative AI & Large Language Models
- **Chapter 03: Generative AI Foundations** — GenAI vs Discriminative, Neural Nets, Transformers, Self-Attention, Tokens, Embeddings, Foundation Models, Pre-training/Fine-tuning, Diffusion, GANs/VAEs, Multimodal, RLHF, Evals, AI Safety
- **Chapter 04: Inside Large Language Models** — Transformer Architecture, Attention Mechanisms, BPE Tokenization, Positional Encoding, Next-Token Prediction, Instruction Tuning, RLHF/DPO, Context Window, Temp/Top-k/p, Hallucinations, LoRA, Quantization, KV Cache, SLMs, Reasoning Models
- **Chapter 05: Prompt & Context Engineering** — Prompt Anatomy, System/Role Prompts, Zero/Few-Shot, Chain-of-Thought, Templates, Delimiters, Structured JSON Outputs, Guardrails, Prompt Chaining, Self-Consistency, ReAct, Prompt Injection, Output Evals, Context Engineering

### Part III: Vector Databases, Data Engineering & Production RAG
- **Chapter 06: Vector Databases & Similarity Search** — Vector DBs, Embeddings, Dimensions, Cosine/Dot Product, k-NN vs. ANN, HNSW & IVF Indexes, Product Quantization, Metadata Filtering, Hybrid Search, Namespaces, Upserts/Deletes, Sharding, Recall vs. Latency, pgvector, Qdrant, Chroma, FAISS
- **Chapter 07: Data Engineering for AI Systems** — Data Collection/APIs, ETL/ELT Pipelines, Data Cleaning, SQL/NoSQL, Streaming, Feature Stores, Data Versioning with DVC
- **Chapter 08: Production Retrieval-Augmented Generation (RAG)** — Why RAG, Architecture, Document Loading, Chunking Strategies, Embedding Models, Indexing, Top-k, Hybrid BM25 Search, Cross-Encoder Re-ranking, Query Rewriting, Prompt Augmentation, Context Mgmt, Citations/Grounding, Multi-hop RAG, GraphRAG, Agentic RAG, RAG Evals

### Part IV: Autonomous Agents, MCP & Production MLOps
- **Chapter 09: Autonomous AI Agents** — Agent Anatomy, Think→Act→Observe, ReAct, Tool/Function Calling, Planning/Decomposition, Short/Long-Term Memory, Reflection/Self-Critique, Multi-Agent Systems, Orchestrator-Worker, Routing, LangGraph Frameworks, Browser/Computer Use, Code Sandboxes, Human-in-the-Loop, Checkpointing, Cost/Latency Control
- **Chapter 10: Model Context Protocol (MCP)** — What is MCP, N×M Problem, Hosts/Clients/Servers, JSON-RPC, Tools, Resources, Prompts, Sampling, Capability Negotiation, stdio vs. Streamable HTTP, Lifecycle, Tool Schemas, OAuth, Building MCP Servers, Connecting IDEs/Apps, Local vs. Remote, Prompt Injection, Permissions, MCP Inspector
- **Chapter 11: Production Systems & MLOps for AI** — System Design, Microservices, Redis Caching, Celery/Queues, Model Serving with vLLM/FastAPI, Docker/Compose, GitHub Actions CI/CD, Prometheus/Grafana Monitoring
- **Chapter 12: Evals, Observability & AI Safety** — Ragas & DeepEval, Prompt A/B Testing, Hallucination Detection, OpenTelemetry Traces/Logs/Metrics, Cost & Latency Optimization, GDPR/HIPAA Privacy, AI Alignment/Fairness, Product UX

---

## ⚡ Quickstart & Zero-Docker Local Development

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ & npm 9+
- Git

### 2. Run Book Build & Sync
```powershell
# Build all 13 interactive notebooks
python "scripts/build_notebooks.py"

# Verify all notebook code cells execute with 0 errors
python "scripts/verify_notebooks.py"

# Sync notebooks into frontend curriculum database
python "scripts/sync_notebooks_to_app.py"

# Verify curriculum integrity
python "scripts/verify_curriculum.py"
```

### 3. Run Backend API
```powershell
# Run FastAPI server (defaults to local SQLite database & in-memory cache)
python -m uvicorn app.backend.main:app --reload --port 8000
```
Backend Swagger API Docs: `http://localhost:8000/docs`

### 4. Run Frontend App
```powershell
cd "app/frontend"
npm install
npm run dev
```
Open `http://localhost:3000` to access the Mastery Dashboard and Studio!

---

## 🐳 Full Containerized Deployment (Docker Compose)

```powershell
docker compose up --build
```
Services spun up:
- **Postgres (pgvector)**: `localhost:5432`
- **Redis 7**: `localhost:6379`
- **Qdrant**: `localhost:6333`
- **Backend API**: `localhost:8000`
- **Frontend App**: `localhost:3000`

---

## 🧪 Verification & Automated Testing

```powershell
# Run backend pytest suite
python -m pytest "app/backend/tests" -v

# Run Next.js production build verification
cd "app/frontend"
npm run build
```

---

## 🛡 License
MIT License. Built for the modern AI engineering community.
