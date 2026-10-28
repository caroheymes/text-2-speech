# Guide de reprise de la session

Ce document resume l'etat du projet Text2Speech et detaille les etapes exactes pour reprendre le developpement sans perte de contexte.

## Identifiants de la session

- Identifiant de conversation: `326d155e-d36b-4d22-ac28-d56d4c249551`
- Repertoire de travail: `C:\Users\Admin\Desktop\servitudes\text2speech`
- Depot distant GitHub: `https://github.com/caroheymes/text-2-speech.git`
- Service de production Cloud Run: `https://text2speech-948219637422.europe-west1.run.app`

## Etat du code et des branches Git

Le projet dispose de deux branches distantes sur GitHub:

- `origin/master`: socle initial de l'application (Streamlit local, extraction de documents, integration clic droit Windows, mini-lecteur de bureau Tkinter, moteur TTS neuronal).
- `origin/cloud-run`: configuration conteneurisee complete pour Google Cloud Run (Dockerfile, scripts de deploiement, scale-to-zero, limitation budgetaire a 3 EUR, schema d'architecture Eraser).

La branche de travail courante en local est `cloud-run` (ou `feature/cloud-run`).

## Commandes directes pour reprendre le travail

### 1. Se positionner dans le dossier et synchroniser

Dans un terminal PowerShell:

```powershell
cd C:\Users\Admin\Desktop\servitudes\text2speech
git checkout cloud-run
git pull origin cloud-run
```

### 2. Lancer l'environnement virtuel et executer les tests

Pour verifier l'integrite du socle (17 tests unitaires):

```powershell
.venv\Scripts\pytest tests/ -v
```

### 3. Lancer l'application en local

- Via le script PowerShell:
  ```powershell
  .\start_app.ps1
  ```
- Ou en double-cliquant sur `launch.bat`.
- L'interface s'ouvre sur `http://localhost:9001`.

### 4. Partager localement sans deploiement

Pour generer un lien public temporaire depuis la machine locale:
- Double-cliquer sur `partager.bat` (tunnel Cloudflare direct vers le port 9001).

### 5. Redeployer sur Google Cloud Run

Si des modifications sont apportees au code pour la production en ligne:

```powershell
.\deploy_cloud_run.ps1 -Project "cover-letter-app-479600" -Region "europe-west1"
```

## Parametres de securite budgetaire en place

- Projet Google Cloud actif: `cover-letter-app-479600`
- Plafond budgetaire Google Cloud: 3 EUR / mois (alerte a 50%, 80% et 100%)
- Echelle Cloud Run: `--min-instances 0` (scale-to-zero absolu) et `--max-instances 1` (aucun debordement d'instances)
- Mode CPU: `--cpu-throttling` (processeur coupe hors traitement de requete)

## Reprise de session avec un agent IA

Pour reprendre cette conversation avec un assistant (Antigravity ou autre), copier-coller le prompt suivant des le debut de la nouvelle session:

```text
Je reprends le projet text2speech situe dans C:\Users\Admin\Desktop\servitudes\text2speech.
Le depot GitHub est https://github.com/caroheymes/text-2-speech.git avec les branches master et cloud-run.
L'application est deployee sur Google Cloud Run (https://text2speech-948219637422.europe-west1.run.app) avec extinction a zero instances et budget mensuel plafonne a 3 EUR sur le projet cover-letter-app-479600.
Les 17 tests unitaires sont dans tests/ et passent tous.
Consulte REPRISE.md et README.md pour continuer le developpement.
```
