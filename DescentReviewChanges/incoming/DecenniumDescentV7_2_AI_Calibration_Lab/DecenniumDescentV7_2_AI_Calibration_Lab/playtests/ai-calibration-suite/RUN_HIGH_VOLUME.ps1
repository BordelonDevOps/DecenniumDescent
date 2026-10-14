$ErrorActionPreference = 'Stop'
$env:DD_TRAIN_RUNS = '200'
$env:DD_HOLDOUT_RUNS = '1000'
$env:DD_OBJECTIVE_RUNS = '1000'
$env:DD_EXPEDITION_RUNS = '10000'
$env:DD_HAVEN_RUNS = '100000'
$env:DD_CYCLE_RUNS = '50000'
$env:DD_FUZZ_RUNS = '1000000'
python playtests/ai-calibration-suite/tools/run_all_math.py
