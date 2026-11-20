---
marp: true
theme: default
paginate: true
header: 'AI Engineering: Zero to Hero | Week 11: Production RAG Systems Part B'
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
## Week 11: Production RAG Systems Part B
### Multi-Hop RAG, GraphRAG, Inline Citations & Ragas Evals

**Part IV: Capstone & Production** • *CH08 Companion*

### Learning Objectives:
1. Multi-Hop Query Decomposition: Splitting complex comparative questions into sub-queries for multi-step retrieva...
2. GraphRAG Fundamentals: Extracting entity-relationship graphs to capture cross-document global themes....
3. Inline Citations & Grounding: Guaranteed bracketed citations `[1][2]` tied strictly to retrieved source spans....
4. The RAG Triad Evals: Context Precision, Faithfulness (groundedness), and Answer Relevance....

> *"Advanced RAG architectures: multi-hop query decomposition, Knowledge Graph RAG, strict bracketed citations, and automated Ragas evaluation."*

<!-- Speaker Notes:
Welcome cohort to Week 11: Production RAG Systems Part B. Emphasize production rigor and end-to-end integration.
-->
---

## System Architecture & Mental Model
### Week 11: Production RAG Systems Part B Architectural Overview

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

## Core Concept: Multi-Hop Query Decomposition
### Multi-Hop RAG, GraphRAG, Inline Citations & Ragas Evals

### Technical Breakdown:
- Splitting complex comparative questions into sub-queries for multi-step retrieval.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Multi-Hop Query Decomposition. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: GraphRAG Fundamentals
### Multi-Hop RAG, GraphRAG, Inline Citations & Ragas Evals

### Technical Breakdown:
- Extracting entity-relationship graphs to capture cross-document global themes.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into GraphRAG Fundamentals. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: Inline Citations & Grounding
### Multi-Hop RAG, GraphRAG, Inline Citations & Ragas Evals

### Technical Breakdown:
- Guaranteed bracketed citations `[1][2]` tied strictly to retrieved source spans.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Inline Citations & Grounding. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: The RAG Triad Evals
### Multi-Hop RAG, GraphRAG, Inline Citations & Ragas Evals

### Technical Breakdown:
- Context Precision, Faithfulness (groundedness), and Answer Relevance.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into The RAG Triad Evals. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: Ragas & DeepEval in CI/CD
### Multi-Hop RAG, GraphRAG, Inline Citations & Ragas Evals

### Technical Breakdown:
- Automated regression gates preventing bad chunking or prompt drift.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Ragas & DeepEval in CI/CD. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Annotated Code: Week 11: Production RAG Systems Part B
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
2. Navigate to: Inspect citation grounding and run automated RAG Triad benchmark on sample enterprise QA pairs.
3. Run baseline scenario and observe real-time telemetry.
4. Introduce deliberate edge-case error and demonstrate recovery mechanism.

<!-- Speaker Notes:
Execute live demo: Inspect citation grounding and run automated RAG Triad benchmark on sample enterprise QA pairs.
-->
---

## Common Pitfalls & Production Failures
### Failure Modes in Week 11: Production RAG Systems Part B

### Top 3 Production Failure Modes:
1. **Unmonitored Latency Drift:** Long-tail queries degrading P99 latency without triggering alerts.
2. **Missing Fallbacks:** Hard crashes when external dependencies experience momentary blips.
3. **Evaluation Blind Spots:** Relying on human vibes instead of automated quantitative metrics.

<!-- Speaker Notes:
Highlight how easily untested assumptions turn into midnight production outages.
-->
---

## Weekly Deliverable: Week 11: Production RAG Systems Part B
### Milestone 11 Specifications

### Deliverable Requirements:
- Evaluate a RAG pipeline on 30 test questions using Ragas metrics and enforce >0.85 faithfulness threshold.
- Unit tests passing cleanly in `pytest`.
- Verified against zero Docker and zero paid API dependencies.
- Push code to your branch `feat/w11-deliverable`.

<!-- Speaker Notes:
Emphasize the definition of done and automated test verification.
-->
---

## Week 11 Check-Out Quiz
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
