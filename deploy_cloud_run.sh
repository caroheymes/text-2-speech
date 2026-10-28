#!/bin/bash
set -e

SERVICE_NAME="${1:-text2speech}"
REGION="${2:-europe-west1}"

echo "========================================================"
echo " Deploiement sur Google Cloud Run: ${SERVICE_NAME}"
echo " Configuration Serverless: Scale-to-Zero actif"
echo "========================================================"

CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ -z "$CURRENT_PROJECT" ]; then
    echo "Erreur: aucun projet GCP defini. Configurez-le via 'gcloud config set project <ID_PROJET>'."
    exit 1
fi

echo "Projet cible : ${CURRENT_PROJECT}"
echo "Region cible : ${REGION}"

gcloud run deploy "${SERVICE_NAME}" \
    --source . \
    --platform managed \
    --region "${REGION}" \
    --allow-unauthenticated \
    --min-instances 0 \
    --max-instances 3 \
    --memory 1Gi \
    --cpu 1 \
    --timeout 300

echo ""
echo "Deploiement effectue avec succes."
echo "L'instance ne s'activera qu'a la reception d'une requete sur son URL."
