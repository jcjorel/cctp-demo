# Mockups du Système de Réservation de Ressources (SRR)

## Introduction

Ce répertoire contient tous les mockups HTML/CSS du Système de Réservation de Ressources pour la Communauté d'Agglomération Plaine Commune et la Ville de Saint-Denis. Ces mockups sont destinés à valider les interfaces utilisateur avant l'implémentation complète en React.js avec Material-UI.

## Organisation du répertoire

- **[index.html](./index.html)** - Point d'entrée pour visualiser tous les mockups
- **[IHM_MOCKUPS.md](./IHM_MOCKUPS.md)** - Spécifications détaillées de l'interface utilisateur
- **[MOCKUPS_PROGRESS.md](./MOCKUPS_PROGRESS.md)** - Suivi d'avancement détaillé et plan d'implémentation
- **[assets/](./assets/)** - Ressources CSS et JavaScript partagées
- **[components/](./components/)** - Composants UI réutilisables
- **[screens/](./screens/)** - Écrans organisés par profil utilisateur
- **[flows/](./flows/)** - Documentation des parcours utilisateurs

## Démarrage rapide

Pour visualiser les mockups :

1. Ouvrez `index.html` dans un navigateur web
2. Naviguez à travers les différents écrans via l'interface

## Identités visuelles appliquées

Les mockups respectent les identités visuelles des entités suivantes :

- Plaine Commune (EPT) - Couleurs principales : #D51B5C (Rouge/Rose) et #8DAD3E (Vert)
- Ville de Saint-Denis
- Direction des Systèmes d'Information Mutualisée (DSIM)

## Principes de design appliqués

- **Simplicité d'utilisation** - Interface intuitive ne nécessitant pas de formation
- **Material Design** - Utilisation des principes de Material Design pour faciliter la transition vers React/Material-UI
- **Responsive Design** - Approche "Mobile First" avec points de rupture à 480px, 768px, 1024px et 1280px
- **Accessibilité** - Conformité WCAG 2.1 niveau AA

## Structure des fichiers de style

Les styles sont organisés comme suit :

- **styles.css** - Feuille de style principale avec :
  - Variables CSS personnalisées (couleurs, espacements, typographie)
  - Styles de base et réinitialisation
  - Composants UI (boutons, formulaires, cartes, tableaux)
  - Utilitaires CSS
  - Media queries pour la responsivité

## Prochaines étapes de développement

Voir [MOCKUPS_PROGRESS.md](./MOCKUPS_PROGRESS.md) pour un suivi détaillé de l'avancement et les prochaines étapes à implémenter.

## Sources de documentation

- Identités visuelles : `/doc/identites_visuelles/`
- Logos : `/doc/logos/`
- Règles UX/UI : `/doc/UX_DESIGN.md`
- Vision produit : `/doc/PR-FAQ.md`, `/doc/WORKING_BACKWARDS.md`
