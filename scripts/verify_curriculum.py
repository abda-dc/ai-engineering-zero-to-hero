import json
from pathlib import Path

path = Path("app/frontend/src/data/curriculum.json")
assert path.exists(), "curriculum.json does not exist"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Title: {data['title']}")
print(f"Parts count: {len(data['parts'])}")
print(f"Total Chapters: {data['total_chapters']}")
print(f"Total Concepts: {data['total_concepts']}")

for part in data["parts"]:
    print(f"\n[{part['id'].upper()}] {part['title']}")
    for ch in part["chapters"]:
        print(f"  - {ch['id']}: {ch['title']}")
        print(f"      Concepts: {len(ch['concepts'])} | Sections: {len(ch['sections'])} | Quiz: {len(ch['quiz'])} questions")
        assert len(ch['concepts']) > 0, f"No concepts in {ch['id']}"
        assert len(ch['sections']) > 0, f"No sections in {ch['id']}"
        assert len(ch['quiz']) >= 4, f"Expected at least 4 quiz questions in {ch['id']}"

print("\nCurriculum validation passed with flying colors!")
