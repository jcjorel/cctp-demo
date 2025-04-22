# Identité Visuelle de la Direction des Systèmes d'Information Mutualisée (DSIM)

## Présentation de l'entité
La Direction des Systèmes d'Information Mutualisée (DSIM) est une structure créée le 1er janvier 2011, gérant les systèmes d'information de quatre collectivités : Plaine Commune, Saint-Denis, Villetaneuse et L'Île-Saint-Denis. Elle couvre 220 sites et environ 5 500 postes informatiques. La DSIM maintient un fort engagement sur la cybersécurité, ayant notamment participé à l'European Cyber Week en octobre 2024.

## Logo SVG

```svg
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Fond transparent -->
  <rect width="200" height="200" fill="none"/>
  
  <!-- Cercle extérieur -->
  <circle cx="100" cy="100" r="80" fill="#0072CE" stroke="#FFFFFF" stroke-width="2"/>
  
  <!-- Motif réseau stylisé -->
  <circle cx="100" cy="100" r="40" fill="#FFFFFF" opacity="0.2"/>
  <circle cx="100" cy="100" r="20" fill="#FFFFFF" opacity="0.4"/>
  
  <!-- Points de connexion -->
  <circle cx="100" cy="45" r="8" fill="#FFFFFF"/>
  <circle cx="155" cy="100" r="8" fill="#FFFFFF"/>
  <circle cx="100" cy="155" r="8" fill="#FFFFFF"/>
  <circle cx="45" cy="100" r="8" fill="#FFFFFF"/>
  
  <!-- Lignes de connexion -->
  <line x1="100" y1="45" x2="100" y2="80" stroke="#FFFFFF" stroke-width="3"/>
  <line x1="155" y1="100" x2="120" y2="100" stroke="#FFFFFF" stroke-width="3"/>
  <line x1="100" y1="155" x2="100" y2="120" stroke="#FFFFFF" stroke-width="3"/>
  <line x1="45" y1="100" x2="80" y2="100" stroke="#FFFFFF" stroke-width="3"/>
  
  <!-- Symbole de sécurité au centre -->
  <path d="M90,100 L100,110 L115,90" stroke="#FFFFFF" stroke-width="4" fill="none"/>
  
  <!-- Texte "DSIM" -->
  <text x="100" y="175" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#FFFFFF">DSIM</text>
</svg>
```

## Charte graphique

### Couleurs principales
- **Bleu (#0072CE)** - Couleur principale, symbolisant la technologie et la fiabilité
- **Vert (#00A651)** - Couleur secondaire, symbolisant l'innovation et la durabilité
- **Blanc (#FFFFFF)** - Pour le texte et les éléments graphiques sur fond coloré
- **Gris (#565656)** - Pour le texte secondaire et les éléments plus discrets

### Typographie
- Police technique sans-serif pour refléter la nature technologique de l'entité
- Typographie claire et précise pour faciliter la lecture d'informations techniques

### Éléments graphiques distinctifs
- Motifs de réseau et de connexion représentant l'infrastructure informatique
- Symboles de sécurité reflétant l'engagement en cybersécurité
- Design épuré et professionnel en accord avec les standards du secteur informatique

## Vision stratégique
La DSIM porte une vision stratégique claire en matière de transformation numérique du territoire, articulée autour de quatre piliers fondamentaux :

1. **Innovation technologique au service du développement local** - Pilotage de plus de 30 projets annuels visant à enrichir le patrimoine applicatif des collectivités

2. **Sécurisation renforcée des infrastructures numériques** - Une priorité absolue, particulièrement dans un contexte où le territoire accueille régulièrement des événements internationaux

3. **Accompagnement continu des services** - Rôle de conseil et d'expertise auprès des différents services pour optimiser leurs processus via le numérique

4. **Gouvernance mutualisée** - Modèle qui optimise les ressources et les compétences entre les collectivités partenaires

## Infrastructures gérées

### Réseau Plaine Commune
- Réseau local avec deux cœurs de réseau HP 7500
- Architecture redondante avec implémentation du "Spanning tree"
- Infrastructure de production entièrement virtualisée sous Vsphere 4.1
- Environ 100 serveurs principalement sous Windows
- 9 serveurs ESX gérés par l'hyperviseur VMware
- Environnement virtuel basé sur un châssis DELL Blade M1000e avec lames M610 et SAN Compellent

### Serveurs et Messageries
- **Plaine Commune** : Serveurs AD 2008 R2, Exchange 2007
- **Saint-Denis** : Serveurs AD 2003/2003 R2, migration de Lotus Notes 6.5.4 vers Exchange prévue
