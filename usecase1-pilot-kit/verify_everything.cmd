@echo off
setlocal
cd /d "%~dp0"
set "PYTHONPATH=%CD%\source;%PYTHONPATH%"
py -3 -W error::ResourceWarning -m unittest discover -s tests -p "test_genuity_reconcile.py" -v
if errorlevel 1 exit /b %errorlevel%
py -3 -m genuity_reconcile verify --output-dir demo_output
exit /b %errorlevel%
