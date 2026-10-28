---
title: PRD Lecteur Vocal Accessible (Text2Speech)
status: draft
created: 2026-10-28
updated: 2026-10-28
---

# PRD: Lecteur vocal accessible (Text2Speech)

## 0. Contexte et objet du document

Ce document definit les exigences produit pour l'application d'assistance a la lecture par synthese vocale. Concu pour une execution fluide sous l'environnement Antigravity sur poste Windows, le systeme offre deux modalites d'acces: une interface graphique Streamlit et une entree directe par clic droit dans le menu contextuel de l'explorateur Windows. Il s'adresse aux developpeurs et concepteurs charges d'implementer la chaine de traitement: ingestion de documents, extraction de texte, generation de resumes adaptatifs et restitution vocale parametrable.

## 1. Vision du produit

Beaucoup d'utilisateurs eprouvent des difficultes avec la lecture continue de documents ecrits (fatigue visuelle, troubles cognitifs ou dyslexie, manque de temps, preference pour l'apprentissage auditif). L'outil convertit n'importe quel document depose ou selectionne en une experience d'ecoute immediate et fluide.

L'utilisateur garde le controle absolu sur le niveau de detail souhaite (flash express en 60 secondes, resume median a 50 %, ou lecture integrale) ainsi que sur la cadence d'elocution. L'integration au menu contextuel Windows supprime toute barriere d'entree: un simple clic droit sur un fichier lance l'audio sans manipulation prealable. L'execution s'articule directement au sein de l'environnement de commande Antigravity.

## 2. Utilisateurs cibles et cas d'usage

### 2.1 Objectifs utilisateurs (Jobs To Be Done)

Quand je repere un document dans mon explorateur de fichiers, je veux faire un clic droit dessus pour l'entendre immediatement sans devoir lancer une interface lourde.

Quand je dispose d'un document ecrit dense, je veux en ecouter une synthese actionnable en moins d'une minute pour decider si le contenu merite une lecture approfondie.

Quand je dois assimiler un rapport volumineux sans epuisement cognitif, je veux ecouter un resume a mi-longueur conservant l'ossature essentielle du texte d'origine.

Quand je ne peux pas ou ne veux pas lire a l'ecran, je veux lancer la lecture integrale du document d'un simple clic a la vitesse adaptee a ma capacite auditive.

### 2.2 Utilisateurs hors cible (version 1)

Le systeme ne vise pas le traitement de flux documentaires d'entreprise par lots automatises ni la traduction multilingue synchrone dans cette premiere version. Il cible l'usage individuel direct sur document unique.

### 2.3 Parcours utilisateurs cles

#### UJ-1. Marc ecoute la synthese operationnelle d'une note de service
Marc ouvre l'application Streamlit locale. Il depose un fichier PDF de 6 pages dans la zone de televersement. Il selectionne l'option "Condense (1 minute)", ajuste la vitesse a x1.1 et clique sur "Generer et ecouter". En quelques secondes, le lecteur audio integre demarre: Marc entend successivement le sujet traite, les apports cles et les actions requises. Marc quitte l'application informe sans avoir passe 20 minutes a dechiffrer le PDF.

#### UJ-2. Sophie suit un document administratif en resume a 50 %
Sophie eprouve une fatigue visuelle severe en fin de journee. Elle depose un document de reference au format Word (.docx). Elle selectionne "Resume 50 %" et conserve la vitesse standard x1.0. Le lecteur vocal demarre et deroule le contenu epure de ses digressions tout en conservant les arguments et chiffres cles.

#### UJ-3. Arthur lance la lecture integrale a vitesse reduite
Arthur suit un cours technique complexe. Il depose son document texte et choisit "Texte integral" avec une cadence ralentie a x0.85 pour mieux assimiler les concepts. L'audio demarre avec des commandes de pause, retour et reprise a volonte.

#### UJ-4. Claire ecoute directement une piece jointe depuis son explorateur Windows
Claire navigue dans ses dossiers de telechargements. Elle clique droit sur une convention PDF et choisit "Ecouter (Synthese vocale)" dans le menu contextuel. Une mini-fenetre de restitution audio apparait aussitot, resume les points cles a voix haute et propose des raccourcis simples pour mettre en pause ou basculer en lecture integrale.

## 3. Glossaire

Document source: fichier textuel ou bureautique televerse par l'interface ou pointe via l'explorateur (formats supportes: PDF, DOCX, TXT).

Synthese condensee: restitution structuree de moins de 60 secondes d'ecoute, decomposee en trois axes stricts (objet du texte, apports majeurs, synthese operationnelle).

Resume median: contraction de la masse textuelle a environ 50 % du volume d'origine, respectant la chronologie et les articulations majeures du propos.

Lecture integrale: lecture complete du texte brut extrait du document source, nettoyee des artefacts techniques (numeros de page, pieds de page parasites).

Vitesse d'elocution: facteur multiplicateur applique a la cadence du flux audio (plage standard 0.75x a 1.75x).

Moteur TTS: composant logiciel de synthese vocale transformant le texte traite en flux audio fluide.

Menu contextuel Windows: entree enregistree dans le registre utilisateur Windows Explorer pour declencher le traitement par clic droit sur un fichier.

## 4. Fonctionnalites et exigences fonctionnelles

### 4.1 Ingestion et extraction documentaire

L'application accepte le televersement de fichiers ou leur passage en parametre de ligne de commande.

#### FR-1: Depot de fichier unique et passage d'argument
L'utilisateur peut televerser un document aux formats PDF, DOCX ou TXT via l'interface Streamlit ou le cibler par chemin de fichier en argument de script. Realise UJ-1, UJ-2, UJ-3, UJ-4.

Consequences testables:
- L'application rejette les extensions non supportees avec un message d'erreur clair.
- Limite de taille fixee par defaut a 20 Mo.
- Le texte extrait est traite en session ou en processus temporaire sans persistence non sollicitee.

#### FR-2: Nettoyage et normalisation du texte
Le systeme supprime les sauts de ligne parasites, entetes repetitifs et coupures de mots avant traitement par le resume ou la voix.

Consequences testables:
- Les tirets de cesure en fin de ligne sont recolles avant lecture.
- Les blocs textuels vides ou composes exclusivement d'espaces sont ignores.

### 4.2 Traitement textuel selon l'option choisie

L'utilisateur dispose de trois modes de restitution mutuellement exclusifs pour chaque document charge.

#### FR-3: Option Condense express (format court < 60s)
Le systeme genere une synthese verbale structuree en trois segments explicites: objet ("De quoi ca parle"), apports majeurs, puis synthese operationnelle et conclusions. Realise UJ-1, UJ-4.

Consequences testables:
- Le volume du script genere reste sous la barre des 140 mots (permettant une elocution sous la minute a vitesse standard).
- [ASSUMPTION: la synthese s'appuie sur une execution LLM locale ou une API rapide selon la configuration active].

#### FR-4: Option Resume a 50 %
Le systeme condense le document source pour en produire une version comprimee de moitie, conservant la logique d'exposition et les elements factuels cruciaux. Realise UJ-2.

Consequences testables:
- Le nombre de mots du resume produit oscille entre 40 % et 60 % du document d'origine.
- La trame des paragraphes principaux reste fidele au deroule initial.

#### FR-5: Option Texte integral
Le systeme envoie la totalite du texte extrait directement au moteur de synthese vocale, sans alteration editoriale. Realise UJ-3.

Consequences testables:
- 100 % des segments textuels valides extraits du document sont presents dans la file de lecture vocale.

### 4.3 Synthese vocale et controle audio

L'application procure un lecteur audio integre permettant de lancer, d'arreter et de regler la cadence d'ecoute.

#### FR-6: Generation de voix agreable et naturelle
Le moteur TTS transforme le texte retenu en un flux audio haute fidelite exempt de voix robotique saccadee. Realise UJ-1, UJ-2, UJ-3, UJ-4.

Consequences testables:
- La voix utilisee prend en charge la prononciation correcte du francais (liaisons courantes, accents, ponctuations expressives).
- Moteur par defaut: Edge-TTS pour une diction fluide et naturelle en francais, avec repli autonome possible.

#### FR-7: Reglage de la vitesse d'elocution
L'utilisateur peut ajuster la vitesse de restitution via un curseur gradue avant ou pendant l'ecoute.

Consequences testables:
- La plage de reglages va de 0.75x a 1.75x par paliers de 0.05x ou 0.1x.
- La modification de la vitesse ne degrade pas la hauteur tonale (conservation du pitch).

#### FR-8: Lecteur et telechargement de l'audio
L'application met a disposition un composant de lecture audio complet et permet a l'utilisateur de telecharger le fichier audio produit (.mp3 ou .wav).

Consequences testables:
- Le composant audio permet la lecture, la pause et le deplacement temporel.
- Un bouton permet d'exporter l'audio sur le disque local.

### 4.4 Integrations systeme Windows et Antigravity

Ces exigences couvrent le declenchement rapide depuis l'OS et l'orchestration par le runtime Antigravity.

#### FR-9: Entree dans le menu contextuel Windows (clic droit)
L'application fournit un script d'installation sans privilege administrateur (registre `HKEY_CURRENT_USER\Software\Classes`) pour ajouter l'option "Ecouter ce document" sur les fichiers `.pdf`, `.docx` et `.txt`. Realise UJ-4.

Consequences testables:
- Un clic droit sur un fichier supporte fait apparaitre l'entree de menu.
- Le declenchement ouvre un mini-lecteur immediat (ou notification avec lecture de la synthese en arriere-plan).
- Un script de desinstallation propre supprime les cles de registre associees sans laisser de trace.

#### FR-10: Execution et pilotage sous Antigravity
L'architecture de l'application s'articule autour d'un point d'entree modulaire en ligne de commande (CLI Python standard), permettant a Antigravity de lancer l'application Streamlit, d'appeler les modules d'extraction ou de lancer l'ecoute directe via ses propres outils.

Consequences testables:
- Le moteur de traitement peut etre appele en CLI autonome: `python -m src.cli --file <path> --mode <condense|50|full> --speed <float>`.
- Le serveur Streamlit peut etre lance et verifie via les commandes standard Antigravity.

## 5. Exigences non-fonctionnelles (NFR)

### 5.1 Ergonomie et accessibilite cognitive (NFR-1)
L'interface doit rester depouillee au maximum: une zone de depot, un choix en 3 boutons clairs, un curseur de vitesse, et le lecteur. Zero element graphique perturbateur ou jargon technique affiche a l'ecran.

### 5.2 Qualite auditive et naturel (NFR-2)
La voix par defaut ne doit comporter aucun gresillement ni cadence mecanique. Le rendu doit etre chaleureux et intelligible, adapte a une ecoute prolongee sans inconfort.

### 5.3 Temps de reponse (NFR-3)
Pour l'option Condense (moins d'une minute d'audio), le delai entre le declenchement (clic interface ou clic droit) et la disponibilite de la premiere seconde d'ecoute ne doit pas exceder 8 secondes sur une machine standard.

### 5.4 Confidentialite et persistance (NFR-4)
Les documents traites ainsi que les fichiers audio generes sont stockes temporairement dans la session active ou dans le dossier cache utilisateur temporaire. Aucune donnee n'est transmise hors des canaux de synthese necessaires.

## 6. Index des hypotheses et points a trancher

- [ASSUMPTION-1]: Le menu contextuel Windows est enregistre dans la ruche utilisateur (`HKCU`) afin de ne pas requerir d'elevation de privileges administrateur lors de l'installation.
- [ASSUMPTION-2]: Le declenchement par clic droit applique par defaut l'option "Condense (1 minute)" avec ouverture d'un mini-lecteur audio flottant ou notification sonore.
- [ASSUMPTION-3]: L'integration Antigravity repose sur un module CLI Python qui sert de pivot commun entre l'application Streamlit, le menu contextuel Windows et le runtime d'agent.
