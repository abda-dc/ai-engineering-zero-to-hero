---
marp: true
theme: default
paginate: true
header: 'AI Engineering: Zero to Hero | Week 03: The Classical Machine Learning Bridge'
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
## Week 03: The Classical Machine Learning Bridge
### Loss Curves, Overfitting, Regularization & Cross-Validation

### Learning Objectives:
1. Understand Supervised vs. Unsupervised paradigms in the age of LLMs.
2. Diagnose model health via **Loss Curves** (Underfitting vs. Overfitting).
3. Apply **L1 (Lasso)** and **L2 (Ridge)** regularization principles.
4. Establish rigorous **k-Fold Cross-Validation** to prevent data leakage.

> *"Before generating tokens, an AI engineer must know whether a simple logistic regression or decision tree solves the business problem with 100x lower latency."*

<!-- Speaker Notes:
Position classical ML as a vital baseline. Not every problem needs an LLM.
-->
---

## Mental Model: The Bias-Variance Tradeoff
### Generalization vs. Memorization

```
High Loss ^
          |      \  Validation Loss (High Variance / Overfitting)
          |       \       /
          |        \_____/
          |         \   /
          |          \ /  Training Loss (Memorization)
          |           v__________________
          +-----------------------------------> Model Complexity / Epochs
              Underfitting         Sweet Spot          Overfitting
```
- **Underfitting (High Bias):** Model too simple to capture patterns.
- **Overfitting (High Variance):** Model memorizes training noise.

<!-- Speaker Notes:
Explain how this curve applies to LLM fine-tuning and classical ML alike.
-->
---

## Loss Curves Diagnostics
### Reading Training Dynamics Like an EKG

### Common Scenarios:
- **Scenario A:** Both train and val loss stay high $\to$ Learning rate too low or model capacity insufficient.
- **Scenario B:** Train loss drops to 0, val loss explodes $\to$ Severe overfitting. Add dropout / weight decay.
- **Scenario C:** Loss oscillates erratically $\to$ Learning rate too high (stepping over minima).
- **Scenario D:** Train and val decrease together $\to$ Healthy convergence.

<!-- Speaker Notes:
Train students to diagnose training runs before spending hours on compute.
-->
---

## Regularization: Taming Complexity
### L1 (Lasso) vs. L2 (Ridge) vs. Dropout

### Formulations:
- **L1 Regularization (Lasso):**
  $$L_{reg} = L_0 + \lambda \sum |w_i|$$
  *Property:* Drives uninformative weights to **exact zero** (feature selection).
- **L2 Regularization (Ridge / Weight Decay):**
  $$L_{reg} = L_0 + \lambda \sum w_i^2$$
  *Property:* Shrinks weights smoothly; prevents single dominant features.
- **Dropout:** Randomly deactivates neurons during forward pass to force redundant representations.

<!-- Speaker Notes:
Connect L2 regularization to weight decay in AdamW (the default optimizer for Transformers).
-->
---

## Cross-Validation & Data Leakage
### Preventing Metric Hallucinations

```
Dataset [====================================================]

Fold 1:  [ Val  ] [ Train ] [ Train ] [ Train ] [ Train ]
Fold 2:  [ Train ] [ Val  ] [ Train ] [ Train ] [ Train ]
Fold 3:  [ Train ] [ Train ] [ Val  ] [ Train ] [ Train ]
Fold 4:  [ Train ] [ Train ] [ Train ] [ Val  ] [ Train ]
Fold 5:  [ Train ] [ Train ] [ Train ] [ Train ] [ Val  ]
```
### The Cardinal Sin: Data Leakage
- Normalizing or imputing data **before** splitting folds leaks test distributions into training.

<!-- Speaker Notes:
Stress that evaluating on leaked test data gives false confidence before production deployment.
-->
---

## Classical Baselines for AI Systems
### When NOT to Use an LLM

| Feature | Classical ML (scikit-learn) | Large Language Model |
| :--- | :--- | :--- |
| **Latency** | 1 - 5 ms | 500 - 3000 ms |
| **Cost per 1M calls**| \$0.01 (CPU server) | \$5.00 - \$30.00 |
| **Determinism** | 100% deterministic | Probabilistic |
| **Training Data** | Requires labeled tables | Zero/Few-shot |
| **Use Cases** | Fraud score, churn, intent routing | Summaries, code, reasoning |

<!-- Speaker Notes:
Teach students to use cheap classifiers as first-stage routers in AI pipelines.
-->
---

## Annotated Code: scikit-learn Pipeline
### Robust Leak-Free Modeling

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

# Construct pipeline ensuring transformation occurs inside cross-validation
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression(C=1.0, penalty='l2'))
])

scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='f1_macro')
print(f'Mean CV F1 Score: {scores.mean():.4f} (+/- {scores.std():.4f})')
```

<!-- Speaker Notes:
Explain why Pipeline prevents leakage: scaling parameters fit ONLY on training folds.
-->
---

## Live Demo Cue: Overfitting in Action
### Interactive Colab Walkthrough

### Instructor Live Demo Steps:
1. Open `book/chapters/part1-foundations/ch02-classical-ml-bridge.ipynb`.
2. Fit a high-degree polynomial regressor ($degree = 15$) on 20 noisy data points.
3. Show the wild oscillation between data points (overfitting).
4. Apply L2 Ridge penalty and show the curve smoothly regularizing.

<!-- Speaker Notes:
Demonstrate how easy it is to overfit small datasets.
-->
---

## Common Pitfalls & Production Bugs
### Classical ML Traps

1. **Evaluating on Training Data:** Reporting 99.8% training accuracy to stakeholders.
2. **Ignoring Class Imbalance:** Accuracy is misleading when 99% of samples belong to the majority class.
3. **Feature Store Drift:** Training features computed differently from real-time production features.

<!-- Speaker Notes:
Remind students: accuracy on unbalanced fraud data is a dangerous vanity metric.
-->
---

## Weekly Deliverable: Classical ML Bridge
### Capstone Milestone 03

### Deliverable Requirements:
- Complete `ch02-classical-ml-bridge.ipynb`.
- Implement:
  1. Train/Val/Test split with stratification.
  2. Cross-validated baseline classifier.
  3. Loss curve plotting function comparing unregularized vs. regularized models.
- Push verified code to your branch `feat/w03-classical-ml`.

<!-- Speaker Notes:
Encourage students to inspect feature importances.
-->
---

## Week 03 Check-Out Quiz
### Review & Consolidation

1. **What does a diverging validation loss indicate while training loss decreases?**
   - *Answer:* Overfitting.
2. **Why does L1 regularization create sparse weights?**
   - *Answer:* The diamond constraint surface touches loss contours at axes where weights are zero.
3. **Why should data scaling occur inside the cross-validation loop?**
   - *Answer:* To prevent test set distribution metrics from leaking into the training step.

<!-- Speaker Notes:
Conclude Part I: Foundations. Preview Part II: Core Generative AI.
-->
