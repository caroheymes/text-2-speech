---
name: text2speech-design
description: Systeme de design visuel accessible dedie a la synthese vocale et au confort de lecture.
colors:
  background: '#F8FAFC'
  surface: '#FFFFFF'
  surface-muted: '#F1F5F9'
  border-subtle: '#E2E8F0'
  border-focus: '#2563EB'
  text-primary: '#0F172A'
  text-secondary: '#475569'
  text-muted: '#64748B'
  primary-base: '#2563EB'
  primary-hover: '#1D4ED8'
  primary-active: '#1E40AF'
  primary-subtle: '#EFF6FF'
  success-base: '#16A34A'
  success-subtle: '#F0FDF4'
  warning-base: '#D97706'
  error-base: '#DC2626'
typography:
  font-family:
    base: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    heading: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    mono: "Consolas, 'Courier New', monospace"
  title-lg:
    fontSize: '2.25rem'
    fontWeight: '700'
    lineHeight: '1.25'
    letterSpacing: '-0.02em'
  title-md:
    fontSize: '1.5rem'
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: '-0.01em'
  body-base:
    fontSize: '1.05rem'
    fontWeight: '400'
    lineHeight: '1.65'
    letterSpacing: '0.01em'
  body-lead:
    fontSize: '1.15rem'
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: '0'
  label-strong:
    fontSize: '0.95rem'
    fontWeight: '600'
    lineHeight: '1.4'
    letterSpacing: '0.01em'
  caption:
    fontSize: '0.85rem'
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: '0'
rounded:
  sm: '4px'
  md: '8px'
  lg: '12px'
  full: '9999px'
spacing:
  xs: '4px'
  sm: '8px'
  md: '16px'
  lg: '24px'
  xl: '32px'
  container-max: '780px'
components:
  card:
    background: '{colors.surface}'
    border: '1px solid {colors.border-subtle}'
    borderRadius: '{rounded.md}'
    padding: '{spacing.lg}'
  button-primary:
    background: '{colors.primary-base}'
    color: '#FFFFFF'
    borderRadius: '{rounded.md}'
    minHeight: '48px'
    fontWeight: '{typography.label-strong.fontWeight}'
  player-container:
    background: '{colors.surface}'
    border: '1px solid {colors.border-subtle}'
    borderRadius: '{rounded.lg}'
    padding: '{spacing.md}'
  speed-chip:
    background: '{colors.surface}'
    border: '1px solid {colors.border-subtle}'
    borderRadius: '{rounded.sm}'
    minHeight: '36px'
    padding: '{spacing.xs} {spacing.sm}'
---

# Design: Lecteur vocal accessible

## 1. Brand & Style

Ce systeme de conception repond a un objectif d'apaisement et d'accessibilite pour les utilisateurs eprouvant des difficultes de dechiffrage ou de concentration visuelle. L'esthetique refuse tout artefact decoratif distrayant, gradient agressif ou animation superflue.

La tonalite visuelle s'inspire du design editorial sobre: fonds clairs chaleureux evitant l'eblouissement du blanc pur, typographie ouverte a fort contraste noir sur fond clair, et une couleur d'accent unique (bleu franc `{colors.primary-base}`) chargee de focaliser l'attention sur les actions d'ecoute.

## 2. Colors

La palette garantit une conformite stricte avec le niveau AAA du standard d'accessibilite WCAG pour les textes fondamentaux:

- `{colors.background}` (`#F8FAFC`): fond general ardoise tres clair. Il reduit la fatigue retinienne par rapport a un blanc pur `#FFFFFF`.
- `{colors.surface}` (`#FFFFFF`): conteneurs des zones actives (zone de depot, choix du mode, lecteur).
- `{colors.text-primary}` (`#0F172A`): contraste de 14.5:1 sur fond blanc, assurant un confort de lecture optimal meme en cas de vision affaiblie.
- `{colors.text-secondary}` (`#475569`): reserve aux libelles secondaires et indications d'aide.
- `{colors.primary-base}` (`#2563EB`): identifiant visuel de l'interaction sonore (boutons d'action, curseur d'ecoute, barre de progression).
- `{colors.border-subtle}` (`#E2E8F0`): delimite clairement les zones cliquables sans alourdir la page.

## 3. Typography

Les personnes dyslexiques ou fatiguees visuellement ont besoin de glyphes largement ouverts et de lignes aerées:

- Famille: polices sans empattement humanistes du systeme d'exploitation (Segoe UI sous Windows, San Francisco sous macOS) privilegiant des hauteurs d'x genereuses et des formes reconnaissables.
- Cadence de texte: hauteur de ligne fixee a 1.65 `{typography.body-base.lineHeight}` avec un micro-espacement `{typography.body-base.letterSpacing}` de 0.01em pour eviter que les caracteres ne se chevauchent lors du survol.
- Hierarchie: au maximum trois niveaux visuels a l'ecran (titre d'entete `{typography.title-lg}`, section de choix `{typography.title-md}`, et libelles de commande `{typography.label-strong}`).

## 4. Layout & Spacing

L'architecture spatiale s'ordonne en colonne unique strictement centree sur un conteneur etroit `{spacing.container-max}` de 780 pixels:

Cette largeur limite les mouvements occulaires horizontaux balistiques qui provoquent la perte de ligne chez les lecteurs en difficulte.

Les zones de contact (boutons de vitesse, boutons d'option, selecteurs) respectent une hauteur minimale de 44 pixels a 48 pixels pour faciliter le ciblage a la souris comme au toucher.

## 5. Elevation & Depth

L'application privilegie la distinction par la bordure et le contraste plutot que par les ombres portees lourdes:

- Elevation zero: le fond et les cartes reposent a plat, delimites par `{colors.border-subtle}`.
- Focalisation de focus: tout element recevant le focus clavier ou la selection active recoit un contour net de 2 pixels `{colors.border-focus}`.

## 6. Shapes

Les rayons de courbure sont contenus et stables:

- `{rounded.sm}` (4px) pour les boutons de controle de vitesse fins.
- `{rounded.md}` (8px) pour les cartes fonctionnelles et les boutons principaux.
- `{rounded.lg}` (12px) pour le bloc lecteur audio unifie.

## 7. Components

### Zone de depot documentaire (Dropzone)
Surface en blanc `{colors.surface}` avec bordure d'ancrage visible. L'etat survole passe en surbrillance `{colors.primary-subtle}` avec bordure bleue `{colors.primary-base}`. Affichage d'un badge vert de succes `{colors.success-base}` des que le fichier est valide.

### Selecteur d'option de restitution (Options Cards)
Trois cartes radio mutuellement exclusives. La selection active colore la bordure en bleu profond et met le libelle en graisse `{typography.label-strong.fontWeight}`.

### Bloc lecteur audio interactif
Composant composite comprenant le lecteur HTML5 natif, les boutons d'acces rapide a la vitesse (0.85x, 1.0x, 1.2x, 1.5x) et la reglette fine de cadence. Les boutons actifs s'allument sur fond `{colors.primary-subtle}` avec texte bleu.

### Mini-lecteur contextuel Windows
Fenetre native compacte (380x190px) toujours au premier plan, titre du document tronque proprement a 40 caracteres, avec 3 boutons tactiles larges: Pause/Reprendre (primaire), Recommencer (neutre), Fermer (discret).

## 8. Do's and Don'ts

### A faire
- Conserver en permanence un ratio de contraste d'au moins 7:1 sur les textes critiques.
- Indiquer explicitement la vitesse d'elocution active en chiffres clairs (`1.00x`, `1.25x`).
- Permettre a l'utilisateur de fermer ou suspendre l'audio a tout moment d'une simple touche.

### A bannir
- Ne jamais employer de textes gris clairs sur fond blanc (rejet du contraste inferieur a 4.5:1).
- Ne jamais cacher les commandes audios dans des menus deroulants imbriques.
- Ne pas depasser 80 caracteres par ligne de texte pour la transcription.
