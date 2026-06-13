param(
  [int]$Port = 5000,
  [string]$ArduinoPort = "COM3"
)

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = Join-Path $repo ".station-venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $python)) {
  Write-Error "Stationsumgebung fehlt. Zuerst .\scripts\setup_station.ps1 ausführen."
  exit 1
}

Write-Host "AutoSnake-Station startet auf http://localhost:$Port/pty"
Write-Host "Repository: $repo"
Write-Host "Arduino: $ArduinoPort"
Write-Host "Dieses Fenster für die Dauer der Edrys-Station geöffnet lassen."

& $python (Join-Path $repo "station\server.py") `
  --host 127.0.0.1 `
  --port $Port `
  --arduino-port $ArduinoPort
