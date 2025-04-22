# Contexte Business du CCTP - Système de Réservation de Ressources

## Introduction

Ce document présente le contexte business du Cahier des Clauses Techniques Particulières (CCTP) relatif à l'acquisition, la mise en œuvre et la maintenance d'un logiciel de réservation de salles et diverses ressources pour la communauté d'agglomération Plaine Commune et la ville de Saint-Denis. Il s'agit d'un marché à procédure adaptée en application de l'article 28 du Code des Marchés Publics.

## Les Acteurs Principaux

### Plaine Commune

**Structure et gouvernance** :
- **Type d'organisation** : Établissement Public Territorial (EPT)
- **Composition** : Regroupe 9 communes de Seine-Saint-Denis
- **Président** : Mathieu Hanotin (également maire de Saint-Denis)
- **Nombre d'agents** : Environ 1500 utilisateurs potentiels de l'outil (3000 au total dans l'Active Directory)

### Ville de Saint-Denis

**Structure et gouvernance** :
- **Maire actuel** : Mathieu Hanotin (depuis 2020)
- **Évolution récente** : Création d'une commune nouvelle avec Pierrefitte-sur-Seine (effective depuis le 1er janvier 2025)
- **Nombre d'agents** : Environ 3000 agents (200 utilisateurs actuels du système de réservation de salles)
- **Projet majeur récent** : Fusion municipale avec Pierrefitte-sur-Seine, décidée en avril 2023 et officialisée en juin 2024

## Direction des Systèmes d'Information Mutualisée (DSIM)

**Caractéristiques** :
- **Création** : Mutualisée depuis le 1er janvier 2011
- **Périmètre** : Gère les systèmes d'information de quatre collectivités (Plaine Commune, Saint-Denis, Villetaneuse et L'Île-Saint-Denis)
- **Infrastructure** : Couvre 220 sites et environ 5 500 postes
- **Priorité récente** : Maintien d'un fort engagement sur la cybersécurité
- **Événement notable** : Participation à l'European Cyber Week en octobre 2024

## Contexte Technique et Organisationnel

### Situation Actuelle

**Plaine Commune** :
- Utilise un système de réservation de salles issu d'un développement spécifique
- Sans maintenance ni support
- Utilisé par 330 agents
- Évolution difficile car maintenance non assurée

**Ville de Saint-Denis** :
- Utilise un système de réservation de salles développé sur plateforme Lotus/Domino
- Utilisé par 200 agents
- Devient inopérant avec la migration prévue vers Outlook/Exchange

**Point commun** : Aucune des deux organisations ne possède de système de réservation pour des ressources autres que des salles.

### Infrastructure Technique

**Réseau Plaine Commune** :
- Réseau local avec deux cœurs de réseau HP 7500
- Architecture redondante avec implémentation du "Spanning tree"
- Infrastructure de production entièrement virtualisée sous Vsphere 4.1
- Environ 100 serveurs principalement sous Windows
- 9 serveurs ESX gérés par l'hyperviseur VMware
- Environnement virtuel basé sur un châssis DELL Blade M1000e avec lames M610 et SAN Compellent

**Serveurs et Messageries** :
- **Plaine Commune** : Serveurs AD 2008 R2, Exchange 2007
- **Saint-Denis** : Serveurs AD 2003/2003 R2, migration de Lotus Notes 6.5.4 vers Exchange prévue

## Chiffres Clés du Projet

### Volumétrie des Ressources à Gérer

**Salles de réunion** :
- Plaine Commune : 25 salles sur 3 sites
- Ville de Saint-Denis : 25 salles sur 4 sites

**Autres types de ressources (Total pour les deux organismes)** :
- 60 voitures
- 10 bicyclettes
- 10 ordinateurs
- 10 téléphones portables
- 10 clés 3G
- 6 vidéoprojecteurs

### Utilisateurs

**Plaine Commune** :
- 3000 utilisateurs potentiels (tout l'Active Directory)
- 330 utilisateurs effectifs actuels
- 5 gestionnaires différents

**Ville de Saint-Denis** :
- 200 utilisateurs effectifs
- 5 gestionnaires différents

## Contexte de Transformation Numérique

Le projet de système de réservation de ressources s'inscrit dans une démarche plus large de transformation numérique des deux collectivités. Cette modernisation est marquée par plusieurs évolutions significatives :

1. **Migration des systèmes de messagerie** : Passage de Lotus Notes à Exchange/Outlook pour Saint-Denis, imposant le remplacement du système de réservation actuel

2. **Mutualisation des services informatiques** : Création d'une DSI commune pour optimiser la gestion des ressources et harmoniser les pratiques

3. **Volonté d'harmonisation des outils** : Recherche d'une solution unique et commune pour faciliter la gestion et réduire les coûts de maintenance

4. **Développement territorial** : En parallèle de ces évolutions informatiques, Plaine Commune Développement pilote d'importants projets urbains avec 1,4 milliard d'euros d'investissements et 3,2 millions de m² de programmes immobiliers

5. **Réorganisation administrative** : La fusion récente entre Saint-Denis et Pierrefitte-sur-Seine implique une rationalisation des services publics, incluant potentiellement des initiatives numériques pour harmoniser les administrations

## Enjeux et Objectifs du Projet

### Objectifs Principaux

1. **Pour les utilisateurs** : Disposer d'un outil ergonomique permettant de :
   - Réserver facilement des ressources
   - Visualiser leur disponibilité
   - Accéder aux informations pertinentes pour faire les bons choix

2. **Pour les gestionnaires de ressources** : Obtenir un outil permettant de :
   - Optimiser l'utilisation des ressources
   - S'assurer que leur affectation respecte les règles établies
   - Disposer d'outils statistiques pour ajuster l'offre de ressources

3. **Pour les organisations** : Acquérir une solution :
   - Entièrement accessible via navigateur web
   - Proposant une interface ergonomique et intuitive
   - Capable de gérer divers types de ressources fixes et mobiles
   - Communicant sur les événements liés aux réservations
   - Utilisant des circuits de validation prédéfinis pour les réservations

### Contraintes et Exigences

- Interface web intuitive ne nécessitant pas de formation présentielle
- Interfaçage avec les Active Directory des deux organismes
- Compatibilité avec les environnements Exchange
- Hautes exigences de disponibilité (97% minimum)
- Garanties de réversibilité des données

## Positions et Visions sur la Transformation Numérique

### Mathieu Hanotin, Maire de Saint-Denis et Président de Plaine Commune

La vision de Mathieu Hanotin concernant la transformation numérique s'exprime notamment à travers le développement d'un Centre de Supervision Urbaine (CSU) innovant, inauguré en juillet 2024 à Saint-Denis. Ce projet illustre une approche "smart city" intégrée :

> "Nous voulons doter le CSU de Saint-Denis de vidéosurveillance algorithmique." - Mathieu Hanotin

Cette déclaration, rapportée par Smart City Mag, montre l'ambition du maire d'intégrer des technologies avancées dans la gestion urbaine. Le Centre de Supervision Urbaine ne se limite pas à la sécurité mais s'inscrit dans une vision plus large de ville intelligente, puisqu'il inclut également :
- Un centre de crise capable de recevoir diverses informations urbaines
- Le pilotage unifié des feux tricolores et autres dispositifs électriques en cas d'incidents
- Une capacité d'évolution pour gérer jusqu'à 500 caméras

### Direction des Systèmes d'Information Mutualisée (DSIM)

La DSIM, bien que ses dirigeants ne soient pas cités directement dans les sources disponibles, porte une vision stratégique claire en matière de transformation numérique du territoire. Cette vision s'articule autour de quatre piliers fondamentaux :

1. **Innovation technologique au service du développement local** : La DSIM pilote plus de 30 projets annuels visant à enrichir le patrimoine applicatif des collectivités.

2. **Sécurisation renforcée des infrastructures numériques** : Une priorité absolue, particulièrement dans un contexte où le territoire accueille régulièrement des événements internationaux.

3. **Accompagnement continu des services** : La DSIM joue un rôle de conseil et d'expertise auprès des différents services pour optimiser leurs processus via le numérique.

4. **Gouvernance mutualisée** : Un modèle qui optimise les ressources et les compétences entre les collectivités partenaires.

Cette stratégie numérique vise à améliorer tant l'efficacité administrative locale que l'expérience utilisateur au sein du territoire Plaine Commune.

## Conclusion

Le projet de système de réservation de ressources représente un élément stratégique dans la modernisation des outils de travail des deux collectivités. Il s'inscrit dans un contexte de transformation numérique plus large, incluant une mutualisation des services informatiques et une harmonisation des pratiques. La réussite de ce projet contribuera à l'optimisation de la gestion des ressources publiques et à l'amélioration de l'expérience utilisateur pour les agents des deux collectivités.
