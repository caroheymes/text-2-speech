# Script PowerShell d'enregistrement du menu contextuel Windows (HKCU - sans droits administrateur)

$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Item $PSScriptRoot).Parent.FullName
$PythonwExe = Join-Path $ProjectRoot ".venv\Scripts\pythonw.exe"
$LauncherPy = Join-Path $ProjectRoot "launcher.py"

if (-not (Test-Path $PythonwExe)) {
    Write-Error "L'interpreteur Pythonw est introuvable a l'emplacement: $PythonwExe. Installez l'environnement virtuel au prealable."
    exit 1
}

$Extensions = @(".pdf", ".docx", ".txt", ".md")
$MenuLabel = "Ecouter ce document (Synthese vocale)"
$CommandStr = "`"$PythonwExe`" `"$LauncherPy`" `"%1`""

foreach ($ext in $Extensions) {
    $BasePath = "HKCU:\Software\Classes\SystemFileAssociations\$ext\shell\Text2Speech"
    $CommandPath = "$BasePath\command"

    New-Item -Path $BasePath -Force | Out-Null
    Set-ItemProperty -Path $BasePath -Name "(Default)" -Value $MenuLabel
    Set-ItemProperty -Path $BasePath -Name "Icon" -Value "shell32.dll,168"

    New-Item -Path $CommandPath -Force | Out-Null
    Set-ItemProperty -Path $CommandPath -Name "(Default)" -Value $CommandStr

    Write-Host "Menu contextuel enregistre pour l'extension $ext"
}

Write-Host "Enregistrement effectue avec succes. Vous pouvez desormais faire un clic droit sur un fichier pour l'ecouter."
