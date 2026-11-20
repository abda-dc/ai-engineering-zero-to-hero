import math
import hashlib
from typing import List, Dict, Any, Optional

def toy_bpe_tokenize(text: str) -> List[Dict[str, Any]]:
    """Educational BPE Tokenizer breaking text into visual token slices."""
    words = text.split(" ")
    tokens = []
    current_idx = 0
    for w_idx, word in enumerate(words):
        prefix = " " if w_idx > 0 else ""
        full_word = prefix + word
        
        if len(word) > 5:
            mid = len(word) // 2
            sub1 = prefix + word[:mid]
            sub2 = word[mid:]
            h1 = int(hashlib.md5(sub1.encode()).hexdigest()[:6], 16) % 32000
            h2 = int(hashlib.md5(sub2.encode()).hexdigest()[:6], 16) % 32000
            tokens.append({"id": h1, "text": sub1, "start": current_idx, "length": len(sub1), "type": "subword"})
            current_idx += len(sub1)
            tokens.append({"id": h2, "text": sub2, "start": current_idx, "length": len(sub2), "type": "subword"})
            current_idx += len(sub2)
        else:
            h = int(hashlib.md5(full_word.encode()).hexdigest()[:6], 16) % 32000
            tokens.append({"id": h, "text": full_word, "start": current_idx, "length": len(full_word), "type": "word"})
            current_idx += len(full_word)
            
    return tokens

def generate_embedding_2d_projection(texts: List[str]) -> List[Dict[str, Any]]:
    """Generates simulated 16-D embeddings and projects to 2D for interactive scatter visualization."""
    points = []
    for idx, text in enumerate(texts):
        seed = int(hashlib.sha256(text.encode()).hexdigest()[:8], 16)
        x = ((seed % 1000) / 500.0) - 1.0
        y = (((seed // 1000) % 1000) / 500.0) - 1.0
        
        cat = "general"
        if any(k in text.lower() for k in ["rag", "vector", "search", "retriev"]):
            cat = "retrieval"
        elif any(k in text.lower() for k in ["agent", "react", "langgraph", "tool"]):
            cat = "agents"
        elif any(k in text.lower() for k in ["mcp", "protocol", "json-rpc", "server"]):
            cat = "protocol"
            
        points.append({
            "id": f"pt_{idx+1}",
            "text": text,
            "x": round(x, 3),
            "y": round(y, 3),
            "category": cat
        })
    return points

def chunk_text(text: str, strategy: str = "sliding", chunk_size: int = 20, overlap: int = 5) -> List[Dict[str, Any]]:
    """Interactive Chunking Engine supporting Fixed, Sliding Window, and Paragraph/Semantic splitting."""
    words = text.split()
    chunks = []
    
    if strategy == "fixed":
        for i in range(0, len(words), chunk_size):
            slice_words = words[i:i + chunk_size]
            c_text = " ".join(slice_words)
            chunks.append({
                "index": len(chunks) + 1,
                "text": c_text,
                "word_count": len(slice_words),
                "char_length": len(c_text),
                "start_token": i,
                "end_token": i + len(slice_words)
            })
    elif strategy == "paragraph":
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        for idx, p in enumerate(paragraphs):
            chunks.append({
                "index": idx + 1,
                "text": p,
                "word_count": len(p.split()),
                "char_length": len(p),
                "start_token": 0,
                "end_token": len(p.split())
            })
    else: # Sliding window default
        step = max(chunk_size - overlap, 1)
        for i in range(0, len(words), step):
            slice_words = words[i:i + chunk_size]
            c_text = " ".join(slice_words)
            chunks.append({
                "index": len(chunks) + 1,
                "text": c_text,
                "word_count": len(slice_words),
                "char_length": len(c_text),
                "start_token": i,
                "end_token": i + len(slice_words)
            })
            if i + chunk_size >= len(words):
                break
                
    return chunks

def hybrid_retrieval_benchmark(query: str, corpus: List[str], alpha: float = 0.5, rrf_k: int = 60) -> List[Dict[str, Any]]:
    """
    Runs hybrid retrieval:
    - Dense vector similarity
    - BM25-style keyword overlap
    - Reciprocal Rank Fusion (RRF) & Weighted Interpolation
    """
    q_words = set(query.lower().split())
    scored = []
    
    for idx, doc in enumerate(corpus):
        d_words = set(doc.lower().split())
        sparse_score = len(q_words.intersection(d_words)) / max(len(q_words), 1)
        
        union_len = len(q_words.union(d_words))
        dense_score = (len(q_words.intersection(d_words)) + 0.2) / max(union_len, 1)
        dense_score = min(dense_score * 1.5, 0.99)
        
        scored.append({
            "id": f"doc_{idx+1}",
            "text": doc,
            "sparse_score": round(sparse_score, 3),
            "dense_score": round(dense_score, 3)
        })
        
    scored_by_sparse = sorted(scored, key=lambda x: x["sparse_score"], reverse=True)
    sparse_rank = {item["id"]: rank for rank, item in enumerate(scored_by_sparse, 1)}
    
    scored_by_dense = sorted(scored, key=lambda x: x["dense_score"], reverse=True)
    dense_rank = {item["id"]: rank for rank, item in enumerate(scored_by_dense, 1)}
    
    final_list = []
    for item in scored:
        doc_id = item["id"]
        s_rank = sparse_rank[doc_id]
        d_rank = dense_rank[doc_id]
        rrf = (1.0 / (rrf_k + s_rank)) + (1.0 / (rrf_k + d_rank))
        hybrid_weighted = (alpha * item["dense_score"]) + ((1.0 - alpha) * item["sparse_score"])
        
        final_list.append({
            **item,
            "sparse_rank": s_rank,
            "dense_rank": d_rank,
            "rrf_score": round(rrf, 5),
            "hybrid_weighted_score": round(hybrid_weighted, 3)
        })
        
    final_list.sort(key=lambda x: x["rrf_score"], reverse=True)
    return final_list

def generate_agent_trace(task: str, pattern: str = "orchestrator_worker") -> Dict[str, Any]:
    """Generates a dynamic multi-step LangGraph-style agent graph execution trace."""
    nodes = [
        {"id": "router", "label": "Task Router", "type": "supervisor", "status": "completed"},
        {"id": "researcher", "label": "Research Worker", "type": "worker", "status": "completed"},
        {"id": "coder", "label": "Code Generator", "type": "worker", "status": "completed"},
        {"id": "evaluator", "label": "Safety & Test Gate", "type": "evaluator", "status": "completed"},
        {"id": "synthesizer", "label": "Response Synthesizer", "type": "output", "status": "completed"}
    ]
    edges = [
        {"source": "router", "target": "researcher", "label": "needs_domain_facts"},
        {"source": "router", "target": "coder", "label": "needs_implementation"},
        {"source": "researcher", "target": "evaluator", "label": "submit_evidence"},
        {"source": "coder", "target": "evaluator", "label": "submit_code"},
        {"source": "evaluator", "target": "synthesizer", "label": "tests_passed (score: 0.98)"}
    ]
    steps = [
        {
            "step": 1,
            "node": "router",
            "thought": f"Analyzing task: '{task}'. Requires decomposition into research and implementation phases.",
            "action": "route_to_workers",
            "params": {"workers": ["researcher", "coder"]},
            "observation": "Subtasks assigned to specialized agent workers."
        },
        {
            "step": 2,
            "node": "researcher",
            "thought": "Querying local vector database for architecture specs and best practices.",
            "action": "call_mcp_tool:vector_search",
            "params": {"query": task, "top_k": 3},
            "observation": "Found 3 verified technical passages. Grounding evidence prepared."
        },
        {
            "step": 3,
            "node": "coder",
            "thought": "Writing Python implementation with local fallbacks and type annotations.",
            "action": "execute_sandbox_code",
            "params": {"language": "python", "timeout_sec": 5},
            "observation": "Code executed with zero errors. All assertions passed."
        },
        {
            "step": 4,
            "node": "evaluator",
            "thought": "Running Ragas faithfulness evaluation and PII sanitization gate.",
            "action": "call_mcp_tool:check_guardrail",
            "params": {"target": "coder_output"},
            "observation": "Safety Gate PASSED. Faithfulness=0.96, Injection=False, PII=Clean."
        },
        {
            "step": 5,
            "node": "synthesizer",
            "thought": "Compiling final response with verified citations and structured output contract.",
            "action": "generate_final_answer",
            "params": {"format": "markdown_with_citations"},
            "observation": "Synthesis complete. Delivered to user."
        }
    ]
    return {
        "task": task,
        "pattern": pattern,
        "graph": {"nodes": nodes, "edges": edges},
        "trace": steps,
        "final_output": f"Successfully completed '{task}' with 5-node verified multi-agent graph execution."
    }
