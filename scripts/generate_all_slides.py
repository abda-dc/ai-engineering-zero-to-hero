#!/usr/bin/env python3
"""
Master Slide Generator for AI Engineering: Zero to Hero.
Generates all 16 Marp Markdown slide decks in slides/ directory.
"""

from pathlib import Path
import json

SLIDES_DIR = Path("slides")
SLIDES_DIR.mkdir(parents=True, exist_ok=True)

THEME_HEADER = """---
marp: true
theme: default
paginate: true
header: 'AI Engineering: Zero to Hero | {header_title}'
footer: '16-Week Intensive Cohort © 2026'
style: |
  section {{
    background-color: #0b0f19;
    color: #e2e8f0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    padding: 40px;
    font-size: 24px;
  }}
  h1 {{
    color: #38bdf8;
    font-size: 40px;
    margin-bottom: 16px;
  }}
  h2 {{
    color: #34d399;
    font-size: 30px;
    margin-bottom: 12px;
  }}
  h3 {{
    color: #a78bfa;
    font-size: 24px;
    margin-bottom: 8px;
  }}
  code {{
    background-color: #1e293b;
    color: #38bdf8;
    font-family: 'Fira Code', monospace;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.9em;
  }}
  pre {{
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 14px;
    font-size: 16px;
    line-height: 1.4;
  }}
  blockquote {{
    border-left: 4px solid #38bdf8;
    background: #1e293b;
    padding: 10px 18px;
    border-radius: 0 8px 8px 0;
    margin: 16px 0;
  }}
  footer, header {{
    color: #64748b;
    font-size: 13px;
  }}
---
"""

DECKS_DATA = [
    # Week 01
    {
        "filename": "week-01-builder-launchpad.md",
        "week": 1,
        "title": "Week 01: The Builder's Launchpad",
        "chapter": "ch00",
        "slides": [
            ("Week 01: The Builder's Launchpad", "Python OOP, REST APIs, Git Hygiene & Local Ollama",
             "### Learning Objectives:\n1. Master Object-Oriented modeling for AI components (Pipelines, Embedders, LLM Clients).\n2. Build non-blocking asynchronous REST APIs with **FastAPI**.\n3. Establish Git trunk-based branch hygiene & semantic commit standards.\n4. Set up local zero-cost LLM inference via **Ollama** (`llama3.2:3b`, `qwen2.5:7b`).\n\n> *\"An AI Engineer is first and foremost a rigorous software engineer who treats model calls as unreliable network RPCs.\"*",
             "Welcome students to Week 1. Emphasize software craftsmanship and setting up local-first tooling."),
            ("Architecture: The Modern AI Engineering Stack", "Local-First Development & Deployment Topology",
             "```\n+-------------------------------------------------------------+\n|                    Client UI Layer                          |\n|           (Next.js App Router / Desktop Agent)              |\n+-----------------------------+-------------------------------+\n                              | JSON-RPC / SSE Stream\n+-----------------------------v-------------------------------+\n|               FastAPI Application Gateway                   |\n|        (Pydantic Validation, Rate Limiter, Cache)           |\n+--------------+------------------------------+---------------+\n               |                              |\n+--------------v--------------+ +-------------v---------------+\n|    Local Ollama Inference   | |    Embedded State Layer     |\n| (llama3.2:3b / qwen2.5:7b)  | |  (SQLite Progress & Vector) |\n+-----------------------------+ +-----------------------------+\n```",
             "Walk through each tier. Point out that the architecture works completely offline without cloud API keys."),
            ("OOP System Modeling for AI Components", "Abstracting Volatile Foundation Models",
             "### Why Polymorphic Interfaces Matter:\n- Wrap external model providers behind a uniform contract.\n- Decouple prompt formulation from execution runtime.\n\n```python\nfrom abc import ABC, abstractmethod\n\nclass BaseLLMClient(ABC):\n    @abstractmethod\n    async def generate(self, prompt: str, **kwargs) -> str:\n        \"\"\"Generate text completion.\"\"\"\n        pass\n```\n- Swap between Ollama, vLLM, and Claude with **zero downstream code changes**.",
             "Explain how hardcoding vendor SDKs creates technical debt. BaseLLMClient allows seamless mocking and switching."),
            ("Asynchronous REST with FastAPI", "Non-Blocking I/O for High-Latency LLMs",
             "### Concurrency Under High-Latency Calls:\n- LLM generations take 500ms to 5000ms.\n- Synchronous worker threads deplete rapidly under modest loads.\n- `async / await` frees the Python event loop during network socket I/O.\n\n```python\n@app.post('/api/generate')\nasync def generate_response(req: PromptRequest):\n    # Non-blocking async HTTP call to local Ollama daemon\n    response = await ollama_client.generate(req.prompt)\n    return {'status': 'success', 'data': response}\n```",
             "Explain the difference between CPU-bound and I/O-bound workloads in Python. LLM calls are almost entirely I/O-bound."),
            ("Local Zero-Cost Inference with Ollama", "Running 3B and 7B Models on Everyday Laptops",
             "### Why Local Models in 2026?\n- **Zero API Bill:** Run 10,000 automated unit tests without paying OpenAI/Anthropic.\n- **Absolute Privacy:** Sensitive code and customer data never leave `localhost`.\n\n```bash\n# Pull required course models\nollama pull llama3.2:3b    # Fast 3B model (2.0 GB VRAM)\nollama pull qwen2.5:7b     # High-reasoning 7B model (4.7 GB VRAM)\n\n# Test HTTP inference directly\ncurl -s http://localhost:11434/api/generate -d '{\n  \"model\": \"llama3.2:3b\",\n  \"prompt\": \"What is AI engineering in 10 words?\",\n  \"stream\": false\n}'\n```",
             "Show the terminal commands. Highlight that llama3.2:3b runs at over 40 tokens/sec on standard M-series Macs or NVIDIA RTX GPUs."),
            ("Annotated Code: Streaming Ollama Client", "Processing Tokens in Real Time",
             "```python\nimport httpx\nimport json\nfrom typing import AsyncGenerator\n\nclass LocalOllamaClient:\n    def __init__(self, base_url: str = 'http://localhost:11434'):\n        self.base_url = base_url\n\n    async def stream(self, prompt: str, model: str = 'llama3.2:3b') -> AsyncGenerator[str, None]:\n        async with httpx.AsyncClient(timeout=30.0) as client:\n            async with client.stream(\n                'POST',\n                f'{self.base_url}/api/generate',\n                json={'model': model, 'prompt': prompt, 'stream': True}\n            ) as resp:\n                async for line in resp.aiter_lines():\n                    if line:\n                        chunk = json.loads(line)\n                        yield chunk.get('response', '')\n```",
             "Explain line-by-line streaming. Explain that aiter_lines() allows piping tokens directly into FastAPI's StreamingResponse."),
            ("Live Demo Cue: Studio & Environment", "Instructor Live Walkthrough Steps",
             "### Instructor Live Execution:\n1. Verify local backend: `curl.exe http://127.0.0.1:8000/api/health`\n2. Verify local Ollama: `curl.exe http://localhost:11434/api/tags`\n3. Open `http://localhost:3000` to show the Mastery Dashboard.\n4. Walk through Chapter 00 in the Interactive Reader (`/chapters/ch00`).\n5. Open `http://localhost:3000/studio` to preview live tabs.\n6. Show Google Colab one-click launch badge.",
             "Switch to browser and terminal to demonstrate these live steps. Encourage students to follow along on their machines."),
            ("Common Pitfalls & Failure Modes", "What Breaks in Production Systems",
             "### Top 3 Week 1 Traps:\n1. **Unbounded Input Length:** Users submitting 500kb prompts causing out-of-memory crashes on small models.\n   - *Fix:* Enforce Pydantic `Field(..., max_length=2000)`.\n2. **Synchronous Requests in Async Routes:** Calling `requests.post()` inside `async def` blocks the entire server event loop.\n   - *Fix:* Always use `httpx.AsyncClient`.\n3. **Unquoted Windows Paths with Spaces:** Path errors in PowerShell.\n   - *Fix:* Always quote `\"C:\\Users\\...\\ai-engineering-zero to hero\"`.",
             "Warn students about GIL locking when mixing sync HTTP libraries inside async routes."),
            ("Weekly Deliverable: The Builder Launchpad", "Capstone Milestone 01",
             "### Deliverable Requirements:\n- Complete `book/chapters/part1-foundations/ch00-builder-launchpad.ipynb`.\n- Implement a verified FastAPI microservice with:\n  1. `GET /api/health` checking database and Ollama availability.\n  2. `POST /api/llm/chat` with Pydantic validation and local model routing.\n  3. Passing test suite with `pytest`.\n- Push code to your branch `feat/w01-launchpad`.",
             "Reiterate definition of done: notebook runs top-to-bottom with zero errors and pytest passes."),
            ("Week 01 Check-Out Quiz", "Review & Consolidation",
             "### Knowledge Check:\n1. **Why must LLM endpoints use asynchronous I/O in FastAPI?**\n   - *Answer:* LLM calls are I/O-bound with high latency. Async avoids thread-pool exhaustion.\n2. **What does Ollama's `stream: false` parameter do?**\n   - *Answer:* Blocks until the complete response is generated and returns one aggregated JSON payload.\n3. **Why do we separate model client logic from API routing logic?**\n   - *Answer:* Modularity, ease of unit testing via mocks, and zero vendor lock-in.",
             "Quiz students interactively before closing the session.")
        ]
    },

    # Week 02
    {
        "filename": "week-02-math-and-high-dim-geometry.md",
        "week": 2,
        "title": "Week 02: Math & High-Dimensional Geometry",
        "chapter": "ch01",
        "slides": [
            ("Week 02: Math & High-Dimensional Geometry", "Vectors, Cosine Similarity, Gradients & Bayes Theorem",
             "### Learning Objectives:\n1. Geometric intuition of high-dimensional embedding spaces ($\\mathbb{R}^d$).\n2. Mathematical formulation: Dot Product vs. Cosine Similarity vs. L2 Distance.\n3. The Curse of Dimensionality in vector search.\n4. Gradient Descent optimization and Bayesian inference principles.\n\n> *\"If you don't understand high-dimensional geometry, vector databases will always feel like black magic.\"*",
             "Frame this week around intuition over dry derivations. Vector math is the physical law of modern AI."),
            ("Mental Model: High-Dimensional Embeddings", "Direction Encodes Semantic Meaning",
             "```\n              Dimension 2 (e.g. \"Royalty\")\n              ^\n              |         [King] *          * [Queen]\n              |                   \\        /\n              |                    \\      /\n              |        [Man] *      \\    /    * [Woman]\n              +----------------------\\--/------------> Dimension 1 (e.g. \"Gender\")\n                                      \\/\n                   Vector offset: (King - Man + Woman ≈ Queen)\n```\n- Distance represents dissimilarity.\n- Angle represents semantic orientation.",
             "Point out that semantic vector spaces possess arithmetic properties discovered by Mikolov in 2013."),
            ("Dot Product vs. Cosine Distance", "Formulas & Production Tradeoffs",
             "### Dot Product:\n$$\\mathbf{u} \\cdot \\mathbf{v} = \\sum_{i=1}^d u_i v_i = \\|\\mathbf{u}\\| \\|\\mathbf{v}\\| \\cos \\theta$$\n- Measures both **alignment and magnitude** (longer text has larger magnitude).\n\n### Cosine Similarity:\n$$\\text{Cosine}(\\mathbf{u}, \\mathbf{v}) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{\\|\\mathbf{u}\\| \\|\\mathbf{v}\\|} = \\cos \\theta \\in [-1, 1]$$\n- Purely directional; invariant to document length.\n- *Pro Tip:* If vectors are unit-normalized ($\\left\\|\\mathbf{v}\\right\\| = 1$), dot product **equals** cosine similarity!",
             "Emphasize the performance win: pre-normalizing vectors turns cosine calculation into a pure dot product (saving square roots)."),
            ("The Curse of Dimensionality", "Why High-D Spaces Defy Intuition",
             "### Counter-Intuitive Properties of $\\mathbb{R}^{1536}$:\n1. **Distance Concentration:** As $d \\to \\infty$, the distance between the nearest and farthest vector converges to the average distance.\n2. **Empty Volume:** 99.99% of the volume of a high-dimensional hypersphere resides in an infinitesimally thin outer shell.\n3. **Brute-Force Search Collapses:** Scanning 10M vectors linearly ($O(N \\cdot d)$) creates massive latency spikes.\n- *Solution:* Approximate Nearest Neighbor (ANN) indexing (HNSW, IVF).",
             "Explain why vector databases exist: standard B-trees cannot index multi-dimensional vectors."),
            ("Gradients & Loss Optimization", "How Models Update Parameters",
             "### The Optimization Equation:\n$$\\mathbf{w}_{t+1} = \\mathbf{w}_t - \\eta \\nabla L(\\mathbf{w}_t)$$\n- $\\nabla L$: Gradient vector of partial derivatives pointing uphill.\n- $\\eta$: Learning rate scaling step size.\n- *Intuition:* A ball rolling downhill along the surface of minimum error.",
             "Connect gradient descent to fine-tuning (LoRA in Week 5). You don't derive Jacobians by hand, but you monitor loss curves."),
            ("Bayes' Theorem in Search & Retrieval", "Updating Probabilities with New Evidence",
             "$$P(Relevant \\mid Query) = \\frac{P(Query \\mid Relevant) \\cdot P(Relevant)}{P(Query)}$$\n\n### Application in Hybrid RAG:\n- **Prior $P(Relevant)$:** Base popularity or authority of a document.\n- **Likelihood $P(Query \\mid Relevant)$:** Match frequency of query keywords.\n- **Posterior:** Final reranked confidence score.",
             "Show how Bayesian probability underpins BM25 and cross-encoder rerankers."),
            ("Annotated Code: Vector Math from Scratch", "Pure NumPy Implementation",
             "```python\nimport numpy as np\n\ndef cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:\n    \"\"\"Numerically stable cosine similarity.\"\"\"\n    norm_u = np.linalg.norm(u)\n    norm_v = np.linalg.norm(v)\n    if norm_u == 0.0 or norm_v == 0.0:\n        return 0.0\n    return float(np.dot(u, v) / (norm_u * norm_v))\n\ndef unit_normalize_rows(matrix: np.ndarray) -> np.ndarray:\n    \"\"\"Normalize embedding matrix for rapid dot-product search.\"\"\"\n    norms = np.linalg.norm(matrix, axis=1, keepdims=True)\n    norms[norms == 0.0] = 1.0\n    return matrix / norms\n```",
             "Walk through zero-norm handling. Show how keepdims=True enables vectorized matrix operations."),
            ("Live Demo Cue: Vector Projection Studio", "Hands-on Studio Walkthrough",
             "### Instructor Demo Steps:\n1. Open `http://localhost:3000/studio` -> **Tab 1: Tokenizer & Embedding Explorer**.\n2. Enter pairs of synonymous vs. antonymous sentences.\n3. Inspect the 2D projection scatter plot.\n4. Demonstrate how changing a single keyword rotates the embedding vector in geometric space.",
             "Demonstrate live in browser. Show the cosine matrix heatmap updating in real time."),
            ("Common Pitfalls & Numerical Bugs", "Production Bugs in Vector Math",
             "1. **NaN Infiltration:** Un-clamped division by zero spreads `NaN` across entire index batches.\n2. **Mixing Normalized and Un-Normalized Vectors:** Yields distorted search rankings.\n3. **Mismatched Dimensionality:** Querying a 768-dim index with a 1536-dim embedding model causes runtime dimensional mismatch crashes.",
             "Stress that embedding models cannot be swapped without rebuilding the entire vector index."),
            ("Weekly Deliverable: Math & Vectors", "Capstone Milestone 02",
             "### Deliverable Requirements:\n- Complete `book/chapters/part1-foundations/ch01-math-and-stats-intuition.ipynb`.\n- Implement:\n  1. Vector distance metrics (Cosine, Euclidean, Manhattan).\n  2. Pairwise similarity matrix generator.\n  3. Simple 1D gradient descent simulator.\n- Verify with `python scripts/verify_notebooks.py`.",
             "Check that students verify both unit tests and notebook cells."),
            ("Week 02 Check-Out Quiz", "Review & Consolidation",
             "1. **What is the cosine similarity of orthogonal vectors?**\n   - *Answer:* `0.0` (90-degree angle).\n2. **Why does unit-normalizing vectors speed up search?**\n   - *Answer:* Eliminates runtime norm calculations; similarity equals a simple dot product.\n3. **What is the range of cosine distance ($1 - \\text{similarity}$)?**\n   - *Answer:* $[0.0, 2.0]$.",
             "Recap key takeaways and set expectations for Week 3.")
        ]
    },

    # Week 03
    {
        "filename": "week-03-classical-ml-bridge.md",
        "week": 3,
        "title": "Week 03: The Classical Machine Learning Bridge",
        "chapter": "ch02",
        "slides": [
            ("Week 03: The Classical Machine Learning Bridge", "Loss Curves, Overfitting, Regularization & Cross-Validation",
             "### Learning Objectives:\n1. Understand Supervised vs. Unsupervised paradigms in the age of LLMs.\n2. Diagnose model health via **Loss Curves** (Underfitting vs. Overfitting).\n3. Apply **L1 (Lasso)** and **L2 (Ridge)** regularization principles.\n4. Establish rigorous **k-Fold Cross-Validation** to prevent data leakage.\n\n> *\"Before generating tokens, an AI engineer must know whether a simple logistic regression or decision tree solves the business problem with 100x lower latency.\"*",
             "Position classical ML as a vital baseline. Not every problem needs an LLM."),
            ("Mental Model: The Bias-Variance Tradeoff", "Generalization vs. Memorization",
             "```\nHigh Loss ^\n          |      \\  Validation Loss (High Variance / Overfitting)\n          |       \\       /\n          |        \\_____/\n          |         \\   /\n          |          \\ /  Training Loss (Memorization)\n          |           v__________________\n          +-----------------------------------> Model Complexity / Epochs\n              Underfitting         Sweet Spot          Overfitting\n```\n- **Underfitting (High Bias):** Model too simple to capture patterns.\n- **Overfitting (High Variance):** Model memorizes training noise.",
             "Explain how this curve applies to LLM fine-tuning and classical ML alike."),
            ("Loss Curves Diagnostics", "Reading Training Dynamics Like an EKG",
             "### Common Scenarios:\n- **Scenario A:** Both train and val loss stay high $\\to$ Learning rate too low or model capacity insufficient.\n- **Scenario B:** Train loss drops to 0, val loss explodes $\\to$ Severe overfitting. Add dropout / weight decay.\n- **Scenario C:** Loss oscillates erratically $\\to$ Learning rate too high (stepping over minima).\n- **Scenario D:** Train and val decrease together $\\to$ Healthy convergence.",
             "Train students to diagnose training runs before spending hours on compute."),
            ("Regularization: Taming Complexity", "L1 (Lasso) vs. L2 (Ridge) vs. Dropout",
             "### Formulations:\n- **L1 Regularization (Lasso):**\n  $$L_{reg} = L_0 + \\lambda \\sum |w_i|$$\n  *Property:* Drives uninformative weights to **exact zero** (feature selection).\n- **L2 Regularization (Ridge / Weight Decay):**\n  $$L_{reg} = L_0 + \\lambda \\sum w_i^2$$\n  *Property:* Shrinks weights smoothly; prevents single dominant features.\n- **Dropout:** Randomly deactivates neurons during forward pass to force redundant representations.",
             "Connect L2 regularization to weight decay in AdamW (the default optimizer for Transformers)."),
            ("Cross-Validation & Data Leakage", "Preventing Metric Hallucinations",
             "```\nDataset [====================================================]\n\nFold 1:  [ Val  ] [ Train ] [ Train ] [ Train ] [ Train ]\nFold 2:  [ Train ] [ Val  ] [ Train ] [ Train ] [ Train ]\nFold 3:  [ Train ] [ Train ] [ Val  ] [ Train ] [ Train ]\nFold 4:  [ Train ] [ Train ] [ Train ] [ Val  ] [ Train ]\nFold 5:  [ Train ] [ Train ] [ Train ] [ Train ] [ Val  ]\n```\n### The Cardinal Sin: Data Leakage\n- Normalizing or imputing data **before** splitting folds leaks test distributions into training.",
             "Stress that evaluating on leaked test data gives false confidence before production deployment."),
            ("Classical Baselines for AI Systems", "When NOT to Use an LLM",
             "| Feature | Classical ML (scikit-learn) | Large Language Model |\n| :--- | :--- | :--- |\n| **Latency** | 1 - 5 ms | 500 - 3000 ms |\n| **Cost per 1M calls**| \\$0.01 (CPU server) | \\$5.00 - \\$30.00 |\n| **Determinism** | 100% deterministic | Probabilistic |\n| **Training Data** | Requires labeled tables | Zero/Few-shot |\n| **Use Cases** | Fraud score, churn, intent routing | Summaries, code, reasoning |",
             "Teach students to use cheap classifiers as first-stage routers in AI pipelines."),
            ("Annotated Code: scikit-learn Pipeline", "Robust Leak-Free Modeling",
             "```python\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import cross_val_score\n\n# Construct pipeline ensuring transformation occurs inside cross-validation\npipeline = Pipeline([\n    ('scaler', StandardScaler()),\n    ('classifier', LogisticRegression(C=1.0, penalty='l2'))\n])\n\nscores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='f1_macro')\nprint(f'Mean CV F1 Score: {scores.mean():.4f} (+/- {scores.std():.4f})')\n```",
             "Explain why Pipeline prevents leakage: scaling parameters fit ONLY on training folds."),
            ("Live Demo Cue: Overfitting in Action", "Interactive Colab Walkthrough",
             "### Instructor Live Demo Steps:\n1. Open `book/chapters/part1-foundations/ch02-classical-ml-bridge.ipynb`.\n2. Fit a high-degree polynomial regressor ($degree = 15$) on 20 noisy data points.\n3. Show the wild oscillation between data points (overfitting).\n4. Apply L2 Ridge penalty and show the curve smoothly regularizing.",
             "Demonstrate how easy it is to overfit small datasets."),
            ("Common Pitfalls & Production Bugs", "Classical ML Traps",
             "1. **Evaluating on Training Data:** Reporting 99.8% training accuracy to stakeholders.\n2. **Ignoring Class Imbalance:** Accuracy is misleading when 99% of samples belong to the majority class.\n3. **Feature Store Drift:** Training features computed differently from real-time production features.",
             "Remind students: accuracy on unbalanced fraud data is a dangerous vanity metric."),
            ("Weekly Deliverable: Classical ML Bridge", "Capstone Milestone 03",
             "### Deliverable Requirements:\n- Complete `ch02-classical-ml-bridge.ipynb`.\n- Implement:\n  1. Train/Val/Test split with stratification.\n  2. Cross-validated baseline classifier.\n  3. Loss curve plotting function comparing unregularized vs. regularized models.\n- Push verified code to your branch `feat/w03-classical-ml`.",
             "Encourage students to inspect feature importances."),
            ("Week 03 Check-Out Quiz", "Review & Consolidation",
             "1. **What does a diverging validation loss indicate while training loss decreases?**\n   - *Answer:* Overfitting.\n2. **Why does L1 regularization create sparse weights?**\n   - *Answer:* The diamond constraint surface touches loss contours at axes where weights are zero.\n3. **Why should data scaling occur inside the cross-validation loop?**\n   - *Answer:* To prevent test set distribution metrics from leaking into the training step.",
             "Conclude Part I: Foundations. Preview Part II: Core Generative AI.")
        ]
    },

    # Week 04
    {
        "filename": "week-04-generative-ai-foundations.md",
        "week": 4,
        "title": "Week 04: Generative AI Foundations",
        "chapter": "ch03",
        "slides": [
            ("Week 04: Generative AI Foundations", "GenAI vs. Discriminative, Self-Attention & RLHF",
             "### Learning Objectives:\n1. Contrast Generative ($P(X, Y)$) vs. Discriminative ($P(Y \\mid X)$) models.\n2. Deconstruct the **Transformer Architecture** and the **Self-Attention Mechanism**.\n3. Understand Pre-training vs. Supervised Fine-Tuning (SFT) vs. RLHF.\n4. Explore Multimodal foundation models and AI safety alignment.\n\n> *\"Attention is not just an algorithm; it is dynamic content-based routing across a vector space.\"*",
             "Welcome students to Part II. Today we dive into the core engine of modern LLMs."),
            ("Mental Model: The Self-Attention Mechanism", "Queries, Keys, and Values",
             "```\nQuery (What I'm looking for)  Key (What I contain)  Value (What I communicate)\n         Q                          K                          V\n         |                          |                          |\n         +------------x-------------+                          |\n                      | (Dot Product)                          |\n                      v                                        |\n               Raw Attention Scores                            |\n                      | (Scale by sqrt(d_k) & Softmax)         |\n                      v                                        |\n               Attention Weights [0, 1]                        |\n                      |                                        |\n                      +-------------------x--------------------+\n                                          |\n                                          v\n                                Contextual Output Vector\n```",
             "Walk through the filing cabinet analogy: Query is your search term, Key is the folder label, Value is the folder content."),
            ("The Mathematical Equation of Attention", "Scaled Dot-Product Attention",
             "$$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{Q K^T}{\\sqrt{d_k}}\\right) V$$\n\n### Why the $\\sqrt{d_k}$ Scaling Factor?\n- When dimensionality $d_k$ is large, dot products grow large in magnitude.\n- Large values push the softmax function into regions with near-zero gradients (saturation).\n- Dividing by $\\sqrt{d_k}$ stabilizes numerical gradients during backpropagation.",
             "Ask students what happens when softmax saturates: gradients vanish and learning halts."),
            ("Multi-Head Attention (MHA)", "Attending to Multiple Subspaces in Parallel",
             "### Why Multiple Heads?\n- A single attention head only tracks one type of relationship (e.g. subject-verb agreement).\n- **Multi-Head Attention** projects Q, K, V into $h$ distinct representation subspaces:\n$$\\text{MHA}(Q, K, V) = \\text{Concat}(\\text{head}_1, \\dots, \\text{head}_h) W^O$$\n- Head 1 might track syntax, Head 2 tracks coreference ('it' $\\to$ 'robot'), Head 3 tracks semantics.",
             "Show how parallel heads give the network rich expressive capacity across different linguistic dimensions."),
            ("The LLM Training Lifecycle", "From Raw Text to Helpful Assistant",
             "```\n1. Pre-training (99% of compute)\n   Raw Internet Text -> Base Model (Next-token prediction: \"The capital is...\")\n\n2. Supervised Fine-Tuning / SFT (1% of compute)\n   Curated QA Dialogues -> Instruction Model (\"User: Summarize this...\")\n\n3. Preference Alignment (RLHF / DPO)\n   Human / AI Feedback -> Aligned Assistant (Helpful, Honest, Harmless)\n```",
             "Clarify the difference between a raw Base model (which continues text) and an Instruct model (which answers questions)."),
            ("Multimodal Foundations & AI Safety", "Vision, Audio & Alignment Boundaries",
             "### Multimodality:\n- Project image patch tokens (Vision Transformers / ViT) into the same embedding space as text tokens.\n- Allows joint cross-attention across images and text.\n\n### Safety Guardrails:\n- Red-teaming against prompt injections and jailbreaks.\n- Toxicity classifiers and output filtering.",
             "Preview Chapter 05 red-teaming and Chapter 12 safety audits."),
            ("Annotated Code: Scaled Dot-Product Attention", "Pure PyTorch Implementation",
             "```python\nimport torch\nimport torch.nn.functional as F\n\ndef scaled_dot_product_attention(Q, K, V, mask=None):\n    \"\"\"Compute scaled dot-product attention weights and output.\"\"\"\n    d_k = Q.size(-1)\n    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k ** 0.5)\n    \n    if mask is not None:\n        scores = scores.masked_fill(mask == 0, -1e9)\n        \n    weights = F.softmax(scores, dim=-1)\n    output = torch.matmul(weights, V)\n    return output, weights\n```",
             "Point out the causal mask logic: -1e9 becomes exact zero after softmax, preventing models from looking ahead."),
            ("Live Demo Cue: Studio Attention Explorer", "Visualizing Token Interaction",
             "### Instructor Live Demo Steps:\n1. Open `http://localhost:3000/studio` -> **Tab 1: Tokenizer & Embedding Explorer**.\n2. Input sentence: *'The animal didn't cross the street because it was too tired.'*\n3. Inspect token split and show how *'it'* attends heavily to *'animal'*.\n4. Change to *'it was too wide'* and show how *'it'* shifts attention to *'street'*.",
             "This Winograd schema demonstration visually proves how attention resolves pronouns contextually."),
            ("Common Pitfalls in Generative AI", "Production Realities",
             "1. **Treating LLM Output as Fact:** Hallucinations occur because models optimize next-token likelihood, not truth.\n2. **Confusing Base and Instruct Models:** Deploying a base model leads to repetitive completion loops.\n3. **Quadratic Sequence Memory:** Attention memory scales as $O(N^2)$ with sequence length $N$.",
             "Warn students about memory explosion when scaling context length."),
            ("Weekly Deliverable: Generative Foundations", "Capstone Milestone 04",
             "### Deliverable Requirements:\n- Complete `book/chapters/part2-core-genai/ch03-generative-ai-foundations.ipynb`.\n- Implement:\n  1. Multi-head self-attention module in PyTorch.\n  2. Causal masking for autoregressive decoders.\n  3. Softmax temperature experiment.\n- Push code to `feat/w04-genai-foundations`.",
             "Encourage students to inspect intermediate attention matrices."),
            ("Week 04 Check-Out Quiz", "Review & Consolidation",
             "1. **Why is the dot product divided by $\\sqrt{d_k}$ in self-attention?**\n   - *Answer:* Prevents large dot products from saturating softmax gradients.\n2. **What is the difference between SFT and RLHF?**\n   - *Answer:* SFT teaches task format via demonstration; RLHF steers outputs toward human preference.\n3. **Why does causal masking use $-10^9$ before softmax?**\n   - *Answer:* $e^{-10^9} \\approx 0$, ensuring future tokens have zero attention weight.",
             "Conclude Week 4. Next week: deep dive inside the Transformer decoder and KV cache.")
        ]
    }
]

# We generate weeks 5 through 16 dynamically with the same standard
REMAINING_WEEKS = [
    (5, "week-05-inside-large-language-models.md", "Week 05: Inside Large Language Models", "ch04",
     "BPE Tokenization, KV Cache Math, Sampling, LoRA & Quantization",
     "Inside the modern LLM inference engine: KV Caching, Byte-Pair Encoding, parameter-efficient fine-tuning (LoRA), and AWQ/GGUF quantization.",
     [
         ("BPE Tokenization Mechanics", "Subwords, byte fallbacks, vocabulary sizing, and token boundary anomalies."),
         ("KV Cache Mathematics & GPU Memory", "Why autoregressive generation re-computes keys and values, and how KV caching trades VRAM for $O(1)$ generation speed."),
         ("Sampling Strategies: Temperature, Top-k, Top-p", "Controlling the probability distribution tail during autoregressive decoding."),
         ("LoRA: Low-Rank Adaptation", "Freezing $W_0$ and training low-rank decomposition matrices $A \\times B$ to cut fine-tuning VRAM by 80%."),
         ("Model Quantization: FP16 to INT8 and INT4", "GGUF and AWQ algorithms: preserving perplexity while halving memory footprint.")
     ],
     "Tab 1: Tokenizer & Embedding Explorer — inspect BPE token boundaries and calculate KV cache size live.",
     "Complete ch04-inside-large-language-models.ipynb and calculate KV cache memory for an 8k sequence on Llama 3."),

    (6, "week-06-prompt-and-context-part-a.md", "Week 06: Prompt & Context Engineering Part A", "ch05",
     "Prompt Anatomy, System Roles, CoT, Delimiters & Pydantic JSON",
     "Systematic prompt engineering: anatomy of production prompts, delimiter isolation, chain-of-thought, and guaranteed Pydantic JSON schemas.",
     [
         ("Anatomy of an Enterprise System Prompt", "Role framing, task constraints, output specifications, and defensive boundaries."),
         ("Delimiters & Input Isolation", "Using XML tags (`<context>`, `<query>`) to prevent structural confusion."),
         ("Chain-of-Thought (CoT) Reasoning", "Zero-shot CoT ('Think step by step') vs. Few-shot exemplars to boost reasoning accuracy."),
         ("Structured JSON Outputs via Pydantic", "Enforcing strict schema contracts via JSON Schema and grammar-guided decoding."),
         ("Context Window Packing & Truncation", "Strategies for handling long conversations without blowing token budgets.")
     ],
     "Test prompt delimiters and schema validation live using local Ollama model in /api/llm/chat.",
     "Build a typed Pydantic extractor that parses unstructured customer support transcripts into JSON."),

    (7, "week-07-prompt-and-context-part-b.md", "Week 07: Prompt & Context Engineering Part B", "ch05",
     "Prompt Chaining, ReAct Framework & Injection Red-Teaming",
     "Advanced prompt architectures: multi-step prompt chaining, ReAct (Reason + Act) tool reasoning, and defensive red-teaming against prompt injections.",
     [
         ("Prompt Chaining Architecture", "Breaking monolithic prompts into discrete, validated sequential stages."),
         ("The ReAct Pattern Intuition", "Interleaving Thought -> Action -> Observation cycles to solve complex problems."),
         ("Prompt Injections & Jailbreak Vectors", "Direct injections, indirect document injections, and jailbreak payloads."),
         ("Defensive Sanitization & Guardrails", "Input sanitization layers, PII scrubbers, and dual-model evaluator architectures."),
         ("Self-Consistency & Majority Voting", "Sampling multiple reasoning paths to reach robust consensus answers.")
     ],
     "Red-team a simulated support agent in /studio and observe guardrail intervention.",
     "Construct a 3-stage prompt pipeline (Extract -> Validate -> Format) with automated injection test suites."),

    (8, "week-08-vector-databases-and-ann-search.md", "Week 08: Vector Databases & ANN Search", "ch06",
     "HNSW Graphs, IVF Voronoi, Product Quantization & pgvector",
     "Vector database internals: why flat search fails at scale, graph-based HNSW traversal, IVF clustering, and deploying pgvector and Qdrant.",
     [
         ("The Scalability Problem of Flat Search", "$O(N \\cdot d)$ search complexity and why linear scans collapse beyond 100k vectors."),
         ("HNSW: Hierarchical Navigable Small World", "Skip-list graph indexing: logarithmic $O(\\log N)$ nearest neighbor discovery."),
         ("IVF: Inverted File Indexing", "Partitioning vector space into Voronoi centroids to restrict search space."),
         ("Product Quantization (PQ)", "Compressing high-dimensional vectors into compact sub-vector codebooks."),
         ("pgvector & Qdrant in Production", "Relational metadata filtering + vector ANN in a unified SQL or dedicated engine.")
     ],
     "Tab 2: RAG Chunking & Retrieval Debugger — benchmark search latency across flat vs. indexed stores.",
     "Deploy a local pgvector SQLite/Docker instance, index 10,000 synthetic embeddings, and measure recall vs. QPS."),

    (9, "week-09-data-engineering-for-ai.md", "Week 09: Data Engineering for AI Systems", "ch07",
     "ETL/ELT Pipelines, Document Parsing, Feature Stores & DVC",
     "Data pipelines for AI: document ingestion, PDF/OCR extraction, chunk deduplication, feature stores, and dataset versioning with DVC.",
     [
         ("The AI Data Lifecycle", "Ingestion, normalization, deduplication, chunking, embedding, and continuous indexing."),
         ("Unstructured Document Parsing", "Handling multi-column PDFs, tables, markdown headers, and OCR noise."),
         ("Deduplication & Content Hashing", "MinHash and perceptual hashing to prevent indexing duplicate passages."),
         ("Feature Stores for AI", "Bridging online low-latency inference with offline historical model evaluation."),
         ("Data Versioning with DVC", "Tracking large dataset hashes alongside Git commits for 100% reproducible experiments.")
     ],
     "Run scripts/sync_notebooks_to_app.py to observe deterministic curriculum compilation.",
     "Build an idempotent document ingestion pipeline that extracts, normalizes, and hashes 20 PDF documents."),

    (10, "week-10-production-rag-systems-part-a.md", "Week 10: Production RAG Systems Part A", "ch08",
     "Semantic Chunking, Hybrid BM25 Search & Cross-Encoder Reranking",
     "Production RAG core: chunking strategies, combining dense semantic search with sparse BM25, Reciprocal Rank Fusion, and cross-encoder reranking.",
     [
         ("Why Naive RAG Fails in Production", "Chunk fragmentation, semantic drift, missing context, and retrieval hallucinations."),
         ("Chunking Strategies", "Fixed sliding window vs. recursive markdown character vs. semantic boundary chunking."),
         ("Hybrid Retrieval Architecture", "Combining sparse keyword precision (BM25) with dense semantic recall (HNSW)."),
         ("Reciprocal Rank Fusion (RRF)", "Rank-based score normalization without calibrating score scales ($RRF = \\sum \\frac{1}{k + r_i}$)."),
         ("Cross-Encoder Reranking", "Joint query-passage attention scoring to isolate true needle-in-the-haystack passages.")
     ],
     "Tab 2: RAG Chunking & Retrieval Debugger — adjust Alpha slider live to compare BM25 vs. Dense vs. Hybrid.",
     "Implement a hybrid retriever with RRF and a cross-encoder reranking stage in ch08-production-rag-systems.ipynb."),

    (11, "week-11-production-rag-systems-part-b.md", "Week 11: Production RAG Systems Part B", "ch08",
     "Multi-Hop RAG, GraphRAG, Inline Citations & Ragas Evals",
     "Advanced RAG architectures: multi-hop query decomposition, Knowledge Graph RAG, strict bracketed citations, and automated Ragas evaluation.",
     [
         ("Multi-Hop Query Decomposition", "Splitting complex comparative questions into sub-queries for multi-step retrieval."),
         ("GraphRAG Fundamentals", "Extracting entity-relationship graphs to capture cross-document global themes."),
         ("Inline Citations & Grounding", "Guaranteed bracketed citations `[1][2]` tied strictly to retrieved source spans."),
         ("The RAG Triad Evals", "Context Precision, Faithfulness (groundedness), and Answer Relevance."),
         ("Ragas & DeepEval in CI/CD", "Automated regression gates preventing bad chunking or prompt drift.")
     ],
     "Inspect citation grounding and run automated RAG Triad benchmark on sample enterprise QA pairs.",
     "Evaluate a RAG pipeline on 30 test questions using Ragas metrics and enforce >0.85 faithfulness threshold."),

    (12, "week-12-autonomous-ai-agents.md", "Week 12: Autonomous AI Agents", "ch09",
     "ReAct Loops, LangGraph State Machines, Memory & Human-in-the-Loop",
     "Agentic architectures: ReAct loop mechanics, cyclical state graphs with LangGraph, episodic/working memory, and human approval checkpoints.",
     [
         ("Agent Anatomy: Think -> Act -> Observe", "How agents reason over tools, execute actions, and incorporate real-world feedback."),
         ("LangGraph Architecture", "Cyclical state graphs, nodes, conditional edges, and state persistence."),
         ("Memory Systems", "Working scratchpad (in-context), short-term buffer, and long-term vector/SQL episodic memory."),
         ("Tool & Function Calling", "Pydantic JSON schema declaration and structured tool dispatch."),
         ("Human-in-the-Loop (HITL)", "Interrupting execution graph at sensitive nodes for human approval before write operations.")
     ],
     "Tab 3: LangGraph Agent Flow Visualizer — execute multi-step research agent and watch cyclical state updates.",
     "Build an autonomous multi-step code execution agent using LangGraph with human confirmation checkpoint."),

    (13, "week-13-model-context-protocol-mcp.md", "Week 13: Model Context Protocol (MCP)", "ch10",
     "The N×M Problem, JSON-RPC 2.0, Tools/Resources/Prompts & MCP Inspector",
     "The Model Context Protocol: solving $N \\times M$ agent integration, JSON-RPC 2.0 specification, building MCP Servers with official SDKs, and security.",
     [
         ("The $N \\times M$ Integration Crisis", "Why every agent connecting to every API independently causes ecosystem fragmentation."),
         ("MCP Architecture & Topology", "Host Clients (Cursor, Claude Desktop), Client proxies, and standard MCP Servers."),
         ("Core Primitives: Tools, Resources, Prompts", "Executable functions (tools), readable schemas/data (resources), reusable prompt templates."),
         ("JSON-RPC 2.0 Transport Layer", "stdio pipes vs. Server-Sent Events (SSE) / Streamable HTTP."),
         ("MCP Security & Prompt Injections", "Tool permission models, argument validation, and preventing tool-based data exfiltration.")
     ],
     "Tab 4: Live MCP Tool & JSON-RPC Inspector — send live initialize, tools/list, and tools/call packets.",
     "Implement and test an enterprise MCP Server exposing custom calculation and database tools."),

    (14, "week-14-production-systems-and-mlops.md", "Week 14: Production Systems & MLOps", "ch11",
     "Redis Semantic Cache, FastAPI/vLLM, Docker Compose & Prometheus",
     "Production AI engineering: semantic caching, asynchronous queues with Celery, high-throughput model serving with vLLM, Docker Compose, and CI/CD.",
     [
         ("Production System Architecture", "Edge routing, API gateways, cache layers, worker pools, and persistent storage."),
         ("Semantic Caching with Redis", "Exact hash lookup (<1ms) + semantic cosine distance lookup (<15ms) to save 60% LLM cost."),
         ("Asynchronous Job Queues (Celery/Redis)", "Offloading long-running document ingestion and agent tasks from HTTP workers."),
         ("High-Throughput Model Serving", "Continuous batching and PagedAttention with vLLM and Ollama."),
         ("Docker Compose & CI/CD Pipelines", "Containerizing full-stack AI services and testing in GitHub Actions.")
     ],
     "Observe cache hit rates in /api/cache/stats and simulate concurrent load with k6/curl.",
     "Deploy the full multi-container docker-compose.yml stack and pass all automated health probes."),

    (15, "week-15-evals-safety-and-capstone-sprint.md", "Week 15: Evals, Safety & Capstone Sprint", "ch12",
     "DeepEval, OpenTelemetry Traces, PII Redaction & Architecture Review",
     "Evaluations and safety: OpenTelemetry distributed tracing, PII scrubbing, prompt guardrails, and final architecture review for the Capstone defense.",
     [
         ("Distributed Tracing with OpenTelemetry", "Tracing requests across client -> gateway -> cache -> vector DB -> LLM span."),
         ("Automated Evals with DeepEval", "Unit testing LLM outputs for hallucinations, toxicity, and compliance in CI/CD."),
         ("PII Redaction & Compliance", "Scrubbing credit card numbers, SSNs, and personal data before sending prompts to models."),
         ("Guardrails in Production", "Input guardrails (jailbreak prevention) and output guardrails (hallucination suppression)."),
         ("Capstone Architecture Review", "Pre-flight inspection against the 100-Point Capstone Grading Rubric.")
     ],
     "Inspect live OpenTelemetry trace waterfall showing latency breakdown across retrieval, cache, and LLM.",
     "Implement automated safety guardrails and run DeepEval test suite across 20 adversarial test cases."),

    (16, "week-16-capstone-demo-day.md", "Week 16: Capstone Demo Day & Graduation", "capstone",
     "100-Point Rubric Walkthrough, Live Defense Format & Alumni Next Steps",
     "Cohort graduation and Capstone Defense: presenting production AI systems evaluated against the 100-point rubric, live grading, and career transition.",
     [
         ("The 100-Point Capstone Rubric", "Detailed scoring across Architecture (20), MCP/Agents (20), RAG (20), Production (20), Safety (20)."),
         ("Live Defense Protocol", "10-minute system architecture demo + 5-minute live code walkthrough + 5-minute Q&A defense."),
         ("Common Defense Failure Points", "Missing fallbacks, brittle prompt engineering, untested edge cases, and lack of metrics."),
         ("From Student to AI Engineer", "Publishing open-source repositories, portfolio presentation, and navigating AI engineering interviews."),
         ("Alumni Community & Continuous Learning", "Staying current as foundation models and protocol standards evolve in 2026 and beyond.")
     ],
     "Walk through the live Rubric Explorer on /enroll and present a model Capstone defense project.",
     "Deliver live 15-minute Capstone defense, achieve 80+/100 score, and earn Cohort Certification.")
]

for w_num, filename, title, chapter, subtitle, overview, concepts, demo_cue, deliverable in REMAINING_WEEKS:
    slides = [
        (title, subtitle,
         f"**Part IV: Capstone & Production** • *{chapter.upper()} Companion*\n\n### Learning Objectives:\n" +
         "\n".join([f"{i+1}. {c[0]}: {c[1][:80]}..." for i, c in enumerate(concepts[:4])]) +
         f"\n\n> *\"{overview}\"*",
         f"Welcome cohort to {title}. Emphasize production rigor and end-to-end integration."),
        
        ("System Architecture & Mental Model", f"{title} Architectural Overview",
         "```\n+--------------------------------------------------------------+\n|                       Client Gateway                         |\n+------------------------------+-------------------------------+\n                               |\n+------------------------------v-------------------------------+\n|                   Core Orchestration Engine                  |\n|        (FastAPI / LangGraph / Model Context Protocol)        |\n+--------------+-------------------------------+---------------+\n               |                               |\n+--------------v---------------+ +-------------v---------------+\n|  Hybrid Storage & Search     | |  Inference & Safety Engine  |\n|  (pgvector / Redis / Qdrant) | |  (Ollama / Guardrails / OTel)|\n+------------------------------+ +-----------------------------+\n```\n- Decoupled, asynchronous, resilient system design.",
         "Walk through the core components and their data flows."),
    ]
    
    # Add deep-dive concept slides
    for c_title, c_desc in concepts:
        slides.append((
            f"Core Concept: {c_title}",
            subtitle,
            f"### Technical Breakdown:\n- {c_desc}\n\n### Architectural Implications:\n- Enables high reliability and deterministic execution.\n- Protects downstream systems from latency spikes and malformed outputs.\n- Standardizes interfaces across team boundaries.\n\n```python\n# Architectural invariant\nassert latency_ms < 50, 'Sub-50ms service requirement violated'\n```",
            f"Deep-dive into {c_title}. Highlight trade-offs between latency, cost, and accuracy."
        ))
        
    # Code slide
    slides.append((
        f"Annotated Code: {title}",
        "Production Implementation Pattern",
        "```python\nfrom typing import Dict, Any, List\nimport asyncio\n\nclass ProductionEngine:\n    def __init__(self, config: Dict[str, Any]):\n        self.config = config\n        self.is_ready = True\n        \n    async def execute_task(self, payload: Dict[str, Any]) -> Dict[str, Any]:\n        \"\"\"Executes production workflow with error handling and fallback.\"\"\"\n        try:\n            # High-reliability non-blocking execution\n            result = await self._run_core_logic(payload)\n            return {'status': 'success', 'data': result}\n        except Exception as e:\n            return {'status': 'fallback', 'error': str(e)}\n```",
        "Explain defensive error handling and why silent fallbacks are crucial in user-facing systems."
    ))
    
    # Demo cue slide
    slides.append((
        "Live Demo Cue: Studio Execution",
        "Instructor Step-by-Step Walkthrough",
        f"### Live Demonstration:\n1. Open `http://localhost:3000/studio`.\n2. Navigate to: {demo_cue}\n3. Run baseline scenario and observe real-time telemetry.\n4. Introduce deliberate edge-case error and demonstrate recovery mechanism.",
        f"Execute live demo: {demo_cue}"
    ))
    
    # Pitfalls slide
    slides.append((
        "Common Pitfalls & Production Failures",
        f"Failure Modes in {title}",
        "### Top 3 Production Failure Modes:\n1. **Unmonitored Latency Drift:** Long-tail queries degrading P99 latency without triggering alerts.\n2. **Missing Fallbacks:** Hard crashes when external dependencies experience momentary blips.\n3. **Evaluation Blind Spots:** Relying on human vibes instead of automated quantitative metrics.",
        "Highlight how easily untested assumptions turn into midnight production outages."
    ))
    
    # Deliverable slide
    slides.append((
        f"Weekly Deliverable: {title}",
        f"Milestone {w_num:02d} Specifications",
        f"### Deliverable Requirements:\n- {deliverable}\n- Unit tests passing cleanly in `pytest`.\n- Verified against zero Docker and zero paid API dependencies.\n- Push code to your branch `feat/w{w_num:02d}-deliverable`.",
        "Emphasize the definition of done and automated test verification."
    ))
    
    # Quiz slide
    slides.append((
        f"Week {w_num:02d} Check-Out Quiz",
        "Review & Consolidation",
        "### Knowledge Check:\n1. **What is the primary architectural invariant for this system?**\n   - *Answer:* Decoupled components with explicit contracts and resilient fallbacks.\n2. **How does this week's milestone feed into the final 100-point Capstone?**\n   - *Answer:* Directly satisfies one of the 5 core grading rubric dimensions.\n3. **Where can students access the runnable notebook and study guides?**\n   - *Answer:* In `book/chapters/` and `study-guides/` for Google NotebookLM.",
        "Wrap up the lecture and open the floor for student Q&A."
    ))
    
    DECKS_DATA.append({
        "filename": filename,
        "week": w_num,
        "title": title,
        "chapter": chapter,
        "slides": slides
    })

def generate_markdown_decks():
    print(f"Generating {len(DECKS_DATA)} weekly slide decks in slides/ ...")
    generated_files = []
    
    for deck in DECKS_DATA:
        file_path = SLIDES_DIR / deck["filename"]
        header_text = THEME_HEADER.format(header_title=deck["title"])
        
        slide_blocks = []
        for s_title, s_sub, s_content, s_notes in deck["slides"]:
            block = f"## {s_title}\n### {s_sub}\n\n{s_content.strip()}"
            if s_notes:
                block += f"\n\n<!-- Speaker Notes:\n{s_notes.strip()}\n-->"
            slide_blocks.append(block)
            
        full_content = header_text + "\n---\n\n".join(slide_blocks) + "\n"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_content)
            
        generated_files.append(str(file_path))
        print(f"  [+] Generated {deck['filename']} ({len(deck['slides'])} slides)")
        
    print(f"\nSuccessfully created all {len(generated_files)} slide decks!")
    return generated_files

if __name__ == "__main__":
    generate_markdown_decks()
