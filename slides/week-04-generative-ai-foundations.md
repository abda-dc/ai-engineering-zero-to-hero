---
marp: true
theme: default
paginate: true
header: 'AI Engineering: Zero to Hero | Week 04: Generative AI Foundations'
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
## Week 04: Generative AI Foundations
### GenAI vs. Discriminative, Self-Attention & RLHF

### Learning Objectives:
1. Contrast Generative ($P(X, Y)$) vs. Discriminative ($P(Y \mid X)$) models.
2. Deconstruct the **Transformer Architecture** and the **Self-Attention Mechanism**.
3. Understand Pre-training vs. Supervised Fine-Tuning (SFT) vs. RLHF.
4. Explore Multimodal foundation models and AI safety alignment.

> *"Attention is not just an algorithm; it is dynamic content-based routing across a vector space."*

<!-- Speaker Notes:
Welcome students to Part II. Today we dive into the core engine of modern LLMs.
-->
---

## Mental Model: The Self-Attention Mechanism
### Queries, Keys, and Values

```
Query (What I'm looking for)  Key (What I contain)  Value (What I communicate)
         Q                          K                          V
         |                          |                          |
         +------------x-------------+                          |
                      | (Dot Product)                          |
                      v                                        |
               Raw Attention Scores                            |
                      | (Scale by sqrt(d_k) & Softmax)         |
                      v                                        |
               Attention Weights [0, 1]                        |
                      |                                        |
                      +-------------------x--------------------+
                                          |
                                          v
                                Contextual Output Vector
```

<!-- Speaker Notes:
Walk through the filing cabinet analogy: Query is your search term, Key is the folder label, Value is the folder content.
-->
---

## The Mathematical Equation of Attention
### Scaled Dot-Product Attention

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$

### Why the $\sqrt{d_k}$ Scaling Factor?
- When dimensionality $d_k$ is large, dot products grow large in magnitude.
- Large values push the softmax function into regions with near-zero gradients (saturation).
- Dividing by $\sqrt{d_k}$ stabilizes numerical gradients during backpropagation.

<!-- Speaker Notes:
Ask students what happens when softmax saturates: gradients vanish and learning halts.
-->
---

## Multi-Head Attention (MHA)
### Attending to Multiple Subspaces in Parallel

### Why Multiple Heads?
- A single attention head only tracks one type of relationship (e.g. subject-verb agreement).
- **Multi-Head Attention** projects Q, K, V into $h$ distinct representation subspaces:
$$\text{MHA}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) W^O$$
- Head 1 might track syntax, Head 2 tracks coreference ('it' $\to$ 'robot'), Head 3 tracks semantics.

<!-- Speaker Notes:
Show how parallel heads give the network rich expressive capacity across different linguistic dimensions.
-->
---

## The LLM Training Lifecycle
### From Raw Text to Helpful Assistant

```
1. Pre-training (99% of compute)
   Raw Internet Text -> Base Model (Next-token prediction: "The capital is...")

2. Supervised Fine-Tuning / SFT (1% of compute)
   Curated QA Dialogues -> Instruction Model ("User: Summarize this...")

3. Preference Alignment (RLHF / DPO)
   Human / AI Feedback -> Aligned Assistant (Helpful, Honest, Harmless)
```

<!-- Speaker Notes:
Clarify the difference between a raw Base model (which continues text) and an Instruct model (which answers questions).
-->
---

## Multimodal Foundations & AI Safety
### Vision, Audio & Alignment Boundaries

### Multimodality:
- Project image patch tokens (Vision Transformers / ViT) into the same embedding space as text tokens.
- Allows joint cross-attention across images and text.

### Safety Guardrails:
- Red-teaming against prompt injections and jailbreaks.
- Toxicity classifiers and output filtering.

<!-- Speaker Notes:
Preview Chapter 05 red-teaming and Chapter 12 safety audits.
-->
---

## Annotated Code: Scaled Dot-Product Attention
### Pure PyTorch Implementation

```python
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(Q, K, V, mask=None):
    """Compute scaled dot-product attention weights and output."""
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k ** 0.5)
    
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
        
    weights = F.softmax(scores, dim=-1)
    output = torch.matmul(weights, V)
    return output, weights
```

<!-- Speaker Notes:
Point out the causal mask logic: -1e9 becomes exact zero after softmax, preventing models from looking ahead.
-->
---

## Live Demo Cue: Studio Attention Explorer
### Visualizing Token Interaction

### Instructor Live Demo Steps:
1. Open `http://localhost:3000/studio` -> **Tab 1: Tokenizer & Embedding Explorer**.
2. Input sentence: *'The animal didn't cross the street because it was too tired.'*
3. Inspect token split and show how *'it'* attends heavily to *'animal'*.
4. Change to *'it was too wide'* and show how *'it'* shifts attention to *'street'*.

<!-- Speaker Notes:
This Winograd schema demonstration visually proves how attention resolves pronouns contextually.
-->
---

## Common Pitfalls in Generative AI
### Production Realities

1. **Treating LLM Output as Fact:** Hallucinations occur because models optimize next-token likelihood, not truth.
2. **Confusing Base and Instruct Models:** Deploying a base model leads to repetitive completion loops.
3. **Quadratic Sequence Memory:** Attention memory scales as $O(N^2)$ with sequence length $N$.

<!-- Speaker Notes:
Warn students about memory explosion when scaling context length.
-->
---

## Weekly Deliverable: Generative Foundations
### Capstone Milestone 04

### Deliverable Requirements:
- Complete `book/chapters/part2-core-genai/ch03-generative-ai-foundations.ipynb`.
- Implement:
  1. Multi-head self-attention module in PyTorch.
  2. Causal masking for autoregressive decoders.
  3. Softmax temperature experiment.
- Push code to `feat/w04-genai-foundations`.

<!-- Speaker Notes:
Encourage students to inspect intermediate attention matrices.
-->
---

## Week 04 Check-Out Quiz
### Review & Consolidation

1. **Why is the dot product divided by $\sqrt{d_k}$ in self-attention?**
   - *Answer:* Prevents large dot products from saturating softmax gradients.
2. **What is the difference between SFT and RLHF?**
   - *Answer:* SFT teaches task format via demonstration; RLHF steers outputs toward human preference.
3. **Why does causal masking use $-10^9$ before softmax?**
   - *Answer:* $e^{-10^9} \approx 0$, ensuring future tokens have zero attention weight.

<!-- Speaker Notes:
Conclude Week 4. Next week: deep dive inside the Transformer decoder and KV cache.
-->
