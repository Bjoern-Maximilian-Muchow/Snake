$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$venv = Join-Path $repo ".station-venv"
$python = Join-Path $venv "Scripts\python.exe"

if (-not (Test-Path -LiteralPath $python)) {
  Write-Host "Erzeuge isolierte Python-Umgebung für die AutoSnake-Station ..."
  python -m venv $venv
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Write-Host "Installiere Stationsabhängigkeiten ..."
& $python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $python -m pip install -r (Join-Path $repo "station\requirements.txt")
exit $LASTEXITCODE
