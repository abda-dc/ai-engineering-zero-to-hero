---
marp: true
theme: default
paginate: true
header: 'AI Engineering: Zero to Hero | Week 07: Prompt & Context Engineering Part B'
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
## Week 07: Prompt & Context Engineering Part B
### Prompt Chaining, ReAct Framework & Injection Red-Teaming

**Part IV: Capstone & Production** • *CH05 Companion*

### Learning Objectives:
1. Prompt Chaining Architecture: Breaking monolithic prompts into discrete, validated sequential stages....
2. The ReAct Pattern Intuition: Interleaving Thought -> Action -> Observation cycles to solve complex problems....
3. Prompt Injections & Jailbreak Vectors: Direct injections, indirect document injections, and jailbreak payloads....
4. Defensive Sanitization & Guardrails: Input sanitization layers, PII scrubbers, and dual-model evaluator architectures...

> *"Advanced prompt architectures: multi-step prompt chaining, ReAct (Reason + Act) tool reasoning, and defensive red-teaming against prompt injections."*

<!-- Speaker Notes:
Welcome cohort to Week 07: Prompt & Context Engineering Part B. Emphasize production rigor and end-to-end integration.
-->
---

## System Architecture & Mental Model
### Week 07: Prompt & Context Engineering Part B Architectural Overview

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

## Core Concept: Prompt Chaining Architecture
### Prompt Chaining, ReAct Framework & Injection Red-Teaming

### Technical Breakdown:
- Breaking monolithic prompts into discrete, validated sequential stages.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Prompt Chaining Architecture. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: The ReAct Pattern Intuition
### Prompt Chaining, ReAct Framework & Injection Red-Teaming

### Technical Breakdown:
- Interleaving Thought -> Action -> Observation cycles to solve complex problems.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into The ReAct Pattern Intuition. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: Prompt Injections & Jailbreak Vectors
### Prompt Chaining, ReAct Framework & Injection Red-Teaming

### Technical Breakdown:
- Direct injections, indirect document injections, and jailbreak payloads.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Prompt Injections & Jailbreak Vectors. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: Defensive Sanitization & Guardrails
### Prompt Chaining, ReAct Framework & Injection Red-Teaming

### Technical Breakdown:
- Input sanitization layers, PII scrubbers, and dual-model evaluator architectures.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Defensive Sanitization & Guardrails. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: Self-Consistency & Majority Voting
### Prompt Chaining, ReAct Framework & Injection Red-Teaming

### Technical Breakdown:
- Sampling multiple reasoning paths to reach robust consensus answers.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Self-Consistency & Majority Voting. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Annotated Code: Week 07: Prompt & Context Engineering Part B
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
2. Navigate to: Red-team a simulated support agent in /studio and observe guardrail intervention.
3. Run baseline scenario and observe real-time telemetry.
4. Introduce deliberate edge-case error and demonstrate recovery mechanism.

<!-- Speaker Notes:
Execute live demo: Red-team a simulated support agent in /studio and observe guardrail intervention.
-->
---

## Common Pitfalls & Production Failures
### Failure Modes in Week 07: Prompt & Context Engineering Part B

### Top 3 Production Failure Modes:
1. **Unmonitored Latency Drift:** Long-tail queries degrading P99 latency without triggering alerts.
2. **Missing Fallbacks:** Hard crashes when external dependencies experience momentary blips.
3. **Evaluation Blind Spots:** Relying on human vibes instead of automated quantitative metrics.

<!-- Speaker Notes:
Highlight how easily untested assumptions turn into midnight production outages.
-->
---

## Weekly Deliverable: Week 07: Prompt & Context Engineering Part B
### Milestone 07 Specifications

### Deliverable Requirements:
- Construct a 3-stage prompt pipeline (Extract -> Validate -> Format) with automated injection test suites.
- Unit tests passing cleanly in `pytest`.
- Verified against zero Docker and zero paid API dependencies.
- Push code to your branch `feat/w07-deliverable`.

<!-- Speaker Notes:
Emphasize the definition of done and automated test verification.
-->
---

## Week 07 Check-Out Quiz
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
