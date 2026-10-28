# Lancement rapide de l'application Streamlit Text2Speech
$ProjectRoot = $PSScriptRoot
$env:PYTHONPATH = $ProjectRoot
$StreamlitExe = Join-Path $ProjectRoot ".venv\Scripts\streamlit.exe"
$AppPy = Join-Path $ProjectRoot "src\app.py"

Write-Host "Demarrage du serveur Streamlit sur le port 9001..." -ForegroundColor Cyan
& $StreamlitExe run $AppPy --server.port 9001 --server.address 0.0.0.0 --server.headless true
