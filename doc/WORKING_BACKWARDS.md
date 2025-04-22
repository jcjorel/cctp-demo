# Working Backwards - Système de Réservation de Ressources (SRR)

## Vision du Produit

Le Système de Réservation de Ressources (SRR) est conçu pour transformer fondamentalement la façon dont les agents de la Communauté d'Agglomération Plaine Commune et de la Ville de Saint-Denis réservent, gèrent et utilisent les ressources partagées. Notre vision est de créer une expérience utilisateur fluide et intuitive qui permet à n'importe quel agent, quelle que soit sa familiarité avec les outils numériques, de trouver et réserver rapidement la ressource la plus adaptée à ses besoins.

Ce système élimine les silos organisationnels en proposant une plateforme unifiée pour la gestion de toutes les ressources partagées, qu'il s'agisse de salles de réunion, de véhicules, ou d'équipements. Il remplace les systèmes obsolètes et fragmentés par une solution moderne, évolutive et accessible entièrement via navigateur web.

En cinq ans, nous envisageons que le SRR devienne l'épine dorsale de la gestion des ressources pour l'ensemble des collectivités du territoire, évoluant au-delà des besoins initiaux pour intégrer de nouveaux types de ressources et de nouvelles fonctionnalités qui répondent aux défis émergents de nos organisations.

## Problèmes Résolus

Le SRR résout les problèmes critiques suivants :

1. **Fragmentation des systèmes** : Les deux collectivités utilisent actuellement des systèmes différents et incompatibles pour la réservation de salles uniquement.

2. **Obsolescence technique** : Le système de la Ville de Saint-Denis deviendra inopérant avec la migration vers Exchange/Outlook, tandis que celui de Plaine Commune est un développement spécifique sans maintenance ni support.

3. **Limitation fonctionnelle** : Aucun système actuel ne gère les ressources autres que les salles de réunion (véhicules, équipements informatiques, etc.).

4. **Inefficacité de la gestion** : Absence d'outils statistiques pour analyser et optimiser l'utilisation des ressources.

5. **Mauvaise expérience utilisateur** : Les systèmes actuels ne sont pas intuitifs et nécessitent une formation pour être utilisés efficacement.

6. **Absence de traçabilité** : Manque de suivi systématique des réservations et des utilisations effectives des ressources.

## Parcours Utilisateur

### 1. Agent demandeur de ressource : Marie, chargée de projet

> Marie doit organiser une réunion avec des partenaires externes pour présenter l'avancement de son projet. Elle a besoin d'une salle adaptée et d'un vidéoprojecteur.

Marie se connecte au SRR via son navigateur web en utilisant ses identifiants habituels (authentification AD). Sur la page d'accueil, elle utilise les filtres pour rechercher une salle disponible pour la date souhaitée, avec une capacité de 15 personnes et équipée d'un vidéoprojecteur.

Le système affiche les options disponibles avec des photos, la capacité exacte et les équipements de chaque salle. Marie sélectionne une salle qui lui convient, indique l'objet de sa réunion, les horaires précis et les éventuels services associés (café, configuration spécifique).

Comme cette salle nécessite une validation, Marie reçoit un email confirmant que sa demande a été transmise au gestionnaire concerné. Deux heures plus tard, elle reçoit une notification lui indiquant que sa réservation est confirmée.

Le jour J, les visiteurs sont accueillis dans le hall où un écran d'information indique la salle de réunion et l'horaire.

### 2. Gestionnaire de ressource : Thomas, responsable du parc automobile

> Thomas est chargé de gérer la flotte de véhicules de service. Il doit s'assurer que les véhicules sont utilisés de façon équitable et pour des missions justifiées.

Thomas se connecte au SRR avec son profil de gestionnaire. Sur son tableau de bord personnalisé, il voit immédiatement les demandes de réservation de véhicules en attente de validation.

Pour chaque demande, il peut consulter toutes les informations pertinentes : identité du demandeur, motif du déplacement, destination, durée prévue, type de véhicule demandé. Il évalue chaque demande et peut soit valider, soit refuser avec un motif, soit proposer un véhicule alternatif plus adapté.

Régulièrement, Thomas consulte les statistiques d'utilisation de la flotte : taux d'utilisation par véhicule, kilométrages parcourus, créneaux de forte demande. Ces données l'aident à planifier la maintenance des véhicules et à justifier les éventuels besoins d'extension du parc automobile.

### 3. Administrateur système : Claire, référente applicative à la DSIM

> Claire est responsable de l'administration du SRR au sein de la DSIM. Elle doit configurer le système pour répondre aux besoins spécifiques des services.

Claire se connecte au système avec ses droits d'administrateur. Elle peut créer de nouveaux types de ressources selon les besoins identifiés (comme récemment, des tablettes tactiles pour les agents de terrain).

Elle paramètre pour chaque type de ressource les champs d'information nécessaires, les workflows de validation, les groupes de gestionnaires et les règles d'utilisation. Claire peut également extraire des rapports détaillés sur l'utilisation de l'ensemble du système pour le bilan annuel de la DSIM.

Lorsqu'un nouveau service intègre le système, Claire configure les droits d'accès pour les nouveaux utilisateurs et organise une courte session de formation pour les gestionnaires.

## Principes Directeurs

1. **Priorité à l'expérience utilisateur** : L'interface doit être suffisamment intuitive pour être utilisable sans formation. La plupart des utilisateurs n'utiliseront le système que sporadiquement, d'où l'importance capitale de l'ergonomie.

2. **Décentralisation des demandes** : Le système privilégie la saisie directe des demandes par les utilisateurs finaux plutôt qu'une centralisation des demandes qui créerait des goulots d'étranglement.

3. **Flexibilité des workflows** : Les circuits de validation doivent être configurables selon les types de ressources et les organisations, permettant d'adapter le système aux pratiques de chaque service.

4. **Évolutivité par design** : Le système est conçu pour intégrer facilement de nouveaux types de ressources non identifiés lors du lancement, sans nécessiter de développements lourds.

5. **Prise de décision informée** : Les outils statistiques permettent aux gestionnaires d'optimiser l'utilisation des ressources en se basant sur des données réelles d'utilisation.

6. **Intégration native** : Le système s'intègre de manière transparente avec les infrastructures existantes (Active Directory, Exchange) et les intranets des collectivités.

## Métriques de Succès

### Métriques d'adoption
- 80% des agents ciblés utilisent activement le système dans les 6 mois suivant le déploiement
- Réduction de 90% des demandes de réservation par email ou téléphone au profit du système

### Métriques d'utilisation
- Taux d'utilisation effective des ressources (comparaison entre réservations et utilisations réelles)
- Temps moyen entre la demande et la validation des réservations inférieur à 4 heures ouvrées

### Métriques techniques
- Disponibilité du système supérieure à 97%
- Temps de réponse moyen inférieur à 2 secondes pour le chargement des pages

### Métriques de satisfaction
- Score de satisfaction utilisateur supérieur à 4/5 lors des enquêtes trimestrielles
- Nombre de tickets d'assistance liés à la complexité d'utilisation en diminution constante

### Métriques d'optimisation
- Réduction des ressources sous-utilisées de 25% grâce à une meilleure allocation
- Diminution des conflits de réservation de 80% par rapport à la situation avant déploiement

## Contraintes et Limites

1. **Utilisateurs internes uniquement** : Le système n'est pas conçu pour les réservations destinées à la population, mais uniquement pour l'usage interne des agents des collectivités.

2. **Compatibilité navigateurs** : L'interface web doit fonctionner sur les navigateurs standards supportés par les collectivités, y compris sur des postes plus anciens sous Windows XP.

3. **Périmètre fonctionnel initial** : La première phase se concentre sur la gestion des salles de réunion avant d'étendre progressivement à d'autres types de ressources.

4. **Sécurité des données** : Les informations traitées sont sensibles (localisation des agents, planning des réunions stratégiques) et nécessitent un niveau de sécurité approprié.

5. **Dépendance à l'infrastructure réseau** : La disponibilité du système dépend de la qualité de la connexion réseau des sites concernés.

6. **Réversibilité obligatoire** : Le système doit permettre une extraction complète des données dans un format exploitable par d'autres solutions en cas de changement de prestataire.

## Conclusion

Le Système de Réservation de Ressources représente un élément clé de la transformation numérique des collectivités du groupement. En remplaçant des solutions obsolètes par une plateforme moderne et unifiée, nous simplifions le quotidien des agents tout en optimisant l'utilisation des ressources publiques.

Ce projet s'inscrit dans la vision plus large de modernisation portée par Mathieu Hanotin et la DSIM, avec une ambition d'étendre progressivement les fonctionnalités et le périmètre du système pour répondre aux besoins futurs des services publics locaux. À terme, le SRR pourrait devenir un standard pour d'autres collectivités territoriales confrontées aux mêmes défis de gestion des ressources.

```mermaid
flowchart TD
    A[Utilisateur se connecte au SRR] --> B{Type de ressource?}
    B -->|Ressource libre| C[Réservation directe]
    B -->|Ressource soumise à validation| D[Demande de réservation]
    C --> E[Confirmation immédiate]
    D --> F[Notification au gestionnaire]
    F --> G{Décision du gestionnaire}
    G -->|Approuvée| H[Notification de confirmation]
    G -->|Refusée| I[Notification de refus avec motif]
    E --> J[Utilisation de la ressource]
    H --> J
    J --> K[Statistiques d'utilisation]
    K --> L[Optimisation des ressources]
