import json
import glob
import sys

def verify_all():
    files = glob.glob('book/chapters/**/*.ipynb', recursive=True)
    assert len(files) == 13, f"Expected 13 notebooks, found {len(files)}"
    for path in sorted(files):
        with open(path, encoding='utf-8') as f:
            nb = json.load(f)
        print(f"Testing {path}: {len(nb['cells'])} cells...")
        env = {"__name__": "__main__"}
        for idx, c in enumerate(nb['cells']):
            if c['cell_type'] == 'code':
                code = "".join(c['source'])
                try:
                    exec(code, env)
                except Exception as e:
                    print(f"FAILED in {path} cell {idx}: {e}")
                    sys.exit(1)
    print("\nSUCCESS: All 13 notebooks and their code cells execute cleanly with zero errors!")

if __name__ == "__main__":
    verify_all()
