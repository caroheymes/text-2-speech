---
title: Experience utilisateur et architecture d'interaction (Text2Speech)
status: draft
created: 2026-10-28
updated: 2026-10-28
---

# Experience: Lecteur vocal accessible

## 1. Fondations et posture ergonomique

Ce document definit les comportements, les etats interactifs et les regles d'accessibilite pour l'application d'assistance vocale. L'identite visuelle, les couleurs et la typographie sont regies par [DESIGN.md](file:///C:/Users/Admin/Desktop/servitudes/text2speech/DESIGN.md).

L'application repond a deux surfaces d'utilisation:
- Surface Web (Streamlit): espace complet de depot, parametrage et consultation textuelle / audio.
- Surface OS Locale (Windows Explorer): declenchement direct par clic droit sans manipulation graphique prealable.

L'objectif cardinal de l'experience est l'allegement de la charge mentale: zero formalite technique superflue, retour d'etat immediat et restitution sonore instantanee.

## 2. Architecture de l'information (IA)

Le parcours dans l'interface Streamlit suit un flux vertical lineaire unique sans pagination ni navigation complexe:

```
[Entete: Titre et promesse claire]
               │
               ▼
[Etape 1: Zone de depot documentaire]
               │ (Fichier valide detecte)
               ▼
[Etape 2: Choix du mode d'ecoute (3 options distinctes)]
               │
               ▼
[Action: Bouton principal "Generer et ecouter"]
               │
               ├──────────────────────────────────────────────┐
               ▼                                              ▼
[Affichage prioritaire du texte transcrit]    [Lecteur audio dynamique integre]
                                                              │
                                                              ▼
                                              [Reglage de vitesse en temps reel]
```

La barre laterale (Sidebar) regroupe les parametres d'environnement qui n'ont pas besoin d'etre modifies a chaque document (choix du fournisseur IA/BYOK, choix de la voix, duree de pause inter-phrases).

## 3. Voix et micro-redaction (Voice & Tone)

Le ton adopte est sobre, bienveillant, respectueux et direct. Il bannit toute infantilisation ou paternalisme lie au handicap:

- Descriptifs fonctionnels limpides: "Synthese eclair (< 1 minute)", "Resume a mi-longueur", "Lecture integrale".
- Retours d'erreur sans culpabilisation: "Le fichier Word depose semble vide ou protege par un mot de passe", plutot qu'une erreur technique "Invalid docx structure".
- Confirmation sans verbiage: "Document charge: note_synthese.pdf (420 mots detectes)".

## 4. Etats de l'application (State Patterns)

### 4.1 Etat initial (A vide)
- La zone de depot est active et invite au glisser-deposer.
- Le bouton "Generer et ecouter" reste inactif tant qu'aucun document valide n'est depose.
- Aucun lecteur sonore n'est affiche pour eviter toute confusion visuelle.

### 4.2 Etat document charge
- Le nom du document et le volume de mots s'affichent sous fond vert pale (`{colors.success-subtle}`).
- Le choix par defaut se positionne sur "Synthese eclair (< 1 min)" [ASSUMPTION: choix le plus frequemment recherche par les utilisateurs presses].
- Le bouton principal devient clickable avec surbrillance bleue.

### 4.3 Etat condensation et synthese (Chargement)
- Le bouton principal est desactive pendant le traitement.
- Un indicateur discret informe de l'etape active: "Preparation et condensation du texte...", puis "Synthese vocale haute fidelite en cours...".
- Delai cible: moins de 4 secondes pour la synthese eclair.

### 4.4 Etat lecture active
- Dès que le texte condense est calcule, il s'affiche dans un bloc de previsualisation deplie pour permettre a l'utilisateur de commencer a lire des yeux s'il le souhaite.
- Le lecteur audio demarre automatiquement (`autoplay: true`).
- La barre de defilement temporel avance et le chronometre de position s'actualise.

### 4.5 Etat erreur de traitement
- En cas de cle API invalide ou de document corrompu, une alerte fond rouge pale apparait avec une consigne claire de resolution immediate (ex: "Verifiez votre cle API Gemini dans la barre laterale ou basculez en mode Heuristique autonome").

## 5. Primitives d'interaction et acceleration

### 5.1 Manipulation de la vitesse en direct (Zero-Latency Speed Scrub)
La vitesse n'impose aucune re-generation sonore. Les boutons de cadence (0.85x, 1.0x, 1.2x, 1.5x) ou le curseur fin modifient la frequence d'horloge du lecteur en plein cours d'ecoute:
- L'utilisateur percoit l'acceleration des la milliseconde ou il clique.
- Aucun gresillement ni artefact de hauteur n'est produit grace a l'algorithme d'etirement temporel du navigateur (WSOLA).

### 5.2 Espacement des phrases
Pour les auditeurs souffrant de saturation cognitive, l'option de pause inter-phrases dans la barre laterale introduit un silence parametre (de 0.2s a 2.5s) permettant a l'esprit de structurer les propositions entendues avant le demarrage de la phrase suivante.

## 6. Accessibilite socle (Accessibility Floor)

- Ratio de contraste: conformite WCAG 2.1 AAA (ratio superieur a 7:1) pour l'ensemble des textes et elements d'action.
- Reperage clavier: navigation seculaire par touche Tabulation avec contour de focus bleu vif de 2 pixels `{colors.border-focus}`.
- Cible tactile minimale: 44 x 44 pixels pour chaque zone cliquable.
- Support des lecteurs d'ecran: les composants HTML5 (`<audio>`) disposent d'attributs `aria-label` clairs permettant la pause et la reprise via les technologies d'assistance natives (NVDA, JAWS, Narrateur Windows).

## 7. Parcours cles (Key Flows)

### UJ-1. Synthese d'un rapport long en moins de 60 secondes
1. L'utilisateur glisse un document de 10 pages dans l'application.
2. Il conserve le choix preselectionne "Synthese eclair".
3. Il clique sur "Generer et ecouter".
4. Le texte en trois parties (De quoi ca parle, Apports, Synthese operationnelle) s'affiche.
5. La voix chaude demarre et delivre l'essentiel en 45 secondes.

### UJ-4. Ecoute contextuelle depuis l'explorateur Windows
1. L'utilisateur repere un document PDF sur son bureau.
2. Il effectue un clic droit et clique sur "Ecouter ce document".
3. Une fenetre compacte de 380x190px apparait immediatement en premier plan.
4. La synthese vocale demarre sans ouvrir de navigateur. L'utilisateur appuie sur Espace ou clique sur "Pause" pour interrompre a tout moment.

## 8. Index des hypotheses retenues

- [ASSUMPTION-1]: La synthese eclair en trois volets reste le mode par defaut le plus efficient pour les personnes fuyant l'epuisement textuel.
- [ASSUMPTION-2]: L'acceleration audio doit toujours s'effectuer localement sans relancer de requete serveur afin de garantir l'absence totale de friction.
