---
marp: true
theme: default
paginate: true
header: 'AI Engineering: Zero to Hero | Week 06: Prompt & Context Engineering Part A'
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
## Week 06: Prompt & Context Engineering Part A
### Prompt Anatomy, System Roles, CoT, Delimiters & Pydantic JSON

**Part IV: Capstone & Production** • *CH05 Companion*

### Learning Objectives:
1. Anatomy of an Enterprise System Prompt: Role framing, task constraints, output specifications, and defensive boundaries....
2. Delimiters & Input Isolation: Using XML tags (`<context>`, `<query>`) to prevent structural confusion....
3. Chain-of-Thought (CoT) Reasoning: Zero-shot CoT ('Think step by step') vs. Few-shot exemplars to boost reasoning a...
4. Structured JSON Outputs via Pydantic: Enforcing strict schema contracts via JSON Schema and grammar-guided decoding....

> *"Systematic prompt engineering: anatomy of production prompts, delimiter isolation, chain-of-thought, and guaranteed Pydantic JSON schemas."*

<!-- Speaker Notes:
Welcome cohort to Week 06: Prompt & Context Engineering Part A. Emphasize production rigor and end-to-end integration.
-->
---

## System Architecture & Mental Model
### Week 06: Prompt & Context Engineering Part A Architectural Overview

```
+--------------------------------------------------------------+
|                       Client Gateway                         |
+------------------------------+-------------------------------+
                               |
+------------------------------v-------------------------------+
|                   Core Orchestration Engine                  |
|        (FastAPI / LangGraph / Model Context Protocol)        |
+--------------+-------------------------------+---------------+
               |                               |
+--------------v---------------+ +-------------v---------------+
|  Hybrid Storage & Search     | |  Inference & Safety Engine  |
|  (pgvector / Redis / Qdrant) | |  (Ollama / Guardrails / OTel)|
+------------------------------+ +-----------------------------+
```
- Decoupled, asynchronous, resilient system design.

<!-- Speaker Notes:
Walk through the core components and their data flows.
-->
---

## Core Concept: Anatomy of an Enterprise System Prompt
### Prompt Anatomy, System Roles, CoT, Delimiters & Pydantic JSON

### Technical Breakdown:
- Role framing, task constraints, output specifications, and defensive boundaries.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Anatomy of an Enterprise System Prompt. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: Delimiters & Input Isolation
### Prompt Anatomy, System Roles, CoT, Delimiters & Pydantic JSON

### Technical Breakdown:
- Using XML tags (`<context>`, `<query>`) to prevent structural confusion.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Delimiters & Input Isolation. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: Chain-of-Thought (CoT) Reasoning
### Prompt Anatomy, System Roles, CoT, Delimiters & Pydantic JSON

### Technical Breakdown:
- Zero-shot CoT ('Think step by step') vs. Few-shot exemplars to boost reasoning accuracy.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Chain-of-Thought (CoT) Reasoning. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: Structured JSON Outputs via Pydantic
### Prompt Anatomy, System Roles, CoT, Delimiters & Pydantic JSON

### Technical Breakdown:
- Enforcing strict schema contracts via JSON Schema and grammar-guided decoding.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Structured JSON Outputs via Pydantic. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: Context Window Packing & Truncation
### Prompt Anatomy, System Roles, CoT, Delimiters & Pydantic JSON

### Technical Breakdown:
- Strategies for handling long conversations without blowing token budgets.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Context Window Packing & Truncation. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Annotated Code: Week 06: Prompt & Context Engineering Part A
### Production Implementation Pattern

```python
from typing import Dict, Any, List
import asyncio

class ProductionEngine:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.is_ready = True
        
    async def execute_task(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Executes production workflow with error handling and fallback."""
        try:
            # High-reliability non-blocking execution
            result = await self._run_core_logic(payload)
            return {'status': 'success', 'data': result}
        except Exception as e:
            return {'status': 'fallback', 'error': str(e)}
```

<!-- Speaker Notes:
Explain defensive error handling and why silent fallbacks are crucial in user-facing systems.
-->
---

## Live Demo Cue: Studio Execution
### Instructor Step-by-Step Walkthrough

### Live Demonstration:
1. Open `http://localhost:3000/studio`.
2. Navigate to: Test prompt delimiters and schema validation live using local Ollama model in /api/llm/chat.
3. Run baseline scenario and observe real-time telemetry.
4. Introduce deliberate edge-case error and demonstrate recovery mechanism.

<!-- Speaker Notes:
Execute live demo: Test prompt delimiters and schema validation live using local Ollama model in /api/llm/chat.
-->
---

## Common Pitfalls & Production Failures
### Failure Modes in Week 06: Prompt & Context Engineering Part A

### Top 3 Production Failure Modes:
1. **Unmonitored Latency Drift:** Long-tail queries degrading P99 latency without triggering alerts.
2. **Missing Fallbacks:** Hard crashes when external dependencies experience momentary blips.
3. **Evaluation Blind Spots:** Relying on human vibes instead of automated quantitative metrics.

<!-- Speaker Notes:
Highlight how easily untested assumptions turn into midnight production outages.
-->
---

## Weekly Deliverable: Week 06: Prompt & Context Engineering Part A
### Milestone 06 Specifications

### Deliverable Requirements:
- Build a typed Pydantic extractor that parses unstructured customer support transcripts into JSON.
- Unit tests passing cleanly in `pytest`.
- Verified against zero Docker and zero paid API dependencies.
- Push code to your branch `feat/w06-deliverable`.

<!-- Speaker Notes:
Emphasize the definition of done and automated test verification.
-->
---

## Week 06 Check-Out Quiz
### Review & Consolidation

### Knowledge Check:
1. **What is the primary architectural invariant for this system?**
   - *Answer:* Decoupled components with explicit contracts and resilient fallbacks.
2. **How does this week's milestone feed into the final 100-point Capstone?**
   - *Answer:* Directly satisfies one of the 5 core grading rubric dimensions.
3. **Where can students access the runnable notebook and study guides?**
   - *Answer:* In `book/chapters/` and `study-guides/` for Google NotebookLM.

<!-- Speaker Notes:
Wrap up the lecture and open the floor for student Q&A.
-->
