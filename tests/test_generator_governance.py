
from pathlib import Path
import json
import subprocess
import hashlib

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT/"analytics/python/generate_data.py"
OUT = ROOT/"data/generated"

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def test_reproducibility_same_seed():
    subprocess.run(["python", str(GEN)], check=True, cwd=ROOT)
    first = {p.name: sha256(p) for p in OUT.glob("*.csv")}
    subprocess.run(["python", str(GEN)], check=True, cwd=ROOT)
    second = {p.name: sha256(p) for p in OUT.glob("*.csv")}
    assert first == second

def test_no_forced_target_scaling_pattern():
    text = GEN.read_text()
    forbidden = ["target/down.sum()", "target = 132", "target=132", "==14", "== 14"]
    assert all(x not in text for x in forbidden)
