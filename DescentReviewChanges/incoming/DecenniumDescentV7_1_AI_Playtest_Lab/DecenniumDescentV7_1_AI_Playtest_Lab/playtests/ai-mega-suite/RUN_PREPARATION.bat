@echo off
python playtests\ai-mega-suite\tools\run_all_preparation.py
if errorlevel 1 exit /b %errorlevel%
echo Preparation complete. Paste CURSOR_MASTER_ORCHESTRATOR_PROMPT.md into Cursor.
