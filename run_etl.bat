@echo off
python etl\\run_etl.py
if errorlevel 1 exit /b 1
