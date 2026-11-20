---
marp: true
theme: default
paginate: true
header: 'AI Engineering: Zero to Hero | Week 01: The Builder's Launchpad'
footer: '16-Week Intensive Cohort © 2026'
style: |
  section {
    background-color: #0b0f19;
    color: #e2e8f0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    padding: 40px;
    font-size: 24px;
  }
  h1 {
    color: #38bdf8;
    font-size: 40px;
    margin-bottom: 16px;
  }
  h2 {
    color: #34d399;
    font-size: 30px;
    margin-bottom: 12px;
  }
  h3 {
    color: #a78bfa;
    font-size: 24px;
    margin-bottom: 8px;
  }
  code {
    background-color: #1e293b;
    color: #38bdf8;
    font-family: 'Fira Code', monospace;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.9em;
  }
  pre {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 14px;
    font-size: 16px;
    line-height: 1.4;
  }
  blockquote {
    border-left: 4px solid #38bdf8;
    background: #1e293b;
    padding: 10px 18px;
    border-radius: 0 8px 8px 0;
    margin: 16px 0;
  }
  footer, header {
    color: #64748b;
    font-size: 13px;
  }
---
## Week 01: The Builder's Launchpad
### Python OOP, REST APIs, Git Hygiene & Local Ollama

### Learning Objectives:
1. Master Object-Oriented modeling for AI components (Pipelines, Embedders, LLM Clients).
2. Build non-blocking asynchronous REST APIs with **FastAPI**.
3. Establish Git trunk-based branch hygiene & semantic commit standards.
4. Set up local zero-cost LLM inference via **Ollama** (`llama3.2:3b`, `qwen2.5:7b`).

> *"An AI Engineer is first and foremost a rigorous software engineer who treats model calls as unreliable network RPCs."*

<!-- Speaker Notes:
Welcome students to Week 1. Emphasize software craftsmanship and setting up local-first tooling.
-->
---

## Architecture: The Modern AI Engineering Stack
### Local-First Development & Deployment Topology

```
+-------------------------------------------------------------+
|                    Client UI Layer                          |
|           (Next.js App Router / Desktop Agent)              |
+-----------------------------+-------------------------------+
                              | JSON-RPC / SSE Stream
+-----------------------------v-------------------------------+
|               FastAPI Application Gateway                   |
|        (Pydantic Validation, Rate Limiter, Cache)           |
+--------------+------------------------------+---------------+
               |                              |
+--------------v--------------+ +-------------v---------------+
|    Local Ollama Inference   | |    Embedded State Layer     |
| (llama3.2:3b / qwen2.5:7b)  | |  (SQLite Progress & Vector) |
+-----------------------------+ +-----------------------------+
```

<!-- Speaker Notes:
Walk through each tier. Point out that the architecture works completely offline without cloud API keys.
-->
---

## OOP System Modeling for AI Components
### Abstracting Volatile Foundation Models

### Why Polymorphic Interfaces Matter:
- Wrap external model providers behind a uniform contract.
- Decouple prompt formulation from execution runtime.

```python
from abc import ABC, abstractmethod

class BaseLLMClient(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate text completion."""
        pass
```
- Swap between Ollama, vLLM, and Claude with **zero downstream code changes**.

<!-- Speaker Notes:
Explain how hardcoding vendor SDKs creates technical debt. BaseLLMClient allows seamless mocking and switching.
-->
---

## Asynchronous REST with FastAPI
### Non-Blocking I/O for High-Latency LLMs

### Concurrency Under High-Latency Calls:
- LLM generations take 500ms to 5000ms.
- Synchronous worker threads deplete rapidly under modest loads.
- `async / await` frees the Python event loop during network socket I/O.

```python
@app.post('/api/generate')
async def generate_response(req: PromptRequest):
    # Non-blocking async HTTP call to local Ollama daemon
    response = await ollama_client.generate(req.prompt)
    return {'status': 'success', 'data': response}
```

<!-- Speaker Notes:
Explain the difference between CPU-bound and I/O-bound workloads in Python. LLM calls are almost entirely I/O-bound.
-->
---

## Local Zero-Cost Inference with Ollama
### Running 3B and 7B Models on Everyday Laptops

### Why Local Models in 2026?
- **Zero API Bill:** Run 10,000 automated unit tests without paying OpenAI/Anthropic.
- **Absolute Privacy:** Sensitive code and customer data never leave `localhost`.

```bash
# Pull required course models
ollama pull llama3.2:3b    # Fast 3B model (2.0 GB VRAM)
ollama pull qwen2.5:7b     # High-reasoning 7B model (4.7 GB VRAM)

# Test HTTP inference directly
curl -s http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "What is AI engineering in 10 words?",
  "stream": false
}'
```

<!-- Speaker Notes:
Show the terminal commands. Highlight that llama3.2:3b runs at over 40 tokens/sec on standard M-series Macs or NVIDIA RTX GPUs.
-->
---

## Annotated Code: Streaming Ollama Client
### Processing Tokens in Real Time

```python
import httpx
import json
from typing import AsyncGenerator

class LocalOllamaClient:
    def __init__(self, base_url: str = 'http://localhost:11434'):
        self.base_url = base_url

    async def stream(self, prompt: str, model: str = 'llama3.2:3b') -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream(
                'POST',
                f'{self.base_url}/api/generate',
                json={'model': model, 'prompt': prompt, 'stream': True}
            ) as resp:
                async for line in resp.aiter_lines():
                    if line:
                        chunk = json.loads(line)
                        yield chunk.get('response', '')
```

<!-- Speaker Notes:
Explain line-by-line streaming. Explain that aiter_lines() allows piping tokens directly into FastAPI's StreamingResponse.
-->
---

## Live Demo Cue: Studio & Environment
### Instructor Live Walkthrough Steps

### Instructor Live Execution:
1. Verify local backend: `curl.exe http://127.0.0.1:8000/api/health`
2. Verify local Ollama: `curl.exe http://localhost:11434/api/tags`
3. Open `http://localhost:3000` to show the Mastery Dashboard.
4. Walk through Chapter 00 in the Interactive Reader (`/chapters/ch00`).
5. Open `http://localhost:3000/studio` to preview live tabs.
6. Show Google Colab one-click launch badge.

<!-- Speaker Notes:
Switch to browser and terminal to demonstrate these live steps. Encourage students to follow along on their machines.
-->
---

## Common Pitfalls & Failure Modes
### What Breaks in Production Systems

### Top 3 Week 1 Traps:
1. **Unbounded Input Length:** Users submitting 500kb prompts causing out-of-memory crashes on small models.
   - *Fix:* Enforce Pydantic `Field(..., max_length=2000)`.
2. **Synchronous Requests in Async Routes:** Calling `requests.post()` inside `async def` blocks the entire server event loop.
   - *Fix:* Always use `httpx.AsyncClient`.
3. **Unquoted Windows Paths with Spaces:** Path errors in PowerShell.
   - *Fix:* Always quote `"C:\Users\...\ai-engineering-zero to hero"`.

<!-- Speaker Notes:
Warn students about GIL locking when mixing sync HTTP libraries inside async routes.
-->
---

## Weekly Deliverable: The Builder Launchpad
### Capstone Milestone 01

### Deliverable Requirements:
- Complete `book/chapters/part1-foundations/ch00-builder-launchpad.ipynb`.
- Implement a verified FastAPI microservice with:
  1. `GET /api/health` checking database and Ollama availability.
  2. `POST /api/llm/chat` with Pydantic validation and local model routing.
  3. Passing test suite with `pytest`.
- Push code to your branch `feat/w01-launchpad`.

<!-- Speaker Notes:
Reiterate definition of done: notebook runs top-to-bottom with zero errors and pytest passes.
-->
---

## Week 01 Check-Out Quiz
### Review & Consolidation

### Knowledge Check:
1. **Why must LLM endpoints use asynchronous I/O in FastAPI?**
   - *Answer:* LLM calls are I/O-bound with high latency. Async avoids thread-pool exhaustion.
2. **What does Ollama's `stream: false` parameter do?**
   - *Answer:* Blocks until the complete response is generated and returns one aggregated JSON payload.
3. **Why do we separate model client logic from API routing logic?**
   - *Answer:* Modularity, ease of unit testing via mocks, and zero vendor lock-in.

<!-- Speaker Notes:
Quiz students interactively before closing the session.
-->
