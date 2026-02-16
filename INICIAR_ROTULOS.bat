@echo off
setlocal

cd /d %~dp0

call .venv\Scripts\activate
start "" http://127.0.0.1:8000/rotulos
uvicorn app.main:app --host 127.0.0.1 --port 8000

endlocal
pause