#!/usr/bin/env python3
"""
scripts/export_notebooklm_guides.py
Exports high-yield, structured Markdown study guides for each chapter,
optimized for ingestion into Google NotebookLM to generate audio overviews,
podcasts, Socratic study sessions, and flashcard decks.
"""

import json
from pathlib import Path

CURRICULUM_PATH = Path("app/frontend/src/data/curriculum.json")
OUTPUT_DIR = Path("study-guides")

def generate_study_guide(chapter: dict) -> str:
    concepts_list = "\n".join([f"- **{c}**" for c in chapter["concepts"]])
    
    sections_text = ""
    for sec in chapter["sections"]:
        sections_text += f"\n### {sec['title']}\n\n{sec['content']}\n"
        if sec.get("mermaid"):
            sections_text += f"\n*Architecture Concept Diagram:*\n```mermaid\n{sec['mermaid']}\n```\n"

    quiz_flashcards = ""
    for idx, q in enumerate(chapter["quiz"], 1):
        correct_letter = chr(65 + q["answer"])
        correct_text = q["options"][q["answer"]]
        quiz_flashcards += f"""
#### Flashcard {idx}: {q['question']}
- **Answer:** {correct_letter}) {correct_text}
- **Explanation:** {q['explanation']}
"""

    return f"""# NotebookLM Study Guide: {chapter['title']}

**Chapter ID:** `{chapter['id']}`  
**Part:** {chapter.get('part_title', 'Core Curriculum')}  
**Target Ingestion:** Google NotebookLM Source (Audio Podcast, Socratic Tutor & Flashcards)

---

## 🎯 Executive Summary & Core Pillars
This chapter covers foundational and production-grade knowledge in modern AI engineering.

### Core Concepts Covered:
{concepts_list}

---

## 📖 In-Depth Concept Breakdown
{sections_text}

---

## 🛠 Hands-On Capstone Lab Blueprint
- **Title:** {chapter['capstone']['title']}
- **Objective:** {chapter['capstone']['objective']}
- **Implementation Strategy:**
{chapter['capstone']['instructions']}

---

## 🎙 Socratic Discussion Questions for NotebookLM Audio Overviews
1. **Trade-off Analysis:** What are the operational latency, memory, and cost implications of the techniques introduced in this chapter?
2. **Production Pitfalls:** Under what conditions do these methods fail (e.g. out-of-memory, prompt injections, catastrophic forgetting, low recall)?
3. **Engineering Synthesis:** How does this chapter connect to downstream systems such as RAG retrieval, agent orchestration, or MCP tooling?

---

## 🗂 Flashcard & Self-Check Review Deck
{quiz_flashcards}
"""

def main():
    with open(CURRICULUM_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    count = 0

    # Index Guide
    index_md = f"""# AI Engineering: Zero to Hero — Master Study Guides Collection

This directory contains standalone, highly structured Markdown study guides for all 13 chapters, specifically formatted for one-click ingestion into **Google NotebookLM** to generate:
- Chapter-by-chapter Audio Overviews & Deep-Dive Podcasts
- Socratic Study Guides & Adaptive Tutoring
- Flashcard Decks & Concept Summaries

## Chapters Index:
"""

    for part in data["parts"]:
        index_md += f"\n### {part['title']}\n"
        for ch in part["chapters"]:
            filename = f"{ch['id']}-study-guide.md"
            filepath = OUTPUT_DIR / filename
            guide_content = generate_study_guide(ch)
            with open(filepath, "w", encoding="utf-8") as gf:
                gf.write(guide_content)
            index_md += f"- [{ch['title']}](./{filename}) ({len(ch['concepts'])} concepts)\n"
            count += 1
            print(f"  [EXPORTED] {filepath}")

    with open(OUTPUT_DIR / "README.md", "w", encoding="utf-8") as rf:
        rf.write(index_md)

    print(f"\nSuccessfully generated {count} NotebookLM study guides + README in '{OUTPUT_DIR}'!")

if __name__ == "__main__":
    main()
