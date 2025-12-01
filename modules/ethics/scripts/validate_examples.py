import json, sys, pathlib, math
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
ok = True

def fail(msg):
    global ok
    ok = False
    print(f"::error::{msg}")

# POAV
poav_p = ROOT / "EXAMPLES/poav_report.sample.json"
if poav_p.exists():
    data = json.loads(poav_p.read_text())
    score = float(data.get("score", -1))
    th = float(data.get("threshold", 0.90))
    if not (score >= th - 0.02):  # 0.90 ± 0.02
        fail(f"POAV score {score} below threshold {th}±0.02")
else:
    fail(f"Missing {poav_p}")

# Drift Score
ds_p = ROOT / "EXAMPLES/drift_score.sample.json"
if ds_p.exists():
    data = json.loads(ds_p.read_text())
    ds = float(data.get("DS", -1))
    warn = float(data.get("gate", {}).get("warn", 0.85))
    if ds < warn:
        fail(f"Drift Score {ds} below warn gate {warn}")
else:
    fail(f"Missing {ds_p}")

# StepLedger YAML sanity
sl_p = ROOT / "EXAMPLES/step_ledger.sample.yaml"
if sl_p.exists():
    data = yaml.safe_load(sl_p.read_text())
    asserts = sum(len(x.get("asserts", [])) for x in data.get("steps", []))
    if asserts == 0:
        fail("StepLedger has no asserts")
else:
    fail(f"Missing {sl_p}")

# Time-Island YAML sanity
ti_p = ROOT / "EXAMPLES/time_island.sample.yaml"
if ti_p.exists():
    data = yaml.safe_load(ti_p.read_text())
    for k in ["chronos", "kairos", "trace"]:
        if k not in data:
            fail(f"Time-Island missing key: {k}")
else:
    fail(f"Missing {ti_p}")

if not ok:
    sys.exit(1)
print("All example checks passed.")
