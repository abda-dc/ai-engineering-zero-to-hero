import json
import re
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from .config import settings
from .db import init_db, ProgressRepository, VectorRepository, CohortEnrollmentRepository
from .cache import semantic_cache
from .llm_service import query_llm, stream_llm
from .mcp_server import mcp_server
from .studio_service import (
    toy_bpe_tokenize,
    generate_embedding_2d_projection,
    chunk_text,
    hybrid_retrieval_benchmark,
    generate_agent_trace
)

# Initialize Database on startup
init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Full-Stack Backend Companion for AI Engineering: Zero to Hero"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request / Response Models ---
class ProgressUpdateRequest(BaseModel):
    chapter_id: str
    completed: Optional[bool] = None
    quiz_score: Optional[float] = None
    bookmarked: Optional[bool] = None
    notes: Optional[str] = None

class LLMChatRequest(BaseModel):
    prompt: str
    model: Optional[str] = None

class TokenizeRequest(BaseModel):
    text: str

class EmbeddingsRequest(BaseModel):
    texts: List[str]

class ChunkRequest(BaseModel):
    text: str
    strategy: str = "sliding"
    chunk_size: int = 20
    overlap: int = 5

class HybridSearchRequest(BaseModel):
    query: str
    corpus: Optional[List[str]] = None
    alpha: float = 0.5
    rrf_k: int = 60

class AgentTraceRequest(BaseModel):
    task: str
    pattern: str = "orchestrator_worker"

class EnrollmentRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=150)
    github_username: Optional[str] = Field(None, max_length=100)
    experience_level: str = Field("intermediate", description="beginner, intermediate, or advanced")
    track: str = Field("live_cohort", description="live_cohort or self_paced")
    goal: Optional[str] = Field(None, max_length=1000)

# --- Endpoints ---

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": "sqlite_local_ready"
    }

@app.get("/api/curriculum")
async def get_curriculum():
    if not settings.CURRICULUM_PATH.exists():
        raise HTTPException(status_code=404, detail="curriculum.json not found. Run sync script.")
    with open(settings.CURRICULUM_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/api/progress")
async def get_progress():
    return ProgressRepository.get_all_progress()

@app.post("/api/progress")
async def update_progress(req: ProgressUpdateRequest):
    return ProgressRepository.update_progress(
        chapter_id=req.chapter_id,
        completed=req.completed,
        quiz_score=req.quiz_score,
        bookmarked=req.bookmarked,
        notes=req.notes
    )

@app.post("/api/llm/chat")
async def chat_completion(req: LLMChatRequest):
    return await query_llm(req.prompt, req.model)

@app.post("/api/llm/stream")
async def stream_completion(req: LLMChatRequest):
    return StreamingResponse(
        stream_llm(req.prompt, req.model),
        media_type="text/event-stream"
    )

@app.get("/api/cache/stats")
async def get_cache_stats():
    return semantic_cache.get_stats()

# --- Studio Lab Endpoints ---

@app.post("/api/studio/tokenize")
async def studio_tokenize(req: TokenizeRequest):
    tokens = toy_bpe_tokenize(req.text)
    return {
        "text": req.text,
        "token_count": len(tokens),
        "tokens": tokens
    }

@app.post("/api/studio/embeddings")
async def studio_embeddings(req: EmbeddingsRequest):
    points = generate_embedding_2d_projection(req.texts)
    return {
        "points": points,
        "count": len(points)
    }

@app.post("/api/studio/chunk")
async def studio_chunk(req: ChunkRequest):
    chunks = chunk_text(
        text=req.text,
        strategy=req.strategy,
        chunk_size=req.chunk_size,
        overlap=req.overlap
    )
    return {
        "strategy": req.strategy,
        "chunk_size": req.chunk_size,
        "overlap": req.overlap,
        "total_chunks": len(chunks),
        "chunks": chunks
    }

@app.post("/api/studio/hybrid-search")
async def studio_hybrid_search(req: HybridSearchRequest):
    default_corpus = [
        "Retrieval-Augmented Generation grounds LLMs with external verified documents.",
        "Model Context Protocol standardizes AI tools and resources via JSON-RPC 2.0.",
        "LangGraph enables stateful multi-agent systems with cyclical decision graphs.",
        "HNSW provides high-speed approximate nearest neighbor vector search.",
        "Cross-Encoder reranking scores token interactions between queries and candidate chunks.",
        "Prometheus and OpenTelemetry capture latency, token usage, and system traces."
    ]
    corpus = req.corpus if req.corpus and len(req.corpus) > 0 else default_corpus
    results = hybrid_retrieval_benchmark(
        query=req.query,
        corpus=corpus,
        alpha=req.alpha,
        rrf_k=req.rrf_k
    )
    return {
        "query": req.query,
        "alpha": req.alpha,
        "rrf_k": req.rrf_k,
        "results": results
    }

@app.post("/api/studio/agent-trace")
async def studio_agent_trace(req: AgentTraceRequest):
    return generate_agent_trace(task=req.task, pattern=req.pattern)

# --- MCP Inspector Endpoint ---

@app.post("/api/mcp/inspect")
async def mcp_inspect(request: Request):
    try:
        rpc_body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON-RPC payload")
    return mcp_server.dispatch(rpc_body)

# --- Cohort Enrollment Endpoints ---

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

@app.get("/api/enroll/stats")
async def get_enrollment_stats():
    """Returns live cohort seat counts and enrollment statistics."""
    return CohortEnrollmentRepository.get_stats()

@app.post("/api/enroll")
async def enroll_student(req: EnrollmentRequest):
    """Enrolls a student in the cohort, preventing duplicate signups and issuing a ticket ID."""
    clean_email = req.email.strip().lower()
    
    # 1. Validate email format
    if not EMAIL_REGEX.match(clean_email):
        raise HTTPException(status_code=422, detail="Invalid email address format.")
    
    # 2. Prevent duplicate signups cleanly
    existing = CohortEnrollmentRepository.get_by_email(clean_email)
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Email '{clean_email}' is already enrolled with Ticket ID {existing['id']}."
        )
    
    # 3. Generate unique Ticket ID
    ticket_id = f"AIENG-{uuid.uuid4().hex[:8].upper()}"
    
    # 4. Save enrollment
    record = CohortEnrollmentRepository.create_enrollment(
        enrollment_id=ticket_id,
        full_name=req.full_name,
        email=clean_email,
        github_username=req.github_username,
        experience_level=req.experience_level,
        track=req.track,
        goal=req.goal
    )
    
    return {
        "status": "confirmed",
        "ticket_id": ticket_id,
        "message": f"Welcome aboard, {req.full_name}! Your enrollment in the AI Engineering Cohort is confirmed.",
        "enrollment": record,
        "onboarding_steps": [
            "1. Launch Chapter 00 (Builder Launchpad) to verify your local Python 3.11+ environment.",
            "2. Install Ollama and pull local models: 'ollama pull llama3.2:3b' and 'ollama pull qwen2.5:7b'.",
            "3. Explore Split-Screen Studio at /studio to test tokenizer and hybrid retrieval labs.",
            "4. Ingest study-guides/ into Google NotebookLM for audio podcast overviews."
        ]
    }
