---
marp: true
theme: default
paginate: true
header: 'AI Engineering: Zero to Hero | Week 05: Inside Large Language Models'
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
## Week 05: Inside Large Language Models
### BPE Tokenization, KV Cache Math, Sampling, LoRA & Quantization

**Part IV: Capstone & Production** • *CH04 Companion*

### Learning Objectives:
1. BPE Tokenization Mechanics: Subwords, byte fallbacks, vocabulary sizing, and token boundary anomalies....
2. KV Cache Mathematics & GPU Memory: Why autoregressive generation re-computes keys and values, and how KV caching tr...
3. Sampling Strategies: Temperature, Top-k, Top-p: Controlling the probability distribution tail during autoregressive decoding....
4. LoRA: Low-Rank Adaptation: Freezing $W_0$ and training low-rank decomposition matrices $A \times B$ to cut ...

> *"Inside the modern LLM inference engine: KV Caching, Byte-Pair Encoding, parameter-efficient fine-tuning (LoRA), and AWQ/GGUF quantization."*

<!-- Speaker Notes:
Welcome cohort to Week 05: Inside Large Language Models. Emphasize production rigor and end-to-end integration.
-->
---

## System Architecture & Mental Model
### Week 05: Inside Large Language Models Architectural Overview

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

## Core Concept: BPE Tokenization Mechanics
### BPE Tokenization, KV Cache Math, Sampling, LoRA & Quantization

### Technical Breakdown:
- Subwords, byte fallbacks, vocabulary sizing, and token boundary anomalies.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into BPE Tokenization Mechanics. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: KV Cache Mathematics & GPU Memory
### BPE Tokenization, KV Cache Math, Sampling, LoRA & Quantization

### Technical Breakdown:
- Why autoregressive generation re-computes keys and values, and how KV caching trades VRAM for $O(1)$ generation speed.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into KV Cache Mathematics & GPU Memory. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: Sampling Strategies: Temperature, Top-k, Top-p
### BPE Tokenization, KV Cache Math, Sampling, LoRA & Quantization

### Technical Breakdown:
- Controlling the probability distribution tail during autoregressive decoding.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Sampling Strategies: Temperature, Top-k, Top-p. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: LoRA: Low-Rank Adaptation
### BPE Tokenization, KV Cache Math, Sampling, LoRA & Quantization

### Technical Breakdown:
- Freezing $W_0$ and training low-rank decomposition matrices $A \times B$ to cut fine-tuning VRAM by 80%.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into LoRA: Low-Rank Adaptation. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Core Concept: Model Quantization: FP16 to INT8 and INT4
### BPE Tokenization, KV Cache Math, Sampling, LoRA & Quantization

### Technical Breakdown:
- GGUF and AWQ algorithms: preserving perplexity while halving memory footprint.

### Architectural Implications:
- Enables high reliability and deterministic execution.
- Protects downstream systems from latency spikes and malformed outputs.
- Standardizes interfaces across team boundaries.

```python
# Architectural invariant
assert latency_ms < 50, 'Sub-50ms service requirement violated'
```

<!-- Speaker Notes:
Deep-dive into Model Quantization: FP16 to INT8 and INT4. Highlight trade-offs between latency, cost, and accuracy.
-->
---

## Annotated Code: Week 05: Inside Large Language Models
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
2. Navigate to: Tab 1: Tokenizer & Embedding Explorer — inspect BPE token boundaries and calculate KV cache size live.
3. Run baseline scenario and observe real-time telemetry.
4. Introduce deliberate edge-case error and demonstrate recovery mechanism.

<!-- Speaker Notes:
Execute live demo: Tab 1: Tokenizer & Embedding Explorer — inspect BPE token boundaries and calculate KV cache size live.
-->
---

## Common Pitfalls & Production Failures
### Failure Modes in Week 05: Inside Large Language Models

### Top 3 Production Failure Modes:
1. **Unmonitored Latency Drift:** Long-tail queries degrading P99 latency without triggering alerts.
2. **Missing Fallbacks:** Hard crashes when external dependencies experience momentary blips.
3. **Evaluation Blind Spots:** Relying on human vibes instead of automated quantitative metrics.

<!-- Speaker Notes:
Highlight how easily untested assumptions turn into midnight production outages.
-->
---

## Weekly Deliverable: Week 05: Inside Large Language Models
### Milestone 05 Specifications

### Deliverable Requirements:
- Complete ch04-inside-large-language-models.ipynb and calculate KV cache memory for an 8k sequence on Llama 3.
- Unit tests passing cleanly in `pytest`.
- Verified against zero Docker and zero paid API dependencies.
- Push code to your branch `feat/w05-deliverable`.

<!-- Speaker Notes:
Emphasize the definition of done and automated test verification.
-->
---

## Week 05 Check-Out Quiz
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
