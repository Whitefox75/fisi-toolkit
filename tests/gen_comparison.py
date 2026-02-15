import sys
import os
import random

# Add parent directory to path to import fisi_toolkit
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fisi_toolkit import UnitConverterEngine

def generate_cases():
    engine = UnitConverterEngine()
    units = engine.unit_names
    
    interesting_pairs = [
        ("KB", "Byte"), ("KiB", "Byte"), 
        ("GB", "MB"), ("GiB", "MiB"),
        ("TB", "TiB"), ("Bit", "Byte")
    ]
    
    with open("tests/comparison_results.md", "w", encoding="utf-8") as f:
        f.write("# Local Unit Helper Conversion Results\n\n")
        f.write("| # | Value | Source | Dest | Local Result | Bytes Value |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        count = 1
        # 1. Guaranteed interesting cases (12 cases)
        for src, dst in interesting_pairs:
            vals = [1.0, random.randint(2, 500)]
            for v in vals:
                res, bytes_val = engine.convert(v, src, dst)
                f.write(f"| {count} | {v} | {src} | {dst} | {res:g} | {bytes_val:g} |\n")
                count += 1

        # 2. Random checks
        while count <= 50:
            src = random.choice(units)
            dst = random.choice(units)
            if src == dst: continue
            
            val = round(random.uniform(0.1, 10000.0), 4)
            res, bytes_val = engine.convert(val, src, dst)
            f.write(f"| {count} | {val} | {src} | {dst} | {res:g} | {bytes_val:g} |\n")
            count += 1


if __name__ == "__main__":
    generate_cases()
