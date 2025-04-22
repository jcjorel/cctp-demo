# Spécifications IHM - Système de Réservation de Ressources

Ce document décrit les spécifications des interfaces utilisateur pour le Système de Réservation de Ressources (SRR) destiné à la Communauté d'Agglomération Plaine Commune et la Ville de Saint-Denis.

## Table des matières

1. [Introduction](#introduction)
2. [Principes de design](#principes-de-design)
3. [Guide de style](#guide-de-style)
4. [Composants UI communs](#composants-ui-communs)
5. [Structure des écrans](#structure-des-écrans)
6. [Écrans par rôle](#écrans-par-rôle)
7. [Parcours utilisateurs](#parcours-utilisateurs)
8. [Responsive design](#responsive-design)
9. [Accessibilité](#accessibilité)
10. [Approche technique](#approche-technique)

## Introduction

### Objectif des mockups

Ces mockups ont pour objectif de valider en amont les interfaces utilisateur du Système de Réservation de Ressources avant de procéder à leur implémentation complète. Ils permettront au donneur d'ordre d'évaluer à la fois la forme (aspect visuel, ergonomie) et le fond (fonctionnalités, workflows) des interfaces proposées.

### Public cible

Les mockups s'adressent à quatre types d'utilisateurs :
- **Agents demandeurs** (tous profils confondus) : Environ 3500 utilisateurs potentiels
- **Gestionnaires de ressources** : Environ 10 personnes (5 par collectivité)
- **Administrateurs système** : Équipe DSIM (moins de 5 personnes)
- **Agents d'accueil** : Personnel en charge de l'accueil des visiteurs

### Contraintes principales

- Interface entièrement accessible via navigateur web
- Interface intuitive ne nécessitant pas de formation présentielle
- Compatibilité avec les navigateurs standards supportés par les collectivités
- Adaptation possible à des postes plus anciens sous Windows XP

## Principes de design

### Philosophie générale

1. **Simplicité avant tout** : La plupart des utilisateurs n'utiliseront le système que sporadiquement, d'où l'importance capitale de l'ergonomie.
2. **Décentralisation des demandes** : Le système privilégie la saisie directe des demandes par les utilisateurs finaux.
3. **Flexibilité des workflows** : Les circuits de validation sont adaptables selon les types de ressources et les organisations.
4. **Prise de décision informée** : Les outils statistiques permettent d'optimiser l'utilisation des ressources.

### Material Design

Les mockups s'inspirent des principes du Material Design de Google, qui sera implémenté via Material-UI dans la version finale en React. Ces principes incluent :

- Surface élevée et ombres pour créer une hiérarchie visuelle
- Animations et transitions significatives
- Interface basée sur une grille
- Utilisation de la couleur pour attirer l'attention et guider l'utilisateur
- Typographie claire et hiérarchisée

## Guide de style

### Palette de couleurs

#### Couleurs primaires

- **Plaine Commune Rouge/Rose (#D51B5C)** - Couleur principale utilisée pour les actions primaires
- **Vert (#8DAD3E)** - Couleur secondaire utilisée pour les éléments de succès et de validation

#### Couleurs sémantiques

- **Succès (#4CAF50)** : Validations, confirmations
- **Avertissement (#FF9800)** : Alertes, mises en garde
- **Erreur (#F44336)** : Erreurs, refus, suppressions
- **Information (#2196F3)** : Conseils, aide, informations

#### Couleurs neutres

- **Texte principal (#000000)**
- **Texte secondaire (#757575)**
- **Fond principal (#FFFFFF)**
- **Fond secondaire (#F5F5F5)**
- **Bordures (#E0E0E0)**

### Typographie

- **Titres** : Roboto, sans-serif, poids 500 (Medium)
- **Corps du texte** : Roboto, sans-serif, poids 400 (Regular)
- **Taille de police de base** : 16px
- **Échelle typographique** :
  - Titre h1 : 2rem (32px)
  - Titre h2 : 1.5rem (24px)
  - Titre h3 : 1.25rem (20px)
  - Paragraphe : 1rem (16px)
  - Texte secondaire : 0.875rem (14px)

### Espacement

- **Unité de base** : 8px
- **Grille** : Multiples de 8px (8px, 16px, 24px, 32px, 48px, 64px)
- **Padding** : 16px pour les conteneurs principaux, 24px pour les sections importantes
- **Marge entre éléments** : 16px (standard), 8px (compact), 24px (spacieux)

### Ombres

Inspirées de Material Design pour créer un effet de profondeur :
- **Niveau 1** : `0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)`
- **Niveau 2** : `0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23)`
- **Niveau 3** : `0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23)`
- **Niveau 4** : `0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22)`

## Composants UI communs

### Système d'en-tête

```html
<header class="app-header">
  <div class="logo-container">
    <img src="../logos/plaine_commune.svg" alt="Logo Plaine Commune" class="header-logo">
  </div>
  <nav class="main-nav">
    <!-- Navigation principale -->
  </nav>
  <div class="user-controls">
    <!-- Contrôles utilisateur (profil, déconnexion) -->
  </div>
</header>
```

L'en-tête contient :
- Logo de Plaine Commune à gauche (48px de hauteur)
- Navigation principale au centre
- Contrôles utilisateur à droite (nom utilisateur, photo profil, menu déconnexion)

### Système de navigation

```html
<nav class="main-nav">
  <ul class="nav-list">
    <li class="nav-item"><a href="home.html" class="nav-link active">Accueil</a></li>
    <li class="nav-item"><a href="search.html" class="nav-link">Rechercher</a></li>
    <li class="nav-item"><a href="bookings.html" class="nav-link">Mes réservations</a></li>
    <!-- Autres liens selon le profil -->
  </ul>
</nav>
```

La navigation principale change selon le profil de l'utilisateur connecté.

### Pied de page

```html
<footer class="app-footer">
  <div class="footer-logos">
    <!-- Logos des entités en version réduite -->
  </div>
  <div class="footer-links">
    <!-- Liens légaux, contact, etc. -->
  </div>
  <div class="footer-copyright">
    &copy; 2025 Plaine Commune & Ville de Saint-Denis
  </div>
</footer>
```

Le pied de page contient :
- Logos de toutes les entités impliquées (32px de hauteur)
- Liens vers mentions légales, politique de confidentialité, contact
- Mention de copyright

### Boutons

```html
<button class="btn btn-primary">Action principale</button>
<button class="btn btn-secondary">Action secondaire</button>
<button class="btn btn-text">Action texte</button>
<button class="btn btn-icon"><span class="material-icon">edit</span></button>
<button class="btn btn-primary btn-large">Grande action</button>
<button class="btn btn-primary disabled">Action désactivée</button>
```

Types de boutons :
- **Primaire** : Actions principales, fond coloré (#D51B5C)
- **Secondaire** : Actions alternatives, contour coloré
- **Texte** : Actions tertiaires, texte seul
- **Icône** : Actions compactes, icône seule
- **Variantes** : Large, petit, désactivé

### Champs de formulaire

```html
<div class="form-field">
  <label for="field-id" class="form-label">Libellé</label>
  <input type="text" id="field-id" class="form-input" placeholder="Exemple">
  <span class="form-helper">Texte d'aide</span>
</div>
```

Types de champs :
- Texte simple
- Texte multiligne
- Sélection (dropdown)
- Case à cocher
- Boutons radio
- Sélecteur de date
- Sélecteur d'heure
- Upload de fichier

États des champs :
- Par défaut
- Focus
- Rempli
- Erreur
- Désactivé

### Cartes de ressources

```html
<div class="resource-card">
  <div class="resource-image">
    <!-- Image de la ressource -->
  </div>
  <div class="resource-content">
    <h3 class="resource-title">Nom de la ressource</h3>
    <p class="resource-details">Caractéristiques principales</p>
  </div>
  <div class="resource-actions">
    <button class="btn btn-primary">Réserver</button>
  </div>
</div>
```

Les cartes de ressources sont utilisées pour afficher :
- Salles de réunion
- Véhicules
- Équipements

### Tableaux de données

```html
<table class="data-table">
  <thead>
    <tr>
      <th>En-tête 1</th>
      <th>En-tête 2</th>
      <!-- Autres en-têtes -->
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Donnée 1</td>
      <td>Donnée 2</td>
      <!-- Autres données -->
    </tr>
    <!-- Autres lignes -->
  </tbody>
</table>
```

Fonctionnalités des tableaux :
- Tri des colonnes
- Pagination
- Recherche/filtrage
- Actions par ligne

### Notifications

```html
<div class="notification notification-success">
  <span class="notification-icon">✓</span>
  <div class="notification-content">
    <h4 class="notification-title">Titre</h4>
    <p class="notification-message">Message de la notification</p>
  </div>
  <button class="notification-close">&times;</button>
</div>
```

Types de notifications :
- Succès (vert)
- Information (bleu)
- Avertissement (orange)
- Erreur (rouge)

### Modals et dialogues

```html
<div class="modal-overlay">
  <div class="modal-container">
    <div class="modal-header">
      <h3 class="modal-title">Titre du modal</h3>
      <button class="modal-close">&times;</button>
    </div>
    <div class="modal-content">
      <!-- Contenu du modal -->
    </div>
    <div class="modal-actions">
      <button class="btn btn-secondary">Annuler</button>
      <button class="btn btn-primary">Confirmer</button>
    </div>
  </div>
</div>
```

Utilisations des modals :
- Confirmations d'action
- Formulaires courts
- Affichage de détails supplémentaires
- Alertes importantes

## Structure des écrans

### Layout général

```
+-----------------------------------------------+
| HEADER (logo + navigation + user controls)    |
+-----------------------------------------------+
|                                               |
|                                               |
|                                               |
|               CONTENU PRINCIPAL               |
|                                               |
|                                               |
|                                               |
+-----------------------------------------------+
| FOOTER (logos + liens + copyright)            |
+-----------------------------------------------+
```

### Grille de contenu

Le contenu principal utilise une grille responsive avec trois points de rupture :
- **Mobile** : < 768px (1 colonne)
- **Tablette** : 768px - 1024px (8 colonnes)
- **Desktop** : > 1024px (12 colonnes)

## Écrans par rôle

### Communs à tous les utilisateurs

#### Page de connexion

![Page de connexion wireframe](../logos/plaine_commune.svg)

Éléments :
- Logo centré (72px)
- Formulaire de connexion (utilisateur/mot de passe)
- Bouton "Se connecter"
- Mention "Connexion via Active Directory"

#### Page d'accueil

Éléments :
- Barre de recherche principale
- Types de ressources disponibles (cartes clickables)
- Réservations à venir de l'utilisateur
- Notifications importantes

#### Recherche de ressources

Éléments :
- Filtres par type de ressource
- Filtres par date/horaire
- Filtres par caractéristiques
- Liste des résultats (affichage en cartes ou tableau)

#### Détail d'une ressource

Éléments :
- Photos/images de la ressource
- Description complète
- Caractéristiques techniques
- Disponibilité (calendrier)
- Bouton de réservation

#### Formulaire de réservation

Éléments :
- Récapitulatif de la ressource sélectionnée
- Sélection de date et horaires
- Motif de la réservation
- Services associés (si applicable)
- Participants (si applicable)
- Bouton de soumission

### Spécifiques aux gestionnaires

#### Tableau de bord

Éléments :
- Statistiques d'utilisation (graphiques)
- Demandes en attente
- Alertes et notifications
- Actions rapides

#### Liste des demandes

Éléments :
- Tableau des demandes en attente
- Filtres (par ressource, par date, par demandeur)
- Actions en masse
- Statuts des demandes (code couleur)

#### Détail d'une demande

Éléments :
- Informations complètes sur la demande
- Informations sur le demandeur
- Historique des interactions
- Boutons d'action (Approuver/Refuser)
- Champ de commentaire

### Spécifiques aux administrateurs

#### Configuration du système

Éléments :
- Paramètres généraux
- Gestion des types de ressources
- Configuration des workflows
- Paramètres d'email

#### Gestion des ressources

Éléments :
- Liste des ressources
- Ajout/modification/suppression
- Upload de photos
- Définition des caractéristiques

#### Gestion des utilisateurs

Éléments :
- Liste des utilisateurs
- Attribution des rôles
- Gestion des groupes
- Historique d'activité

### Écrans d'affichage public

#### Écran d'information hall

Éléments :
- Liste des réunions du jour
- Localisation des salles
- Horloge et date
- Informations importantes

## Parcours utilisateurs

### Parcours de Marie (Agent demandeur)

1. **Connexion** → Page d'accueil
2. **Recherche d'une salle** → Liste de résultats filtrés
3. **Sélection d'une salle** → Détail de la salle
4. **Réservation** → Formulaire de réservation
5. **Confirmation** → Notification d'attente de validation
6. **Notification par email** → Réservation confirmée

### Parcours de Thomas (Gestionnaire de ressources)

1. **Connexion** → Tableau de bord gestionnaire
2. **Nouvelle demande** → Notification
3. **Liste des demandes** → Visualisation des demandes en attente
4. **Sélection d'une demande** → Détail de la demande
5. **Évaluation** → Validation ou refus avec motif
6. **Statistiques** → Analyse de l'utilisation

### Parcours de Claire (Administratrice système)

1. **Connexion** → Tableau de bord administrateur
2. **Configuration** → Paramètres système
3. **Création de ressource** → Formulaire d'ajout
4. **Modification de workflow** → Configuration du circuit de validation
5. **Consultation des statistiques** → Rapports détaillés

## Responsive design

### Approche générale

Approche "Mobile First" pour garantir une expérience utilisateur optimale sur tous les appareils :

1. **Base mobile** : Conception initiale pour les petits écrans
2. **Adaptations progressives** : Améliorations pour tablettes et desktops
3. **Points de rupture** : 
   - 480px (petits mobiles)
   - 768px (tablettes)
   - 1024px (petits écrans)
   - 1280px (grands écrans)

### Adaptations spécifiques

#### Mobile
- Navigation sous forme de menu hamburger
- Une colonne pour le contenu
- Éléments empilés verticalement
- Boutons pleine largeur
- Tableaux adaptés (colonnes flexibles ou scroll horizontal)

#### Tablette
- Navigation visible horizontalement (items principaux)
- Grille à 8 colonnes
- Disposition mixte (2-4 colonnes selon les éléments)

#### Desktop
- Navigation complète horizontale
- Grille à 12 colonnes
- Contenu organisé en sections horizontales
- Utilisation de l'espace pour afficher plus d'informations

## Accessibilité

### Principes WCAG 2.1 AA

Les mockups respectent les principes d'accessibilité WCAG 2.1 niveau AA :

1. **Perceptible** :
   - Textes alternatifs pour les images
   - Contraste suffisant (minimum 4.5:1)
   - Mise en page adaptable

2. **Utilisable** :
   - Navigation au clavier possible
   - Temps suffisant pour lire et utiliser le contenu
   - Pas de contenu susceptible de provoquer des crises

3. **Compréhensible** :
   - Texte lisible et compréhensible
   - Fonctionnement prévisible
   - Assistance à la saisie

4. **Robuste** :
   - Compatible avec les technologies d'assistance

### Éléments spécifiques

- **Labels explicites** pour tous les champs de formulaire
- **Messages d'erreur** clairs et liés aux champs concernés
- **Focus visible** sur tous les éléments interactifs
- **Structure sémantique** avec utilisation appropriée des balises HTML5
- **Navigation par tabulation** logique et cohérente

## Approche technique

### HTML/CSS pur avec inspiration Material Design

Les mockups sont réalisés en HTML/CSS pur pour permettre une visualisation directe dans un navigateur, mais s'inspirent des principes et composants de Material-UI pour faciliter la transition vers React.

### Structure modulaire

```html
<!-- Exemple de structure modulaire -->
<div class="app-container">
  <!-- Inclusion de l'en-tête modulaire -->
  <div id="header-component"></div>
  
  <!-- Contenu principal -->
  <main class="main-content">
    <!-- Composants de page -->
  </main>
  
  <!-- Inclusion du pied de page modulaire -->
  <div id="footer-component"></div>
</div>
```

### Préfixes CSS pour correspondance Material-UI

Les classes CSS utilisent des préfixes pour indiquer leur correspondance avec Material-UI :

```css
/* Exemple de préfixes CSS */
.mui-btn { /* équivalent de <Button> */ }
.mui-card { /* équivalent de <Card> */ }
.mui-input { /* équivalent de <TextField> */ }
```

### Commentaires de migration

Des commentaires sont ajoutés pour faciliter la transition vers React/Material-UI :

```html
<!-- 
  React/Material-UI équivalent:
  <Button 
    variant="contained" 
    color="primary" 
    startIcon={<SaveIcon />}
    onClick={handleSave}
  >
    Enregistrer
  </Button>
-->
<button class="mui-btn mui-btn-primary mui-btn-with-icon">
  <span class="mui-icon">save</span>
  Enregistrer
</button>
```

---

Ce document servira de référence tout au long du développement des mockups. Il sera régulièrement mis à jour pour refléter les décisions de conception et les ajustements nécessaires.
