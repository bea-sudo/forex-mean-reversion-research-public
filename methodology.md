# Methodology

## Strategy family

The private engine belongs to the mean-reversion family: it looks for conditions where price appears stretched relative to a reference equilibrium and tests whether subsequent movement tends to revert.

The exact signal formula, thresholds, risk parameters, and execution rules are private.

## Trade-result encoding

Completed trades are reduced to:

- `1` = profitable completed trade
- `0` = losing completed trade

Excluded / break-even observations can break the sequence instead of being bridged.

## Pattern analysis

The public research layer scans five-result sequences.

Example:

```text
00110
```

For every historical occurrence, the next completed result is recorded.

A candidate must have:

- at least 100 occurrences
- at least 55% next-result win rate

## Rolling stability

Candidate occurrences remain chronological.

The first 10 form the initial baseline. Every following group of 10 is compared with the pattern's historical win rate before that batch.

The z-score is:

```text
z = (p_batch - p_history)
    / sqrt(p_history * (1 - p_history) / n)
```

with `n = 10`.

The public stability threshold is:

```text
|z| < 1.96
```

A pattern is labeled unstable if a checked batch crosses the threshold.

## Why this exists

A high full-sample win rate can hide deterioration.

The rolling test tries to answer a different question:

> Did the pattern behave reasonably consistently as new observations arrived?

That is still not the same as proving live profitability.
