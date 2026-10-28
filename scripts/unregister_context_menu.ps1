# Script PowerShell de desinstallation du menu contextuel Windows

$Extensions = @(".pdf", ".docx", ".txt", ".md")

foreach ($ext in $Extensions) {
    $BasePath = "HKCU:\Software\Classes\SystemFileAssociations\$ext\shell\Text2Speech"
    if (Test-Path $BasePath) {
        Remove-Item -Path $BasePath -Recurse -Force
        Write-Host "Menu contextuel supprime pour l'extension $ext"
    }
}

Write-Host "Desinstallation du menu contextuel terminee avec succes."
