@echo off
setlocal
cd /d "%~dp0"
set "PYTHONPATH=%CD%\source;%PYTHONPATH%"
py -3 -m genuity_reconcile demo --output-dir demo_output --overwrite-demo
exit /b %errorlevel%
