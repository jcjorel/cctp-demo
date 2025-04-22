# Cahier des Clauses Techniques Particulières

**Direction des Systèmes d'Information mutualisée - Groupement de commande**

## Groupement de commandes pour l'acquisition, la mise en œuvre et la maintenance d'un logiciel de réservation de salles et diverses ressources pour la communauté d'agglomération Plaine Commune et la ville de Saint-Denis

**PROCÉDURE DE CONSULTATION :**
MARCHÉ À PROCÉDURE ADAPTÉE EN APPLICATION DES ARTICLES 28 DU CODE DES MARCHÉS PUBLICS

**Système de réservation de ressources**

## 1. Le projet

### 1.1. Préambule

Ce document décrit les fournitures et prestations attendues dans le cadre de ce marché. Il est complété par deux autres documents :
- Un "Bordereau des prix unitaires (BPU)" servant également de "Devis quantitatif estimatif (DQE)" pour détailler l'offre économique
- Un "Cadre de Réponse Technique et Fonctionnelle" (CRTF) à remplir pour faciliter l'analyse des offres

Le groupement de commande réunit :
- La communauté d'agglomération Plaine Commune
- La Ville de Saint-Denis

Dans ce document, les termes "le groupement" ou "les membres du groupement" désignent ces deux entités. La ville de Saint-Denis est le coordinateur du groupement de commande. La DSIM fait référence à la Direction des Systèmes d'Information Mutualisée, et l'abréviation SRR signifie système de réservation de ressources. Le terme SAAS désigne le mode d'hébergement externalisé où les logiciels sont installés sur des serveurs distants sous la responsabilité complète du titulaire.

### 1.2. Contexte

La communauté d'agglomération Plaine Commune, la ville de Saint-Denis et la ville de Villetaneuse ont mutualisé leurs directions des systèmes d'information depuis le 1er janvier 2011. Dans ce cadre, ces partenaires constituent des groupements de commandes pour certains projets informatiques répondant à des besoins communs.

La ville de Saint Denis utilise actuellement un système de réservation de salles développé sur plateforme Lotus/Domino utilisé par 200 agents. Ce système deviendra inopérant avec le passage prévu à Outlook/Exchange, d'où la nécessité d'une nouvelle solution.

La communauté d'agglomération Plaine Commune emploie un système de réservation de salles issu d'un développement spécifique sans maintenance ni support, utilisé par 330 agents. Son évolution est difficile et sa maintenance n'est plus assurée.

Aucune des deux organisations ne possède de système de réservation pour des ressources autres que des salles.

Les deux collectivités souhaitent acquérir un outil unique permettant à leurs agents de réserver des ressources avec une interface affichant disponibilités et informations pertinentes pour faire les meilleurs choix selon leurs besoins. Le projet exclut les réservations destinées à la population. L'outil devra permettre aux gestionnaires d'optimiser l'utilisation des ressources et de s'assurer que leur affectation respecte les règles établies, tout en fournissant des outils statistiques pour ajuster l'offre de ressources.

### 1.3. Recommandations

Les candidats doivent répondre clairement et dans l'ordre à toutes les demandes du CCTP et aux questions du CRTF. Les réponses du CRTF prévaudront sur le mémoire technique.

Les candidats sont informés que leurs offres seront considérées comme établies en pleine connaissance du CCTP, quels que soient les renseignements techniques fournis.

Le groupement privilégie la saisie directe des demandes par les utilisateurs plutôt qu'un système centralisé. Pour faciliter la gestion, une tarification par "site" ou "fonctionnalité" est préférée à une tarification par utilisateur.

### 1.4. Objet du Marché

Ce marché vise à doter les deux membres du groupement d'une solution de réservation de ressources qui devra :
- Être entièrement accessible via navigateur web
- Proposer une interface ergonomique et intuitive, utilisable sans formation présentielle
- Gérer divers types de ressources fixes et mobiles (au minimum salles de réunion, salles événementielles, voitures, bicyclettes et ordinateurs portables)
- Communiquer sur les événements liés aux réservations (confirmation, annulation...)
- Utiliser des circuits de validation prédéfinis pour les réservations

### 1.5. Durée du marché

Le marché sera valide de sa date de notification jusqu'à la fin de la période de garantie, avec possibilité de renouvellement trois fois pour des périodes d'un an. La période de garantie sera d'un an après la réception de la VSR (vérification de service régulier).

Pour une solution avec achat de licence, les renouvellements concerneront la maintenance. Pour une solution SAAS, les renouvellements porteront sur le droit d'usage du logiciel, maintenance incluse.

### 1.6. Personnes en charge du marché

Service responsable de la procédure et des renseignements prévus au Code des Marchés Publics :
- Direction de la commande publique de la Ville de Saint-Denis
- Madame Amina Merhoum
- Téléphone : 01 49 33 66 84
- Courriel : amina.merhoum@mairie-saint-denis.fr/ mp_achats@ville-saint-denis.fr

### 1.7. Architecture technique du groupement

Le réseau local de Plaine Commune comprend deux cœurs de réseau HP 7500 et différents types d'éléments actifs HP dans les sous-répartiteurs. L'architecture est redondante avec implémentation du "Spanning tree".

L'infrastructure de production est entièrement virtualisée sous Vsphere 4.1, comptant une centaine de serveurs principalement sous Windows. L'hyperviseur VMware gère 9 serveurs ESX, avec un environnement virtuel basé sur un châssis DELL Blade M1000e équipé de lames M610 et un SAN Compellent.

Informations techniques sur les différents sites :

| Entités | Plaine Commune | Saint-Denis |
|---------|----------------|-------------|
| Serveurs AD | 2008 R2 | 2003 et 2003 R2 |
| Nombre de DC | 2 DC | 2 DC Mairie-Saint-Denis.local<br>2 DC Saint-Denis.ad<br>2 DC Ville.Saint-Denis.ad |
| Messagerie | Exchange 2007 | Lotus Notes 6.5.4 |

Données chiffrées :

| Entités | Plaine Commune | Saint-Denis |
|---------|----------------|-------------|
| Nombre d'utilisateurs | 1500 | 3000 |
| Nombre de postes | 1000 | 1000 |

Chaque organisme possède son propre Active Directory. Les postes clients fonctionnent sous Windows (XP, Vista, 7, 8). Les utilisateurs de Plaine Commune disposent d'Outlook 2010 ou OWA. Ceux de Saint-Denis disposeront des mêmes messageries courant 2014.

### 1.8. Volumétrie

À titre indicatif, voici une estimation des volumes de ressources que le groupement envisage de gérer. Ces informations ne sont pas contractuelles mais aident les candidats à établir leurs offres et le coordinateur à les analyser.

Besoins identifiés par organisme pour les salles :

| Organisme | Salles | Sites | Groupes de gestionnaires (*) |
|-----------|--------|-------|------------------------------|
| CA Plaine Commune | 25 | 3 | 5 |
| Ville de Saint-Denis | 25 | 4 | 5 |

Autres types de ressources :

| Type de ressource | Nombre (Plaine Commune + Saint-Denis) | Sites | Groupes de gestionnaires(*) |
|-------------------|--------------------------------------|-------|------------------------------|
| Voitures | 60 | 2 | 5 |
| Bicyclettes | 10 | 2 | 2 |
| Ordinateurs | 10 | 2 | 2 |
| Téléphones portables | 10 | 2 | 2 |
| Clés 3G | 10 | 2 | 2 |
| Vidéoprojecteurs | 6 | 2 | 2 |

(*) Un groupe de gestionnaires est un ensemble de personnes qui gère et valide les réservations d'un ensemble de ressources.

Recensement du nombre d'utilisateurs de chaque organisme :

| Organisme | Nb d'utilisateurs potentiels | Nb d'utilisateurs effectifs | Gestionnaires différents |
|-----------|------------------------------|----------------------------|--------------------------|
| CA Plaine Commune | 3000 (tout l'AD) | 330 | 5 |
| Ville de Saint-Denis | 200 | 200 | 5 |

Cette liste n'est pas exhaustive et d'autres types de ressources pourraient s'ajouter pendant la durée du marché.

## 2. Dispositions générales

### 2.1. Engagement de confidentialité

Dans le cadre de ses interventions sur le logiciel et pour garantir le secret, la sécurité et la confidentialité des données, le Titulaire s'engage à :
- Prendre toutes les précautions nécessaires pour préserver la sécurité des données
- Ne traiter les données que selon les instructions et autorisations du coordinateur
- Ne traiter les informations qu'en interne et dans le cadre de cette consultation
- S'assurer de la légalité des traitements réalisés
- Préciser s'il a recours à un sous-traitant (sauf si mandaté par le coordinateur)
- Respecter les obligations de secret, sécurité et confidentialité lors des opérations de maintenance
- Prendre toutes les mesures de sécurité nécessaires pour assurer la conservation et l'intégrité des données
- Empêcher toute utilisation détournée, malveillante ou frauduleuse des données
- Détruire les accès en fin de contrat
- Ne pas divulguer les informations contenues dans les fichiers ou recueillies pendant l'exécution du contrat
- Ne pas utiliser les supports ou documents confiés à des fins autres que celles définies au contrat

### 2.2. Responsabilités du candidat

Le Titulaire devra assurer toutes les prestations nécessaires à la bonne mise en œuvre de la solution, même celles non expressément mentionnées.

Le Titulaire ne pourra pas invoquer d'omissions ou d'oublis dans sa proposition et devra se renseigner auprès du coordinateur pour tout ce qui lui semblerait incomplet ou imprécis.

En cas de difficulté d'interprétation, les prestations exigibles seront celles assurant les meilleures performances de fonctionnement et de coût, au choix des membres du groupement.

Toute dérogation non prévue par le CCTP devra recevoir l'accord du groupement.

## 3. La solution de réservation de ressources

Le coordinateur demande une solution complète et opérationnelle répondant aux spécifications du cahier des charges. La solution sera déployée dans un environnement de production et un environnement de développement pour les deux membres du groupement.

### 3.1. Gestion et profils des utilisateurs

Le Titulaire décrira son module de gestion des profils d'utilisateurs. Pour chaque collectivité et par type de flux, les profils pourraient être identifiés ainsi :

- **Administrateurs** : Accès à toutes les fonctionnalités du progiciel (paramétrage, création d'utilisateurs, de ressources, gestion des droits d'accès)
- **Gestionnaires de ressources** : Chargés de définir et veiller au bon déroulement des processus de réservation des ressources sous leur responsabilité. Ils peuvent rendre une ressource indisponible, valider ou refuser des réservations, arbitrer les conflits et réserver directement sans validation.
- **Demandeurs de ressources** : Accès en consultation au planning des ressources disponibles. Ils peuvent demander des réservations pour validation ou réserver directement les ressources ne nécessitant pas de validation.
- **Agent d'accueil** : Pour les salles ou équipements accueillant du public. Ils ont accès en consultation aux informations sur les réunions pour renseigner les participants (participants, sociétés, horaires, salles, objet).
- **Pilote de réunion** : Personne qui conduit une réunion, mentionnée comme donnée lors de la réservation d'une salle. Ce profil ne nécessite pas de droits spécifiques.
- **Service support** (éventuellement) : Accès aux réservations les concernant pour participer au processus de préparation, d'accueil et de restitution de la ressource.

Le logiciel doit permettre de définir des groupes d'utilisateurs ayant les mêmes droits.

### 3.2. Ressources traitées, fonctionnalités attendues

Le SRR devra gérer au minimum toutes les ressources mentionnées dans l'objet du marché et à terme celles évoquées dans la section volumétrie. Le prestataire devra pouvoir proposer l'intégration de nouveaux types de ressources non identifiés lors de la rédaction du CCTP.

Le candidat détaillera les autres flux que la plateforme pourra supporter et qui ne sont pas décrits dans le document. Pour l'intégration des types de ressources non inclus dans la solution de base, le candidat expliquera la procédure (développement spécifique ou paramétrage).

Les ressources peuvent être classées selon leur disponibilité :
- Ressources libres : réservation directe par le demandeur sans validation
- Ressources soumises à validation : nécessitant l'approbation d'un gestionnaire pour que la réservation soit effective

Fonctionnalités attendues :
- Interface entièrement web
- Interface de réservation ergonomique et intuitive. La plupart des utilisateurs potentiels n'utiliseront le système que sporadiquement, d'où l'importance d'une interface permettant des réservations sans formation spécifique.
- Réservation de salles facilitée par des informations pertinentes (photo, nombre de places, configuration)
- Gestion de ressources fixes (salles des élus, équipements sportifs) avec informations et filtres adaptés à chaque type
- Gestion de ressources mobiles (voitures, PC portables, téléphones, écrans...) avec informations et filtres adaptés
- Définition de groupes d'utilisateurs gestionnaires des ressources
- Définition de circuits de validation distincts selon les types de ressources, avec deux workflows possibles :
  1) Pour les ressources sans validation : réservation directe par le demandeur
  2) Pour les ressources soumises à validation : demande par le demandeur puis approbation ou refus par un gestionnaire
- Production de statistiques d'utilisation des ressources

### 3.3. Intégration avec l'architecture en place

Le Candidat déclare connaître les éléments de l'environnement informatique du groupement nécessaires à son offre (matériel, logiciel, réseau, poste de travail).

Il garantit la compatibilité de la solution avec les environnements informatiques des membres du groupement. Le candidat est libre de proposer l'architecture qu'il juge la plus pertinente en tenant compte des impératifs de sécurité, de continuité de service et du coût total sur la durée du marché.

Le Candidat :
- Confirmera que la configuration du groupement est adaptée à sa solution et décrira la configuration minimale requise
- Indiquera et fournira les couches progicielles à installer en complément si nécessaire
- Précisera les moyens de protection contre les accès frauduleux

### 3.4. Intégration avec des logiciels tiers

Le logiciel proposé devra s'intégrer avec les Active Directory des deux organismes du groupement.

Les deux organismes disposeront de serveurs Exchange. Il est fortement souhaitable que le SRR envoie des notifications à la messagerie et qu'il soit accessible depuis les intranets des deux collectivités via NTLM 2.

### 3.5. Écran d'accueil pour le public

Le groupement souhaite disposer d'un grand écran d'information pour les visiteurs affichant les horaires et emplacements des réunions du jour. Ce besoin est identifié pour le siège de la Communauté d'Agglomération Plaine Commune, mais pourrait être étendu à d'autres sites.

Le candidat devra proposer une solution clé en main. La DSIM fournira une prise RJ45 connectée au réseau et trois prises électriques dans une salle proche de l'accueil et au même étage. Le reste des fournitures et l'installation seront à la charge du Titulaire : moniteur et support, câbles et prises, poste informatique installé et paramétré, et tout autre élément nécessaire.

Le candidat assurera la maintenance de l'ensemble (matériel et logiciel) et son bon fonctionnement.

### 3.6. Mise à disposition de la solution et vérifications qualitatives

La mise en ordre de marche de la solution devra être réalisée dans les 50 jours suivant la notification du marché pour permettre au groupement de procéder aux vérifications d'aptitude puis à la vérification de service régulier.

La ville de Saint-Denis prévoyant de déployer Exchange/Outlook/OWA courant 2014, les fonctionnalités du SRR nécessitant cette messagerie seront mises en place 30 jours après que le groupement aura informé le titulaire de la mise en exploitation de la nouvelle messagerie.

### 3.7. Fonctionnalités supplémentaires

Après la mise en service de la solution, la DSIM pourra demander au Titulaire la mise en place de réservations pour de nouveaux types de ressources.

La DSIM décrira le contexte, les modifications souhaitées, l'existant, la cible, les exigences, les contraintes et les délais. Si le prestataire juge la demande réalisable, il fournira un devis forfaitaire détaillant les caractéristiques de la nouvelle solution, les livrables, les services et les étapes de conception, développement, tests, formations, installation et mise en œuvre.

### 3.8. Documentation

Les documentations fonctionnelles et techniques font partie intégrante de la fourniture de la solution et seront rédigées en français.

La documentation fonctionnelle décrira les fonctionnalités disponibles, leur mode d'accès et leurs conditions d'utilisation pour tous les modules de la solution.

La documentation technique précisera au minimum :
- L'environnement et les contraintes techniques liés au produit
- Les modalités d'intégration dans la chaîne d'exploitation interne (pour les solutions internalisées)
- Les modalités de paramétrage
- Les limites et contraintes d'utilisation
- Une matrice des flux précisant les ports de communication et la bande passante conseillée

Le Titulaire précisera les supports de documentation (papier, aide en ligne...), avec une préférence pour un support informatique au format PDF. Il indiquera les modalités et fréquences de mise à jour, le nombre d'exemplaires fournis gratuitement, et l'existence éventuelle d'un club utilisateur.

### 3.9. Disponibilité

Pour une solution hébergée par le titulaire (mode SAAS), la plateforme et ses services doivent être accessibles au minimum tous les jours ouvrés de l'administration de 8h à 24h sans exception. Le Titulaire indiquera les horaires de disponibilité garantis et décrira en détail l'environnement technique.

Il précisera les moyens et modalités proposés pour faire face aux :
- Dysfonctionnements
- Intrusions
- Indisponibilités

Le Titulaire assurera :
- Le suivi de la connexion et du fonctionnement des serveurs
- Une haute disponibilité
- Une protection contre les attaques extérieures avec des tests périodiques
- La sécurité des données (disponibilité, intégrité, confidentialité, traçabilité)
- Des serveurs de secours
- Un environnement de test et éventuellement de pré-production accessibles simultanément et indépendamment par les membres du groupement
- Un dispositif pour basculer la solution vers le logiciel d'un autre prestataire si nécessaire
- Un taux minimal de disponibilité de 97% (calculé sur une tentative toutes les 2 minutes sur 3 jours ouvrables consécutifs)
- Des temps de réponse garantis : en solution hébergée, le temps moyen d'envoi d'une page (80ko et 5 fichiers image) doit être inférieur à 2 secondes, avec un maximum de 10 secondes

### 3.10. Les prestations de réversibilité

Le titulaire s'engage à mettre en place avant la présentation de son offre tous les éléments matériels, logiciels et organisationnels nécessaires à la réversibilité de la prestation et à les maintenir pendant toute la durée du contrat.

Chaque membre du groupement reste seul propriétaire des données et métadonnées de son SRR.

Le groupement pourra demander la réversibilité en informant le Titulaire trois mois avant l'échéance souhaitée par courrier recommandé. La prestation sera ensuite lancée par bon de commande précisant les modalités et étapes à suivre.

Les candidats devront détailler dans leur offre les moyens disponibles et les conditions de délais, matérielles et financières de cette prestation, notamment :
- Le délai entre la demande et la réalisation complète (maximum trois mois calendaires)
- Le prix de la prestation pour le groupement entier et pour un seul membre
- Les moyens que le groupement doit mettre en œuvre
- Un planning type
- Le(s) format(s) des données restituées (format universel exploitable par tout prestataire SRR)

Le non-respect des délais contractuels pour la réversibilité entraînera des pénalités selon les modalités du CCAG et du CCAP.

## 4. Contraintes techniques

### 4.1. Pré requis des postes de travail

Le Titulaire communiquera les prérequis techniques matériels et logiciels pour le bon fonctionnement de la solution sur les postes de travail du groupement :
- Configuration matérielle minimale supportée
- Systèmes d'exploitation supportés et versions
- Navigateurs standards supportés et versions
- Prérequis de configuration avec procédures de paramétrage si nécessaire

Il détaillera les applications à installer sur les postes de travail et les éventuelles incompatibilités avec des applications bureautiques, des applications métiers ou des éléments de configuration.

### 4.2. Prérequis réseau

Le titulaire décrira les prérequis et contraintes réseau pour le bon fonctionnement de la solution :
- Débits réseau minimum et recommandé
- Ouvertures de ports ou filtrages nécessaires

## 5. Mise en œuvre de la solution

Pour les prestations de mise en œuvre, le titulaire proposera un prix forfaitaire dans son BPU.

### 5.1. Formation

Le Titulaire assurera sur site la formation nécessaire pour les gestionnaires et les administrateurs dans les sièges des membres du groupement. Aucune formation n'est prévue pour les demandeurs de ressources, d'où l'importance d'une interface intuitive permettant une prise en main immédiate.

Le Titulaire proposera des experts expérimentés dans les contacts avec les utilisateurs et précisera les connaissances préalables requises. Il proposera des formations adaptées aux différents profils d'usagers. Le groupement validera le plan de formation et son organisation.

Ce plan de formation mentionnera :
- Les éventuels prérequis logistiques ou techniques (salle, configuration des postes...)
- Les contenus précis des modules

Pour chaque formation, le Titulaire fournira un support en français sur support informatique au moins 4 jours ouvrables avant la première séance. L'effectif de chaque formation sera déterminé par le coordinateur.

### 5.2. Expertise

Le Titulaire assurera sur site, à la demande de la DSIM, les prestations suivantes :
- Expertise
- Assistance
- Transfert de compétences
- Animation de réunions de pilotage ou techniques pour les choix stratégiques d'implémentation et d'optimisation

Il proposera des experts ayant une expérience éprouvée de contact avec les utilisateurs finaux.

### 5.3. Planning

Pour la première phase d'implémentation, les deux organismes souhaitent commencer par la gestion des salles de réunion. Pour les ressources non incluses dans l'offre de base, le candidat indiquera le délai nécessaire pour leur intégration dans l'outil.

Le Titulaire détaillera les phases et le planning de mise en œuvre de la solution, ainsi que la méthodologie et l'organisation prévues avec les directions et services pour rendre la solution opérationnelle.

Le Coordinateur organisera une réunion de lancement avec le groupe projet dans les deux semaines suivant la notification du marché. Lors de cette réunion, un planning plus précis sera établi pour définir les chantiers de travail proposés aux directions et services.

## 6. Garantie, Maintenance et gestion des incidents

### 6.1. Garantie et maintenance

La commande inclut la maintenance, gratuite pendant la période de vérification d'aptitude et de vérification de service régulier. La maintenance sera préventive, curative et évolutive.

Le Titulaire s'engage à maintenir l'application pendant toute la durée du marché. Cette prestation inclut la maintenance corrective, la mise à disposition de nouvelles versions et l'assistance téléphonique.

Le groupement communiquera au titulaire les personnes habilitées à utiliser l'assistance téléphonique : personnel de la DSI pour les aspects techniques et correspondants fonctionnels des deux organismes pour le volet fonctionnel.

Le Titulaire détaillera précisément les modalités de maintenance fonctionnelle et technique.

### 6.2. Gestion des incidents

En cas d'interruption du Service pour maintenance ou mise à jour, le Titulaire planifiera les interventions en accord avec le groupement.

L'assistance téléphonique (hotline) sera accessible au moins de 9h à 18h tous les jours ouvrables.

Le titulaire précisera les modalités de contact de sa hotline fonctionnelle et technique, le type de demandes prises en compte, ses heures ouvrées, les conditions de signalement d'incidents ainsi que leurs délais et modalités de résolution.

Les délais d'engagement du candidat ne devront pas dépasser ceux du tableau suivant :

| Type d'incident | Délai de prise en charge | Délai de résolution |
|-----------------|--------------------------|---------------------|
| Bloquant | 4 heures ouvrées de l'administration | 1 jour ouvré pour résolution ou contournement |
| Non bloquant | 8 heures ouvrées de l'administration | 1 semaine calendrier |
| Exploitation d'une solution de contournement | | 1 semaine calendrier |

Typologie des incidents :
- **Incident bloquant** : incident empêchant l'aboutissement d'une fonction nécessaire au bon fonctionnement de l'application, ou résultats incohérents par rapport aux paramètres définis.
- **Incident non bloquant** : arrêt d'un traitement sans préjudice majeur sur le résultat attendu, ou arrêt/incident ne remettant pas en cause la réalisation de la fonction.
- **Solution de contournement en exploitation** : suite à un incident bloquant non corrigeable dans les délais, mise en place d'une solution permettant d'exploiter les fonctionnalités, éventuellement en mode dégradé ou limité.

Le non-respect des délais engendrera des pénalités selon les modalités du CCAG et du CCAP.

## 7. Modalités administratives

### 7.1. Cadre de réponse

Les candidats doivent utiliser le cadre de réponse fourni pour présenter leur offre de façon formatée afin de faciliter l'analyse. Ce cadre constitue un minimum de réponse que chaque candidat peut compléter par toute information utile.

Se conformer à ce cadre de réponse est important pour garantir une analyse objective de l'offre.

Le cadre de réponse comprend :
- Un Cadre de Réponse Technique et Fonctionnelle (CRTF)
- Un Bordereau des Prix Unitaires (BPU) servant de Devis Quantitatif Estimatif (DQE)

La valeur financière de l'offre sera évaluée sur le DQE.

Le document doit être signé par le candidat avec date, nom et qualité du signataire.
