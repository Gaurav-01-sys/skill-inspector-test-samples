#!/usr/bin/env python3
"""Local, read-only CSV profiler. No network. No shell."""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

MAX_ROWS = 100_000


def infer(values):
    nums = dates = 0
    nonempty = [v for v in values if v.strip()]
    if not nonempty:
        return "empty"
    for v in nonempty[:200]:
        try:
            float(v.replace(",", ""))
            nums += 1
            continue
        except ValueError:
            pass
        if len(v) >= 8 and v[4:5] in "-/":
            dates += 1
    n = min(len(nonempty), 200)
    if nums / n > 0.8:
        return "number"
    if dates / n > 0.8:
        return "date-like"
    return "string"


def main(path_str: str) -> None:
    path = Path(path_str)
    if path.suffix.lower() != ".csv" or not path.is_file():
        raise SystemExit("Provide an existing local .csv path.")

    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            print(json.dumps({"error": "empty file"}))
            return
        cols = [[] for _ in header]
        rows = 0
        sampled = False
        for row in reader:
            rows += 1
            if rows <= MAX_ROWS:
                for i, val in enumerate(row[: len(cols)]):
                    cols[i].append(val)
            else:
                sampled = True
                break

    report = {
        "file": path.name,
        "rows_seen": rows,
        "sampled": sampled,
        "columns": [],
    }
    for name, values in zip(header, cols):
        missing = sum(1 for v in values if not str(v).strip())
        examples = [v[:40] for v in values if str(v).strip()][:3]
        report["columns"].append(
            {
                "name": name,
                "inferred_type": infer(values),
                "missing_pct": round(100.0 * missing / max(len(values), 1), 1),
                "examples": examples,
            }
        )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: summarize_csv.py <file.csv>")
    main(sys.argv[1])
