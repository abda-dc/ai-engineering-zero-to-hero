#!/usr/bin/env python3
"""
Slide Compiler for AI Engineering: Zero to Hero.
1. Compiles all 16 Marp slide decks in slides/ to standalone HTML via @marp-team/marp-cli
2. Copies standalone HTML to app/frontend/public/slides-html/ for zero-latency browser rendering
3. Parses slide markdown, speaker notes, and metadata into app/frontend/src/data/slides.json
"""

import os
import re
import json
import shutil
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SLIDES_DIR = WORKSPACE_ROOT / "slides"
DIST_HTML_DIR = SLIDES_DIR / "dist" / "html"
FRONTEND_PUBLIC_SLIDES = WORKSPACE_ROOT / "app" / "frontend" / "public" / "slides-html"
MANIFEST_PATH = WORKSPACE_ROOT / "app" / "frontend" / "src" / "data" / "slides.json"

DIST_HTML_DIR.mkdir(parents=True, exist_ok=True)
FRONTEND_PUBLIC_SLIDES.mkdir(parents=True, exist_ok=True)
MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

NOTE_REGEX = re.compile(r"<!--\s*Speaker Notes:\s*(.*?)\s*-->", re.DOTALL | re.IGNORECASE)

def extract_slides_from_markdown(content: str):
    """Parses Marp markdown into individual slide objects with speaker notes."""
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            body = parts[2]
            
    raw_slides = [s.strip() for s in body.split("\n---") if s.strip()]
    parsed_slides = []
    
    for i, raw in enumerate(raw_slides, 1):
        notes = ""
        clean_text = raw
        
        # Extract speaker notes
        note_match = NOTE_REGEX.search(raw)
        if note_match:
            notes = note_match.group(1).strip()
            clean_text = NOTE_REGEX.sub("", raw).strip()
            
        # Extract title (first # or ## line)
        title = f"Slide {i}"
        for line in clean_text.splitlines():
            line_str = line.strip()
            if line_str.startswith("#"):
                title = line_str.lstrip("#").strip()
                break
                
        parsed_slides.append({
            "slide_number": i,
            "title": title,
            "markdown": clean_text,
            "notes": notes,
            "has_code": "```" in clean_text,
            "has_demo": "Live Demo" in clean_text or "Studio" in clean_text or "Colab" in clean_text
        })
        
    return parsed_slides

def compile_all_decks():
    md_files = sorted(list(SLIDES_DIR.glob("week-*.md")))
    if not md_files:
        print("No slide markdown files found in slides/! Running generator first...")
        from generate_all_slides import generate_markdown_decks
        generate_markdown_decks()
        md_files = sorted(list(SLIDES_DIR.glob("week-*.md")))

    print(f"Compiling {len(md_files)} Marp slide decks into HTML via marp-cli...")
    
    # Run batch conversion with Marp CLI
    cmd = [
        "npx", "--yes", "@marp-team/marp-cli",
        "--no-stdin",
        "-I", str(SLIDES_DIR),
        "--html",
        "-o", str(DIST_HTML_DIR)
    ]
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Warning: Marp batch compilation returned exit code {res.returncode}:\n{res.stderr}")
    else:
        print("Marp batch HTML compilation succeeded!")
        
    # Copy all generated HTMLs to frontend public folder
    for html_file in DIST_HTML_DIR.glob("*.html"):
        dest = FRONTEND_PUBLIC_SLIDES / html_file.name
        shutil.copy2(str(html_file), str(dest))
    print(f"Copied {len(list(DIST_HTML_DIR.glob('*.html')))} HTML slide decks to frontend public directory.")

    # Build slides.json manifest for Next.js presenter
    manifest = {
        "course_title": "AI Engineering: Zero to Hero — 16-Week Slide Decks",
        "total_weeks": len(md_files),
        "decks": []
    }
    
    for md_file in md_files:
        stem = md_file.stem
        week_match = re.search(r"week-(\d+)", stem)
        week_num = int(week_match.group(1)) if week_match else 1
        
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        slides = extract_slides_from_markdown(content)
        deck_title = slides[0]["title"] if slides else f"Week {week_num:02d}"
        
        manifest["decks"].append({
            "id": f"week-{week_num:02d}",
            "week_number": week_num,
            "title": deck_title,
            "filename": md_file.name,
            "html_path": f"/slides-html/{stem}.html",
            "slide_count": len(slides),
            "slides": slides
        })

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"Successfully compiled all {len(manifest['decks'])} decks!")
    print(f"Manifest written to: {MANIFEST_PATH} ({os.path.getsize(MANIFEST_PATH)} bytes)")

if __name__ == "__main__":
    compile_all_decks()
