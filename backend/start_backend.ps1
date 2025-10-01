# Script para arrancar el backend FastAPI con Uvicorn
cd $PSScriptRoot
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000