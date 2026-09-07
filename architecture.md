# Architecture

The public repository mirrors the real project without exposing the proprietary rule set.

```text
FX market
   ↓
[PRIVATE SIGNAL ENGINE]
   ↓
trade entries / exits
   ↓
completed trade results
   ↓
research/summarize_trades.py
   ↓
research/pattern_stability.py
   ↓
stable / unstable pattern reports
```

## Private boundary

The strategy engine is treated as a black box.

Public code can consume its completed results, but does not contain the formula that decides when to enter or exit.

This makes the repository useful as a portfolio project while keeping the actual trading logic private.
