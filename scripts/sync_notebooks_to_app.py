#!/usr/bin/env python3
"""
scripts/sync_notebooks_to_app.py
Reads book/myst.yml and all 13 .ipynb notebooks and compiles them into
app/frontend/src/data/curriculum.json.
"""

import json
import re
from pathlib import Path
import yaml

BOOK_DIR = Path("book")
MYST_CONFIG = BOOK_DIR / "myst.yml"
OUTPUT_PATH = Path("app/frontend/src/data/curriculum.json")

def parse_quiz_text(text: str) -> list:
    questions = []
    current_q = None
    in_explanation = False

    for line in text.splitlines():
        line_s = line.strip()
        if line_s.startswith("### Question "):
            if current_q:
                questions.append(current_q)
            q_text = line_s.split(":", 1)[1].strip() if ":" in line_s else line_s
            current_q = {
                "id": f"q_{len(questions)+1}",
                "question": q_text,
                "options": [],
                "answer": 0,
                "explanation": ""
            }
            in_explanation = False
        elif current_q:
            if line_s.startswith("- **") and ")**" in line_s:
                # Option line: - **A)** Option text
                opt_text = line_s.split(")**", 1)[1].strip()
                current_q["options"].append(opt_text)
            elif "<b>Correct Answer:</b>" in line_s:
                # <b>Correct Answer:</b> A) Option text
                m = re.search(r"<b>Correct Answer:</b>\s*([A-D])\)", line_s)
                if m:
                    current_q["answer"] = ord(m.group(1).upper()) - ord('A')
            elif line_s.startswith("**Explanation:**"):
                current_q["explanation"] = line_s.replace("**Explanation:**", "").strip()
                in_explanation = True
            elif in_explanation and line_s.startswith("</details>"):
                in_explanation = False
            elif in_explanation and line_s:
                current_q["explanation"] += " " + line_s

    if current_q:
        questions.append(current_q)

    return questions

def parse_notebook(notebook_path: Path) -> dict:
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    meta = nb.get("metadata", {})
    chapter_id = meta.get("chapter_id", notebook_path.stem.split("-")[0])
    title = meta.get("title", notebook_path.stem.replace("-", " ").title())
    part_title = meta.get("part_title", "")
    concepts = meta.get("concepts", [])

    sections = []
    capstone = None
    quiz = []

    current_section = None

    for cell in nb.get("cells", []):
        cell_type = cell.get("cell_type")
        source = "".join(cell.get("source", []))

        if cell_type == "markdown":
            if "## Hands-On Capstone Lab:" in source:
                if current_section:
                    sections.append(current_section)
                    current_section = None

                title_match = re.search(r"## Hands-On Capstone Lab:\s*(.+)", source)
                cap_title = title_match.group(1).strip() if title_match else "Capstone Lab"
                
                obj_match = re.search(r"### Objective:\s*\n(.*?)(?=\n###|\Z)", source, re.DOTALL)
                cap_obj = obj_match.group(1).strip() if obj_match else ""
                
                inst_match = re.search(r"### Instructions:\s*\n(.*?)(?=\n##|\Z)", source, re.DOTALL)
                cap_inst = inst_match.group(1).strip() if inst_match else ""

                capstone = {
                    "title": cap_title,
                    "objective": cap_obj,
                    "instructions": cap_inst,
                    "code": ""
                }
                continue

            if "## Chapter Mastery Self-Check Quiz" in source:
                if current_section:
                    sections.append(current_section)
                    current_section = None

                quiz = parse_quiz_text(source)
                continue

            sec_header_match = re.match(r"^##\s+([^#\n]+)", source)
            if sec_header_match and not source.startswith("## Core Concepts Covered"):
                if current_section:
                    sections.append(current_section)

                sec_title = sec_header_match.group(1).strip()
                mermaid_match = re.search(r"```mermaid\n(.*?)\n```", source, re.DOTALL)
                mermaid_code = mermaid_match.group(1).strip() if mermaid_match else None

                content = re.sub(r"^##\s+[^\n]+\n*", "", source)
                if mermaid_code:
                    content = re.sub(r"```mermaid\n.*?\n```", "", content, flags=re.DOTALL).strip()

                current_section = {
                    "id": f"sec_{len(sections)+1}",
                    "title": sec_title,
                    "content": content.strip(),
                    "mermaid": mermaid_code,
                    "code": []
                }
            elif current_section:
                current_section["content"] += f"\n\n{source.strip()}"

        elif cell_type == "code":
            if capstone and not capstone["code"]:
                capstone["code"] = source.strip()
            elif current_section:
                current_section["code"].append(source.strip())

    if current_section:
        sections.append(current_section)

    return {
        "id": chapter_id,
        "title": title,
        "part_title": part_title,
        "relative_path": str(notebook_path.relative_to(BOOK_DIR)).replace("\\", "/"),
        "concepts": concepts,
        "sections": sections,
        "capstone": capstone or {"title": "Hands-on Lab", "objective": "", "instructions": "", "code": ""},
        "quiz": quiz
    }

def main():
    print(f"Reading configuration from {MYST_CONFIG}...")
    with open(MYST_CONFIG, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    project_meta = config.get("project", {})
    toc = project_meta.get("toc", [])

    curriculum = {
        "title": project_meta.get("title", "AI Engineering: Zero to Hero"),
        "description": project_meta.get("description", ""),
        "github": project_meta.get("github", ""),
        "total_chapters": 0,
        "total_concepts": 0,
        "all_concepts": [],
        "parts": []
    }

    all_concepts_set = set()

    for item in toc:
        if "title" in item and "children" in item:
            part_title = item["title"]
            part_id = f"part-{len(curriculum['parts'])+1}"
            part_obj = {
                "id": part_id,
                "title": part_title,
                "chapters": []
            }

            for child in item["children"]:
                file_rel = child.get("file")
                if not file_rel:
                    continue
                file_path = BOOK_DIR / file_rel
                if file_path.suffix == ".ipynb" and file_path.exists():
                    ch_data = parse_notebook(file_path)
                    part_obj["chapters"].append(ch_data)
                    curriculum["total_chapters"] += 1
                    for c in ch_data["concepts"]:
                        all_concepts_set.add(c)

            curriculum["parts"].append(part_obj)

    curriculum["all_concepts"] = sorted(list(all_concepts_set))
    curriculum["total_concepts"] = len(curriculum["all_concepts"])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(curriculum, f, indent=2)

    print(f"\nCurriculum synced successfully to {OUTPUT_PATH}!")
    print(f"  Total Parts: {len(curriculum['parts'])}")
    print(f"  Total Chapters: {curriculum['total_chapters']}")
    print(f"  Total Distinct Concepts: {curriculum['total_concepts']}")

if __name__ == "__main__":
    main()
