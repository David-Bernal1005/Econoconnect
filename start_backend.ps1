$env:PYTHONPATH = "$(Get-Location)"
& "../.venv/Scripts/uvicorn.exe" backend.app.main:app --reload --host 127.0.0.1 --port 8000
