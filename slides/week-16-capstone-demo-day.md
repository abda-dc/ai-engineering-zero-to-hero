---
marp: true
theme: default
paginate: true
header: 'AI Engineering: Zero to Hero | Week 16: Capstone Demo Day & Graduation'
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
## Week 16: Capstone Demo Day & Graduation
### 100-Point Rubric Walkthrough, Live Defense Format & Alumni Next Steps

**Part IV: Capstone & Production** • *CAPSTONE Companion*

### Learning Objectives:
1. The 100-Point Capstone Rubric: Detailed scoring across Architecture (20), MCP/Agents (20), RAG (20), Production...
2. Live Defense Protocol: 10-minute system architecture demo + 5-minute live code walkthrough + 5-minute Q...
3. Common Defense Failure Points: Missing fallbacks, brittle prompt engineering, untested edge cases, and lack of ...
4. From Student to AI Engineer: Publishing open-source repositories, portfolio presentation, and navigating AI e...

> *"Cohort graduation and Capstone Defense: presenting production AI systems evaluated against the 100-point rubric, live grading, and career transition."*

<!-- Speaker Notes:
Welcome cohort to Week 16: Capstone Demo Day & Graduation. Emphasize production rigor and end-to-end integration.
-->
---

## System Architecture & Mental Model
### Week 16: Capstone Demo Day & Graduation Architectural Overview

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

## Core Concept: The 100-Point Capstone Rubric
### 100-Point Rubric Walkthrough, Live Defense Format & Alumni Next Steps

### Technical Breakdown:
- Detailed scoring across Architecture (20), MCP/Agents (20), RAG (20), Production (20), Safety (20).

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into The 100-Point Capstone Rubric. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: Live Defense Protocol
### 100-Point Rubric Walkthrough, Live Defense Format & Alumni Next Steps

### Technical Breakdown:
- 10-minute system architecture demo + 5-minute live code walkthrough + 5-minute Q&A defense.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Live Defense Protocol. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: Common Defense Failure Points
### 100-Point Rubric Walkthrough, Live Defense Format & Alumni Next Steps

### Technical Breakdown:
- Missing fallbacks, brittle prompt engineering, untested edge cases, and lack of metrics.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Common Defense Failure Points. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: From Student to AI Engineer
### 100-Point Rubric Walkthrough, Live Defense Format & Alumni Next Steps

### Technical Breakdown:
- Publishing open-source repositories, portfolio presentation, and navigating AI engineering interviews.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into From Student to AI Engineer. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: Alumni Community & Continuous Learning
### 100-Point Rubric Walkthrough, Live Defense Format & Alumni Next Steps

### Technical Breakdown:
- Staying current as foundation models and protocol standards evolve in 2026 and beyond.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Alumni Community & Continuous Learning. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Annotated Code: Week 16: Capstone Demo Day & Graduation
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
2. Navigate to: Walk through the live Rubric Explorer on /enroll and present a model Capstone defense project.
3. Run baseline scenario and observe real-time telemetry.
4. Introduce deliberate edge-case error and demonstrate recovery mechanism.

<!-- Speaker Notes:
Execute live demo: Walk through the live Rubric Explorer on /enroll and present a model Capstone defense project.
-->
---

## Common Pitfalls & Production Failures
### Failure Modes in Week 16: Capstone Demo Day & Graduation

### Top 3 Production Failure Modes:
1. **Unmonitored Latency Drift:** Long-tail queries degrading P99 latency without triggering alerts.
2. **Missing Fallbacks:** Hard crashes when external dependencies experience momentary blips.
3. **Evaluation Blind Spots:** Relying on human vibes instead of automated quantitative metrics.

<!-- Speaker Notes:
Highlight how easily untested assumptions turn into midnight production outages.
-->
---

## Weekly Deliverable: Week 16: Capstone Demo Day & Graduation
### Milestone 16 Specifications

### Deliverable Requirements:
- Deliver live 15-minute Capstone defense, achieve 80+/100 score, and earn Cohort Certification.
- Unit tests passing cleanly in `pytest`.
- Verified against zero Docker and zero paid API dependencies.
- Push code to your branch `feat/w16-deliverable`.

<!-- Speaker Notes:
Emphasize the definition of done and automated test verification.
-->
---

## Week 16 Check-Out Quiz
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
