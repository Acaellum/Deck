@echo off
title DECK — Document Extraction and Conversion Kit | Offline AI Workbench
echo Starting DECK local offline AI server at http://127.0.0.1:8000 ...
start "" http://127.0.0.1:8000
"%~dp0.venv\Scripts\python.exe" "%~dp0app.py"
