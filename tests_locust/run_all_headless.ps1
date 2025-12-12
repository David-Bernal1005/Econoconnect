<#
Script: run_all_headless.ps1
Descripción: Automatiza creación de entorno, instalación de dependencias, arranque del backend y ejecución headless de todas las pruebas Locust.
Prerequisitos:
  - Python 3.11+ instalado y accesible como 'python' en PATH.
Uso:
  1. Abrir PowerShell en la raíz del repo.
  2. Ejecutar:  powershell -ExecutionPolicy Bypass -File tests_locust\run_all_headless.ps1
Salida:
  - Logs en tests_locust\logs\*.log
  - Resultados en consola.
Notas:
  - Si ya tienes el backend levantado, puedes comentar la sección de Start-Process uvicorn.
  - Ajusta usuarios / spawn-rate según tus necesidades.
#>

$ErrorActionPreference = 'Stop'

function Ensure-Python {
    if (!(Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Error 'Python no encontrado en PATH. Instala Python y vuelve a ejecutar.'
    }
}

function Ensure-Venv {
    if (!(Test-Path 'ec')) {
        Write-Host 'Creando entorno virtual ec/' -ForegroundColor Cyan
        python -m venv ec
    }
}

function Activate-Venv {
    $activate = Join-Path (Get-Location) 'ec\\Scripts\\Activate.ps1'
    if (!(Test-Path $activate)) { Write-Error 'Activate.ps1 no encontrado. Venv corrupto.' }
    Write-Host 'Activando entorno virtual...' -ForegroundColor Cyan
    . $activate
}

function Install-Requirements {
    Write-Host 'Instalando dependencias (requirements.txt)...' -ForegroundColor Cyan
    try {
        pip install --upgrade pip > $null
    } catch {
        Write-Warning 'No se pudo actualizar pip automáticamente. Continuando con la versión actual de pip.'
    }

    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Warning 'Falló la instalación completa de requirements.txt. Instalando paquetes mínimos para ejecutar Locust y el backend...'
        pip install fastapi uvicorn httpx locust
    }
}

function Start-Backend {
    Write-Host 'Arrancando backend FastAPI (uvicorn)...' -ForegroundColor Cyan
    $backendDir = Join-Path (Get-Location) 'backend'
    $backendProcess = Start-Process -FilePath python -ArgumentList '-m uvicorn app.main:app --host 127.0.0.1 --port 8000' -WorkingDirectory $backendDir -PassThru
    Write-Host "PID backend: $($backendProcess.Id)" -ForegroundColor Yellow
    Write-Host 'Esperando a que el backend responda...' -ForegroundColor Cyan
    $maxRetries = 30; $ready = $false
    for ($i=0;$i -lt $maxRetries;$i++) {
        try {
            $resp = Invoke-WebRequest -Uri 'http://127.0.0.1:8000' -UseBasicParsing -TimeoutSec 3
            if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 500) { $ready = $true; break }
        } catch { Start-Sleep -Seconds 1 }
    }
    if (-not $ready) { Write-Warning 'Backend no respondió a tiempo. Continuando (puede fallar Locust).'}
    return $backendProcess
}

function Run-LocustSuite {
    param(
        [string]$File,
        [string]$Users = '10',
        [string]$SpawnRate = '2',
        [string]$Runtime = '1m'
    )
    if (!(Test-Path $File)) { Write-Error "Archivo $File no existe." }
    $name = [IO.Path]::GetFileNameWithoutExtension($File)
    $logDir = 'tests_locust\\logs'
    if (!(Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
    $logFile = Join-Path $logDir "$name.log"
    Write-Host "Ejecutando suite $name (headless)..." -ForegroundColor Green
    # Ejecuta locust headless y redirige salida
    locust -f $File --host http://127.0.0.1:8000 --headless -u $Users -r $SpawnRate --run-time $Runtime *>&1 | Tee-Object -FilePath $logFile
}

# ------------------------------------------------------------
# Flujo principal
# ------------------------------------------------------------
Ensure-Python
Ensure-Venv
Activate-Venv
Install-Requirements
$backend = Start-Backend

# Ejecutar cada suite
Run-LocustSuite -File 'tests_locust/test_funcionalidad.py' -Users 10 -SpawnRate 2 -Runtime '1m'
Run-LocustSuite -File 'tests_locust/test_rendimiento.py'   -Users 15 -SpawnRate 5 -Runtime '1m'
Run-LocustSuite -File 'tests_locust/test_seguridad.py'     -Users 5  -SpawnRate 2 -Runtime '1m'
Run-LocustSuite -File 'tests_locust/test_compatibilidad.py'-Users 6  -SpawnRate 2 -Runtime '1m'
Run-LocustSuite -File 'tests_locust/test_usabilidad.py'    -Users 8  -SpawnRate 2 -Runtime '1m'

Write-Host 'Finalizando backend...' -ForegroundColor Cyan
if ($backend -and !$backend.HasExited) { $backend | Stop-Process }
Write-Host 'Ejecución completa. Revisar logs en tests_locust\logs' -ForegroundColor Magenta
