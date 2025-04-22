# Règles d'usage des logos dans l'interface utilisateur

Ce document définit les règles d'usage des logos dans l'interface utilisateur du système de réservation de ressources, en respectant les meilleures pratiques UX/UI pour garantir à la fois l'esthétique et l'accessibilité.

## Principes généraux d'utilisation des logos

### Zone de protection

![Zone de protection](./logos/plaine_commune.svg)

- **Règle d'or** : Maintenir une zone de protection autour de chaque logo équivalente à au moins 25% de sa largeur
- **Objectif** : Préserver l'impact visuel du logo et empêcher les interférences avec d'autres éléments graphiques
- **Application** : Aucun texte, image ou élément graphique ne doit empiéter sur cette zone de protection

### Tailles minimales

| Contexte | Taille minimale |
|----------|-----------------|
| En-tête | 48px de hauteur |
| Pied de page | 32px de hauteur |
| Dans le contenu | 24px de hauteur |
| Version mobile | 40px de hauteur |

- **Règle** : Ne jamais réduire les logos en-dessous des tailles minimales spécifiées
- **Raison** : Garantir la lisibilité et la reconnaissance, particulièrement sur les écrans haute densité

### Fonds recommandés et à éviter

#### Fonds recommandés

- **Blanc (#FFFFFF)** : Fond principal recommandé pour tous les logos
- **Gris très clair (#F5F5F5)** : Alternative acceptable pour les interfaces utilisant des tonalités de gris
- **Dégradés subtils** : Acceptables uniquement si le contraste demeure élevé

#### Fonds à éviter

- **Couleurs vives** : Éviter les fonds de couleurs saturées qui créeraient des vibrations visuelles avec les logos
- **Motifs complexes** : Proscrire tout fond avec motif qui nuirait à la lisibilité du logo
- **Fonds de même tonalité** que la couleur principale du logo (risque d'absorption visuelle)

## Placement dans l'interface

### En-tête (Header)

- **Position** : Aligné à gauche, centré verticalement
- **Marge** : 24px depuis le bord gauche sur desktop, 16px sur mobile
- **Comportement responsive** : Maintenir les proportions, réduire la taille mais pas en-dessous du minimum spécifié

```css
.header-logo {
  margin-left: 24px;
  height: 48px;
  width: auto;
  padding: 12px 0;
}

@media (max-width: 768px) {
  .header-logo {
    margin-left: 16px;
    height: 40px;
  }
}
```

### Pied de page (Footer)

- **Position** : Aligné soit à gauche, soit centré selon la conception globale
- **Taille** : Plus petite que dans l'en-tête, mais jamais moins de 32px de hauteur
- **Accompagnement** : Peut être accompagné de liens légaux et de mentions de copyright

### Modal de connexion

- **Position** : Centré en haut de la modal, avec 32px de marge supérieure
- **Taille** : 64px de hauteur recommandée pour renforcer la confiance utilisateur

## Utilisation par contexte

### Application principale

- **En-tête** : Logo de Plaine Commune comme logo principal
- **Pied de page** : Logos de toutes les entités impliquées (taille réduite)

### Module de réservation pour Saint-Denis

- **En-tête** : Logo de Saint-Denis
- **Indication** : Mention "Un service de Plaine Commune" avec logo Plaine Commune de petite taille

### Écrans d'authentification

- **Position** : Logo centré en haut avec taille plus importante (72px)
- **Marge** : 48px de marge supérieure et latérale

## Règles d'accessibilité

### Contraste

- **Règle WCAG** : Maintenir un ratio de contraste d'au moins 4.5:1 entre le logo et le fond
- **Vérification** : Utiliser des outils comme WebAIM pour vérifier le ratio de contraste

### Alternative textuelle

- **Balise alt** : Toujours fournir un texte alternatif descriptif
- **Exemple** : `<img src="logos/plaine_commune.svg" alt="Logo Plaine Commune - Établissement Public Territorial">`

### Animation et interaction

- **Animation** : Éviter toute animation du logo qui pourrait distraire ou provoquer des problèmes d'accessibilité
- **État survol** : Aucune modification visuelle au survol, sauf si le logo est un lien (dans ce cas, curseur pointer)

## Intégration technique

### Format recommandé

- **SVG** : Format privilégié pour sa scalabilité et sa netteté sur tous les écrans
- **Fallback PNG** : Prévoir une version PNG pour les navigateurs anciens (usage très limité aujourd'hui)

### Performance

- **Optimisation** : Utiliser des outils comme SVGOMG pour optimiser le poids des fichiers SVG
- **Chargement** : Ne pas bloquer le rendu avec le chargement des logos (utiliser defer ou async)

```html
<link rel="preload" href="logos/plaine_commune.svg" as="image">
```

### Mise en cache

- **Stratégie** : Mettre en cache les logos avec une longue durée de validité
- **Headers** : Configurer les en-têtes HTTP pour un cache efficace

```
Cache-Control: public, max-age=31536000
```

## Cas particuliers

### Impression

- **Version monochrome** : Prévoir une version monochrome des logos pour l'impression
- **Contraste** : S'assurer que les logos restent visibles à l'impression en noir et blanc

### Mode sombre

- **Inversion** : Dans les interfaces en mode sombre, utiliser des versions inversées des logos avec fond transparent
- **Technique** : Utiliser CSS pour appliquer un filtre d'inversion contrôlé

```css
@media (prefers-color-scheme: dark) {
  .logo {
    filter: brightness(0) invert(1);
  }
}
```

## Matrice d'utilisation des logos par contexte

| Contexte | Logo principal | Logo secondaire | Remarques |
|----------|---------------|-----------------|-----------|
| Page d'accueil | Plaine Commune | - | Taille plus importante (72px) |
| Réservation de salles | Entité concernée | Plaine Commune | Adapter selon l'entité propriétaire de la ressource |
| Tableau de bord | Plaine Commune | - | Version plus petite (48px) |
| Rapports | Plaine Commune + DSIM | - | Positionnés côte à côte avec un séparateur |
| Écrans d'erreur | Plaine Commune | - | Version plus discrète (32px) |

## Bonnes pratiques générales

1. **Cohérence** : Maintenir une utilisation cohérente des logos sur toutes les interfaces
2. **Simplicité** : Éviter la surcharge de logos dans une même vue
3. **Hiérarchie** : Établir une hiérarchie claire quand plusieurs logos sont présents
4. **Qualité** : Toujours utiliser les versions haute qualité des logos
5. **Respect** : Ne jamais déformer, recadrer ou modifier les logos de quelque manière que ce soit
