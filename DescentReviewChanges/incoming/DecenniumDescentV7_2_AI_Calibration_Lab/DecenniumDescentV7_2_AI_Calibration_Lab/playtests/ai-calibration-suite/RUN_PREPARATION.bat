@echo off
python playtests\ai-calibration-suite\tools\run_all_math.py
if errorlevel 1 exit /b %errorlevel%
