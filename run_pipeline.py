"""
run_pipeline.py
One-click runner: generates data → cleans it → builds the Excel report.
Usage:  python run_pipeline.py
"""

import subprocess, sys, time

STEPS = [
    ("Generating raw messy data …",     ["python", "generate_data.py"]),
    ("Cleaning data …",                  ["python", "clean_data.py"]),
    ("Building Excel report & charts …", ["python", "generate_report.py"]),
]

def run(label, cmd):
    print(f"\n{'='*60}")
    print(f"  STEP: {label}")
    print(f"{'='*60}")
    t0 = time.time()
    result = subprocess.run(cmd, capture_output=False, text=True)
    elapsed = time.time() - t0
    if result.returncode != 0:
        print(f"\n❌  Step failed (exit {result.returncode})")
        sys.exit(result.returncode)
    print(f"\n  ✓  Done in {elapsed:.1f}s")

for label, cmd in STEPS:
    run(label, cmd)

print(f"\n{'='*60}")
print("  ✅  PIPELINE COMPLETE")
print("  Output files:")
print("    raw_sales_data.csv")
print("    cleaned_sales_data.csv")
print("    cleaning_log.txt")
print("    sales_report.xlsx")
print("    charts/  (PNG charts)")
print(f"{'='*60}\n")
