# Test Volume Presets

## Standard calibration

Run `RUN_PREPARATION.ps1` or `npm run test:ai:prepare`.

Approximate executable volume before persona agents:

- 43,200 training combat runs
- 12,000 holdout combat runs
- 60,000 objective encounters
- 96,000 full expedition simulations
- 100,000 Haven transactions
- 10,000 ten-year Cycles
- 100,000 fuzzed rule states

## High-volume calibration

Run `RUN_HIGH_VOLUME.ps1`.

Approximate executable volume before persona agents:

- 216,000 training combat runs
- 120,000 holdout combat runs
- 300,000 objective encounters
- 480,000 full expedition simulations
- 500,000 Haven transactions
- 50,000 ten-year Cycles
- 1,000,000 fuzzed rule states

The high-volume preset is intentionally expensive. Cursor must retain raw outputs, use disjoint training and holdout seeds, and never edit canon automatically.
