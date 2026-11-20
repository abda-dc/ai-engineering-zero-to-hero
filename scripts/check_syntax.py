import importlib.util

spec = importlib.util.spec_from_file_location("build_notebooks", "scripts/build_notebooks.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for ch in mod.CHAPTERS_DATA:
    for idx, s in enumerate(ch['sections']):
        if s.get('code'):
            try:
                compile(s['code'], f"{ch['chapter_id']}_sec{idx}", 'exec')
            except SyntaxError as e:
                print(f"SyntaxError in {ch['chapter_id']} section {idx} ({s['title']}): {e}")
    if ch['capstone'].get('code'):
        try:
            compile(ch['capstone']['code'], f"{ch['chapter_id']}_capstone", 'exec')
        except SyntaxError as e:
            print(f"SyntaxError in {ch['chapter_id']} capstone ({ch['capstone']['title']}): {e}")

print("Syntax check finished.")
