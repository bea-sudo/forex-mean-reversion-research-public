# Forex Mean-Reversion Research

A public research shell for a private FX mean-reversion strategy.

This repository documents the **research process, validation pipeline, and statistical tooling** while intentionally excluding the proprietary entry/exit rules and private parameter values.

## Project idea

The private strategy is a rules-based FX mean-reversion system.

The public research workflow is:

```text
Market data
    ↓
Private mean-reversion signal engine
    ↓
Completed trade export
    ↓
Trade-result encoding
    ↓
Binary pattern scan
    ↓
Minimum occurrence / win-rate filter
    ↓
Rolling 10-occurrence z-score stability test
    ↓
Stable research candidates
```

## What is public

- Project architecture
- Research methodology
- Generic TradingView strategy shell
- Trade-result analysis code
- Binary pattern scanner
- Rolling z-score stability checker
- Synthetic sample data
- Reproducible output format

## What is private

The following are intentionally excluded:

- Exact entry rules
- Exact indicator thresholds
- Exact stop-loss / take-profit logic
- Private parameter values
- Broker-specific execution assumptions
- Raw historical trading exports
- Signal-ranking logic
- Live execution logic

The real strategy core belongs in `private/`, which is ignored by Git.

## Research defaults

The public pattern research module uses:

```text
Pattern length      = 5
Minimum occurrences = 100
Minimum win rate    = 55%
Batch size          = 10 occurrences
Stable threshold    = |z| < 1.96
```

These are research settings, not a claim of guaranteed profitability.

## Repository structure

```text
forex-mean-reversion-research-public/
├── README.md
├── requirements.txt
├── .gitignore
├── strategy/
│   └── public_strategy_shell.pine
├── research/
│   ├── pattern_stability.py
│   └── summarize_trades.py
├── docs/
│   ├── architecture.md
│   ├── methodology.md
│   └── limitations.md
├── sample_data/
│   └── sample_trade_results.csv
└── private/
    └── README_PRIVATE.txt
```

## Run the public research tool

```bash
pip install -r requirements.txt
python research/pattern_stability.py sample_data/sample_trade_results.csv
```

## Output

The scanner creates:

```text
STABLE_patterns.csv
UNSTABLE_patterns.csv
pattern_every_10_zscores.csv
```

## Important

This is a quantitative-research project, not financial advice and not proof of a live trading edge.

A backtest can look respectable and still fail once spread, slippage, execution, regime change, or plain bad luck arrive to collect rent.
