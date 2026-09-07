from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import math
import pandas as pd

PATTERN_LENGTH = 5
MIN_OCCURRENCES = 100
MIN_WIN_RATE = 55.0
BATCH_SIZE = 10
Z_LIMIT = 1.96


def load_sequence(csv_path: Path) -> list[int | None]:
    df = pd.read_csv(csv_path)

    if "Result" not in df.columns:
        raise ValueError("CSV must contain a chronological 'Result' column.")

    sequence: list[int | None] = []

    for value in df["Result"]:
        if pd.isna(value):
            sequence.append(None)
            continue

        try:
            value = int(value)
        except (TypeError, ValueError):
            sequence.append(None)
            continue

        sequence.append(value if value in (0, 1) else None)

    return sequence


def scan_patterns(sequence):
    occurrences = defaultdict(list)

    for i in range(PATTERN_LENGTH, len(sequence)):
        prev = sequence[i - PATTERN_LENGTH:i]
        nxt = sequence[i]

        if nxt is None or any(v is None for v in prev):
            continue

        pattern = "".join(str(v) for v in prev)
        occurrences[pattern].append(int(nxt))

    return occurrences


def z_score(batch_rate_pct, historical_rate_pct, n):
    p_batch = batch_rate_pct / 100.0
    p_hist = historical_rate_pct / 100.0

    variance = p_hist * (1.0 - p_hist) / n
    if variance <= 0:
        return 0.0

    return (p_batch - p_hist) / math.sqrt(variance)


def analyze(pattern, results):
    n = len(results)

    if n < MIN_OCCURRENCES:
        return None, []

    wins = sum(results)
    win_rate = wins / n * 100.0

    if win_rate < MIN_WIN_RATE:
        return None, []

    batches = []
    stable = True

    # First 10 occurrences form the initial historical baseline.
    start = BATCH_SIZE
    batch_number = 1

    while start + BATCH_SIZE <= n:
        history = results[:start]
        batch = results[start:start + BATCH_SIZE]

        hist_rate = sum(history) / len(history) * 100.0
        batch_rate = sum(batch) / len(batch) * 100.0
        z = z_score(batch_rate, hist_rate, BATCH_SIZE)

        batch_stable = abs(z) < Z_LIMIT
        if not batch_stable:
            stable = False

        batches.append({
            "Pattern": pattern,
            "Batch": batch_number,
            "Occurrence_Start": start + 1,
            "Occurrence_End": start + BATCH_SIZE,
            "Historical_Win_Rate_Before_Batch_Pct": round(hist_rate, 3),
            "Batch_Win_Rate_Pct": round(batch_rate, 3),
            "Z_Score": round(z, 3),
            "Batch_Status": "STABLE" if batch_stable else "UNSTABLE",
        })

        start += BATCH_SIZE
        batch_number += 1

    worst_z = max((abs(x["Z_Score"]) for x in batches), default=None)

    summary = {
        "Pattern": pattern,
        "Occurrences": n,
        "Wins": wins,
        "Losses": n - wins,
        "Overall_Win_Rate_Pct": round(win_rate, 3),
        "Batches_Checked": len(batches),
        "Worst_Absolute_Z": round(worst_z, 3) if worst_z is not None else None,
        "Status": "STABLE" if stable else "UNSTABLE",
    }

    return summary, batches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path, help="CSV with chronological Result column")
    args = parser.parse_args()

    sequence = load_sequence(args.csv)
    patterns = scan_patterns(sequence)

    stable_rows = []
    unstable_rows = []
    batch_rows = []

    for pattern, results in patterns.items():
        summary, batches = analyze(pattern, results)

        if summary is None:
            continue

        (stable_rows if summary["Status"] == "STABLE" else unstable_rows).append(summary)
        batch_rows.extend(batches)

    pd.DataFrame(stable_rows).to_csv("STABLE_patterns.csv", index=False)
    pd.DataFrame(unstable_rows).to_csv("UNSTABLE_patterns.csv", index=False)
    pd.DataFrame(batch_rows).to_csv("pattern_every_10_zscores.csv", index=False)

    print(f"Patterns scanned : {len(patterns)}")
    print(f"Stable patterns  : {len(stable_rows)}")
    print(f"Unstable patterns: {len(unstable_rows)}")


if __name__ == "__main__":
    main()
