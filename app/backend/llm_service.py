import httpx
import json
import time
import asyncio
from typing import AsyncGenerator, Dict, Any, List
from .config import settings
from .cache import semantic_cache

def generate_educational_response(prompt: str, model: str) -> str:
    """Deterministic high-craft educational simulator when local Ollama is offline."""
    prompt_lower = prompt.lower()
    
    if "rag" in prompt_lower or "retriev" in prompt_lower:
        return (
            f"[AI Engineering Simulator - Model: {model}]\n\n"
            "Retrieval-Augmented Generation (RAG) grounds LLM generations in external enterprise corpora:\n"
            "1. Ingestion: Documents are chunked (e.g. 500 tokens with 10% overlap) and embedded via dense encoders.\n"
            "2. Retrieval: Hybrid search combines BM25 keyword matching with HNSW dense vector ANN search.\n"
            "3. Reranking: A cross-encoder scores (query, passage) token interactions to isolate top-k passages.\n"
            "4. Grounding: Context is passed with bracketed citations [1][2] into the generation prompt."
        )
    elif "mcp" in prompt_lower or "protocol" in prompt_lower:
        return (
            f"[AI Engineering Simulator - Model: {model}]\n\n"
            "The Model Context Protocol (MCP) standardizes AI tool and data connectivity over JSON-RPC 2.0:\n"
            "• Architecture: Host Clients (IDEs, desktop agents) connect to MCP Servers via stdio or SSE.\n"
            "• Core Primitives: Tools (callable functions), Resources (readable data/schemas), Prompts (templates).\n"
            "• Capability Negotiation: Clients and servers exchange supported features during the initialize handshake."
        )
    elif "agent" in prompt_lower or "react" in prompt_lower or "langgraph" in prompt_lower:
        return (
            f"[AI Engineering Simulator - Model: {model}]\n\n"
            "Autonomous AI Agents leverage the ReAct (Reason + Act) loop to solve complex tasks:\n"
            "1. Thought: The agent decomposes the objective and selects candidate tools.\n"
            "2. Action: Executes a tool (e.g., code execution, web search, SQL query) in a sandboxed runtime.\n"
            "3. Observation: Ingests the tool output back into the context window.\n"
            "4. LangGraph: Encapsulates state transitions in cyclical graphs with human-in-the-loop checkpoints."
        )
    elif "vector" in prompt_lower or "embedding" in prompt_lower:
        return (
            f"[AI Engineering Simulator - Model: {model}]\n\n"
            "Vector embeddings map semantic meaning into high-dimensional geometric spaces:\n"
            "• Distance Metrics: Cosine similarity measures directional angle; dot product includes magnitude.\n"
            "• ANN Indexing: HNSW provides logarithmic graph traversal; IVF partitions space into Voronoi centroids.\n"
            "• Hybrid Fusion: Reciprocal Rank Fusion (RRF) harmonizes dense semantics with sparse BM25 keywords."
        )
    else:
        return (
            f"[AI Engineering Simulator - Model: {model}]\n\n"
            f"Processed prompt: '{prompt[:120]}...'\n\n"
            "Core AI Engineering Takeaways:\n"
            "• Minimize Time-To-First-Token (TTFT) via KV caching and streaming.\n"
            "• Guard your system with prompt injection sanitizers and PII scrubbers.\n"
            "• Measure the RAG Triad: Context Precision, Faithfulness, and Answer Relevance."
        )

async def check_ollama_available() -> bool:
    try:
        async with httpx.AsyncClient(timeout=0.6) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            return resp.status_code == 200
    except Exception:
        return False

async def query_llm(prompt: str, model: str = None) -> Dict[str, Any]:
    """Queries Ollama if online; otherwise invokes the deterministic simulator."""
    target_model = model or settings.OLLAMA_MODEL
    t0 = time.time()
    
    # 1. Exact cache check
    cached = semantic_cache.get_exact(prompt)
    if cached:
        return {
            "response": cached,
            "source": "cache_exact",
            "latency_ms": round((time.time() - t0) * 1000, 2),
            "model": target_model
        }

    # 2. Try Ollama
    is_live = await check_ollama_available()
    if is_live:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(
                    f"{settings.OLLAMA_BASE_URL}/api/generate",
                    json={"model": target_model, "prompt": prompt, "stream": False}
                )
                if res.status_code == 200:
                    text = res.json().get("response", "")
                    semantic_cache.set_exact(prompt, text)
                    return {
                        "response": text,
                        "source": "ollama_live",
                        "latency_ms": round((time.time() - t0) * 1000, 2),
                        "model": target_model
                    }
        except Exception:
            pass

    # 3. Simulator Fallback
    text = generate_educational_response(prompt, target_model)
    semantic_cache.set_exact(prompt, text)
    return {
        "response": text,
        "source": "educational_simulator_fallback",
        "latency_ms": round((time.time() - t0) * 1000 + 8.5, 2),
        "model": target_model
    }

async def stream_llm(prompt: str, model: str = None) -> AsyncGenerator[str, None]:
    """Streams tokens as Server-Sent Events (SSE)."""
    target_model = model or settings.OLLAMA_MODEL
    is_live = await check_ollama_available()
    
    if is_live:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                async with client.stream(
                    "POST",
                    f"{settings.OLLAMA_BASE_URL}/api/generate",
                    json={"model": target_model, "prompt": prompt, "stream": True}
                ) as response:
                    if response.status_code == 200:
                        async for line in response.aiter_lines():
                            if line:
                                data = json.loads(line)
                                token = data.get("response", "")
                                yield f"data: {json.dumps({'token': token, 'done': data.get('done', False)})}\n\n"
                        return
        except Exception:
            pass

    full_text = generate_educational_response(prompt, target_model)
    words = full_text.split(" ")
    for idx, w in enumerate(words):
        chunk = w + (" " if idx < len(words) - 1 else "")
        yield f"data: {json.dumps({'token': chunk, 'done': idx == len(words) - 1})}\n\n"
        await asyncio.sleep(0.02)
