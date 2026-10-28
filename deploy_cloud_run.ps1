# Script de deploiement automatise sur Google Cloud Run avec Scale-to-Zero
param(
    [string]$Project = "",
    [string]$Region = "europe-west1",
    [string]$ServiceName = "text2speech"
)

$ErrorActionPreference = "Stop"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " Deploiement sur Google Cloud Run: $ServiceName" -ForegroundColor Cyan
Write-Host " Configuration Serverless: Scale-to-Zero actif" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

if ($Project -ne "") {
    Write-Host "Configuration du projet Google Cloud : $Project"
    gcloud config set project $Project
}

$CurrentProject = (gcloud config get-value project 2>$null).Trim()
if (-not $CurrentProject) {
    Write-Error "Aucun projet GCP selectionne. Executez 'gcloud config set project <ID_PROJET>' ou passez l'argument -Project."
    exit 1
}

Write-Host "Projet GCP cible : $CurrentProject"
Write-Host "Region cible : $Region"
Write-Host "Lancement du deploiement (creation d'image via Cloud Build et mise en ligne)..."

gcloud run deploy $ServiceName `
    --source . `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --min-instances 0 `
    --max-instances 3 `
    --memory 1Gi `
    --cpu 1 `
    --timeout 300

Write-Host "`nDeploiement effectue avec succes !" -ForegroundColor Green
Write-Host "L'instance reste eteinte (0 conteneur actif = 0 cout) et ne demarrera que lors d'un appel sur son URL." -ForegroundColor Green
