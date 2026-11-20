import pytest
from fastapi.testclient import TestClient
from app.backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"

def test_curriculum():
    res = client.get("/api/curriculum")
    assert res.status_code == 200
    data = res.json()
    assert "parts" in data
    assert len(data["parts"]) == 4
    assert data["total_chapters"] == 13

def test_progress_crud():
    # Update progress for ch00
    post_res = client.post("/api/progress", json={
        "chapter_id": "ch00",
        "completed": True,
        "quiz_score": 100.0,
        "bookmarked": True,
        "notes": "Mastered OOP patterns"
    })
    assert post_res.status_code == 200
    updated = post_res.json()
    assert updated["completed"] is True
    assert updated["quiz_score"] == 100.0

    # Retrieve all progress
    get_res = client.get("/api/progress")
    assert get_res.status_code == 200
    all_prog = get_res.json()
    assert "ch00" in all_prog
    assert all_prog["ch00"]["completed"] is True

def test_llm_chat():
    res = client.post("/api/llm/chat", json={"prompt": "Explain RAG architecture"})
    assert res.status_code == 200
    data = res.json()
    assert "response" in data
    assert len(data["response"]) > 20
    assert "latency_ms" in data

def test_studio_tokenize():
    res = client.post("/api/studio/tokenize", json={"text": "Antigravity powers modern AI engineering."})
    assert res.status_code == 200
    data = res.json()
    assert data["token_count"] > 0
    assert len(data["tokens"]) == data["token_count"]

def test_studio_chunking():
    sample_text = "Retrieval-Augmented Generation connects foundation models to external verified knowledge bases, eliminating hallucinations."
    res = client.post("/api/studio/chunk", json={
        "text": sample_text,
        "strategy": "sliding",
        "chunk_size": 5,
        "overlap": 2
    })
    assert res.status_code == 200
    data = res.json()
    assert data["total_chunks"] > 1

def test_studio_hybrid_search():
    res = client.post("/api/studio/hybrid-search", json={
        "query": "vector databases",
        "alpha": 0.5,
        "rrf_k": 60
    })
    assert res.status_code == 200
    data = res.json()
    assert len(data["results"]) > 0
    assert "rrf_score" in data["results"][0]

def test_studio_agent_trace():
    res = client.post("/api/studio/agent-trace", json={"task": "Deploy RAG microservice"})
    assert res.status_code == 200
    data = res.json()
    assert len(data["graph"]["nodes"]) >= 5
    assert len(data["trace"]) == 5

def test_mcp_inspector():
    # 1. Initialize
    init_res = client.post("/api/mcp/inspect", json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    assert init_res.status_code == 200
    init_data = init_res.json()
    assert "result" in init_data
    assert init_data["result"]["protocolVersion"] == "2024-11-05"

    # 2. Tools List
    tools_res = client.post("/api/mcp/inspect", json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    assert tools_res.status_code == 200
    tools = tools_res.json()["result"]["tools"]
    assert any(t["name"] == "calculate_kv_cache" for t in tools)

    # 3. Tool Call
    call_res = client.post("/api/mcp/inspect", json={
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "calculate_kv_cache",
            "arguments": {"seq_len": 4096}
        }
    })
    assert call_res.status_code == 200
    call_data = call_res.json()
    assert "content" in call_data["result"]

def test_enrollment_stats():
    res = client.get("/api/enroll/stats")
    assert res.status_code == 200
    data = res.json()
    assert "total_enrolled" in data
    assert "seats_remaining" in data
    assert "total_live_seats" in data
    assert data["total_live_seats"] == 60

def test_enrollment_flow_and_duplicate_prevention():
    test_email = "alex.turner.test@example.com"
    
    # 1. Valid enrollment
    res1 = client.post("/api/enroll", json={
        "full_name": "Alex Turner",
        "email": test_email,
        "github_username": "alexturner",
        "experience_level": "intermediate",
        "track": "live_cohort",
        "goal": "Master production RAG and MCP server development"
    })
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["status"] == "confirmed"
    assert "ticket_id" in data1
    assert data1["ticket_id"].startswith("AIENG-")
    assert len(data1["onboarding_steps"]) >= 4

    # 2. Duplicate enrollment attempt with same email
    res2 = client.post("/api/enroll", json={
        "full_name": "Alex Turner",
        "email": test_email,
        "github_username": "alexturner",
        "experience_level": "intermediate",
        "track": "live_cohort"
    })
    assert res2.status_code == 409
    assert "already enrolled" in res2.json()["detail"]

def test_enrollment_invalid_email():
    res = client.post("/api/enroll", json={
        "full_name": "Bad Email User",
        "email": "not-an-email",
        "experience_level": "beginner",
        "track": "self_paced"
    })
    assert res.status_code == 422

