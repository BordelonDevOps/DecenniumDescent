@echo off
set DD_TRAIN_RUNS=200
set DD_HOLDOUT_RUNS=1000
set DD_OBJECTIVE_RUNS=1000
set DD_EXPEDITION_RUNS=10000
set DD_HAVEN_RUNS=100000
set DD_CYCLE_RUNS=50000
set DD_FUZZ_RUNS=1000000
python playtests\ai-calibration-suite\tools\run_all_math.py
if errorlevel 1 exit /b %errorlevel%
