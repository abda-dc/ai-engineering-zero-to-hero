---
marp: true
theme: default
paginate: true
header: 'AI Engineering: Zero to Hero | Week 02: Math & High-Dimensional Geometry'
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
## Week 02: Math & High-Dimensional Geometry
### Vectors, Cosine Similarity, Gradients & Bayes Theorem

### Learning Objectives:
1. Geometric intuition of high-dimensional embedding spaces ($\mathbb{R}^d$).
2. Mathematical formulation: Dot Product vs. Cosine Similarity vs. L2 Distance.
3. The Curse of Dimensionality in vector search.
4. Gradient Descent optimization and Bayesian inference principles.

> *"If you don't understand high-dimensional geometry, vector databases will always feel like black magic."*

<!-- Speaker Notes:
Frame this week around intuition over dry derivations. Vector math is the physical law of modern AI.
-->
---

## Mental Model: High-Dimensional Embeddings
### Direction Encodes Semantic Meaning

```
              Dimension 2 (e.g. "Royalty")
              ^
              |         [King] *          * [Queen]
              |                   \        /
              |                    \      /
              |        [Man] *      \    /    * [Woman]
              +----------------------\--/------------> Dimension 1 (e.g. "Gender")
                                      \/
                   Vector offset: (King - Man + Woman ≈ Queen)
```
- Distance represents dissimilarity.
- Angle represents semantic orientation.

<!-- Speaker Notes:
Point out that semantic vector spaces possess arithmetic properties discovered by Mikolov in 2013.
-->
---

## Dot Product vs. Cosine Distance
### Formulas & Production Tradeoffs

### Dot Product:
$$\mathbf{u} \cdot \mathbf{v} = \sum_{i=1}^d u_i v_i = \|\mathbf{u}\| \|\mathbf{v}\| \cos \theta$$
- Measures both **alignment and magnitude** (longer text has larger magnitude).

### Cosine Similarity:
$$\text{Cosine}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|} = \cos \theta \in [-1, 1]$$
- Purely directional; invariant to document length.
- *Pro Tip:* If vectors are unit-normalized ($\left\|\mathbf{v}\right\| = 1$), dot product **equals** cosine similarity!

<!-- Speaker Notes:
Emphasize the performance win: pre-normalizing vectors turns cosine calculation into a pure dot product (saving square roots).
-->
---

## The Curse of Dimensionality
### Why High-D Spaces Defy Intuition

### Counter-Intuitive Properties of $\mathbb{R}^{1536}$:
1. **Distance Concentration:** As $d \to \infty$, the distance between the nearest and farthest vector converges to the average distance.
2. **Empty Volume:** 99.99% of the volume of a high-dimensional hypersphere resides in an infinitesimally thin outer shell.
3. **Brute-Force Search Collapses:** Scanning 10M vectors linearly ($O(N \cdot d)$) creates massive latency spikes.
- *Solution:* Approximate Nearest Neighbor (ANN) indexing (HNSW, IVF).

<!-- Speaker Notes:
Explain why vector databases exist: standard B-trees cannot index multi-dimensional vectors.
-->
---

## Gradients & Loss Optimization
### How Models Update Parameters

### The Optimization Equation:
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \eta \nabla L(\mathbf{w}_t)$$
- $\nabla L$: Gradient vector of partial derivatives pointing uphill.
- $\eta$: Learning rate scaling step size.
- *Intuition:* A ball rolling downhill along the surface of minimum error.

<!-- Speaker Notes:
Connect gradient descent to fine-tuning (LoRA in Week 5). You don't derive Jacobians by hand, but you monitor loss curves.
-->
---

## Bayes' Theorem in Search & Retrieval
### Updating Probabilities with New Evidence

$$P(Relevant \mid Query) = \frac{P(Query \mid Relevant) \cdot P(Relevant)}{P(Query)}$$

### Application in Hybrid RAG:
- **Prior $P(Relevant)$:** Base popularity or authority of a document.
- **Likelihood $P(Query \mid Relevant)$:** Match frequency of query keywords.
- **Posterior:** Final reranked confidence score.

<!-- Speaker Notes:
Show how Bayesian probability underpins BM25 and cross-encoder rerankers.
-->
---

## Annotated Code: Vector Math from Scratch
### Pure NumPy Implementation

```python
import numpy as np

def cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    """Numerically stable cosine similarity."""
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    if norm_u == 0.0 or norm_v == 0.0:
        return 0.0
    return float(np.dot(u, v) / (norm_u * norm_v))

def unit_normalize_rows(matrix: np.ndarray) -> np.ndarray:
    """Normalize embedding matrix for rapid dot-product search."""
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0.0] = 1.0
    return matrix / norms
```

<!-- Speaker Notes:
Walk through zero-norm handling. Show how keepdims=True enables vectorized matrix operations.
-->
---

## Live Demo Cue: Vector Projection Studio
### Hands-on Studio Walkthrough

### Instructor Demo Steps:
1. Open `http://localhost:3000/studio` -> **Tab 1: Tokenizer & Embedding Explorer**.
2. Enter pairs of synonymous vs. antonymous sentences.
3. Inspect the 2D projection scatter plot.
4. Demonstrate how changing a single keyword rotates the embedding vector in geometric space.

<!-- Speaker Notes:
Demonstrate live in browser. Show the cosine matrix heatmap updating in real time.
-->
---

## Common Pitfalls & Numerical Bugs
### Production Bugs in Vector Math

1. **NaN Infiltration:** Un-clamped division by zero spreads `NaN` across entire index batches.
2. **Mixing Normalized and Un-Normalized Vectors:** Yields distorted search rankings.
3. **Mismatched Dimensionality:** Querying a 768-dim index with a 1536-dim embedding model causes runtime dimensional mismatch crashes.

<!-- Speaker Notes:
Stress that embedding models cannot be swapped without rebuilding the entire vector index.
-->
---

## Weekly Deliverable: Math & Vectors
### Capstone Milestone 02

### Deliverable Requirements:
- Complete `book/chapters/part1-foundations/ch01-math-and-stats-intuition.ipynb`.
- Implement:
  1. Vector distance metrics (Cosine, Euclidean, Manhattan).
  2. Pairwise similarity matrix generator.
  3. Simple 1D gradient descent simulator.
- Verify with `python scripts/verify_notebooks.py`.

<!-- Speaker Notes:
Check that students verify both unit tests and notebook cells.
-->
---

## Week 02 Check-Out Quiz
### Review & Consolidation

1. **What is the cosine similarity of orthogonal vectors?**
   - *Answer:* `0.0` (90-degree angle).
2. **Why does unit-normalizing vectors speed up search?**
   - *Answer:* Eliminates runtime norm calculations; similarity equals a simple dot product.
3. **What is the range of cosine distance ($1 - \text{similarity}$)?**
   - *Answer:* $[0.0, 2.0]$.

<!-- Speaker Notes:
Recap key takeaways and set expectations for Week 3.
-->
