# Cahier des Clauses Techniques Particulières

**Groupement de commandes pour l'acquisition, la mise en œuvre et la maintenance d'un logiciel de réservation de salles et diverses ressources pour la communauté d'agglomération Plaine Commune et la ville de Saint-Denis**

**PROCÉDURE DE CONSULTATION :**
**MARCHÉ À PROCÉDURE ADAPTÉE EN APPLICATION DES ARTICLES 28 DU CODE DES MARCHÉS PUBLICS**

**Système de réservation de ressources**

## 1. LE PROJET

### 1.1. Préambule

Les chapitres du présent document décrivent les fournitures et prestations attendues des titulaires du présent marché.
Le présent document est complété :
- d'un "Bordereau des prix unitaires (BPU)" faisant office de "Devis quantitatif estimatif (DQE)" au sein duquel celui-ci décrit son offre quantitative et économique
- D'un « Cadre de Réponse Technique et Fonctionnelle » (CRTF), que le candidat devra remettre avec ses réponses aux questions posées pour faciliter l'analyse qualitative des offres.

Le groupement de commande est constitué par :
- La communauté d'agglomération Plaine Commune
- La Ville de Saint-Denis.

Dans la suite du document, les termes « le groupement » ou « les membres du groupement », dans un cadre contractuel, désignent le groupement composé par les deux membres du groupement de commande.
Le coordinateur de ce groupement de commande est la ville de Saint-Denis, le terme « le coordinateur » désigne celle-ci.
Le terme DSIM désigne la Direction des Systèmes d'Information Mutualisée.
L'abréviation SRR signifie système de réservation de ressources.
Le terme SAAS désigne le mode d'hébergement externalisé où les logiciels sont installés sur des serveurs distants. La maintenance logicielle et matérielle des serveurs, l'intégrité des données et les moyens matériels logiciels et de réseau mis à disposition du groupement, sont sous la complète responsabilité du titulaire.

### 1.2. Contexte

La communauté d'agglomération Plaine Commune, la ville de Saint-Denis et la ville de Villetaneuse ont mené un processus de mutualisation de leurs directions des systèmes d'information qui s'est concrétisé le 1er janvier 2011.
Dans ce cadre, ces trois partenaires ou bien deux parmi les trois, comme dans ce cas, constituent des groupements de commandes pour mener ensemble certains projets informatiques et répondre à des besoins communs.

La ville de Saint Denis dispose d'un système de réservation de salles de réunion ouvert à tous les agents disposant de la messagerie lotus. Aujourd'hui, 200 agents réservent des salles avec ce logiciel. Il a été développé sur la plateforme lotus/domino qui doit être remplacée à moyen terme par la messagerie Outlook/exchange. Cette évolution rendrait le système de réservation actuel inopérant, d'où la nécessité de trouver une autre solution.

La communauté d'agglomération Plaine Commune utilise un système de réservation de salles issu d'un développement spécifique sans maintenance ni support, qui globalement donne satisfaction sur les fonctions de base, mais son évolution vers une autre ergonomie ainsi qu'une extension de ses fonctionnalités et de son périmètre sont difficilement envisageables. Ce système n'a plus de maintenance ni de support ce qui fait qu'il n'est plus envisageable de continuer de l'utiliser. 330 agents font des réservations de salles avec le logiciel en place.

Aucun des deux organismes ne possède un SRR (système de réservation de ressources) pour des ressources autres que des salles.
Dans ce contexte, les collectivités du groupement veulent se doter d'un outil unique qui permette aux agents des collectivités de réserver des ressources avec une interface qui leur donne les disponibilités et les informations pertinentes pour faire les meilleurs choix en fonction de leurs besoins.
Ce projet exclut les réservations de ressources à destination de la population.
Cet outil devra permettre aux gestionnaires des ressources de les mettre à disposition des usagers, de guider et de monitorer les réservations dans le but d'optimiser leur utilisation et de s'assurer que l'affectation des ressources est conforme aux règles. Il sera mis à disposition des gestionnaires des outils statistiques pour ajuster la nature et la volumétrie des ressources mises à disposition des agents.

### 1.3. Recommandations

Les candidats devront répondre sans ambiguïté et dans l'ordre, à toutes les demandes du présent CCTP ainsi qu'aux questions du CRTF. Les réponses données dans le CRTF primeront sur le mémoire technique.

Les candidats sont informés que, quelle que soit la somme des renseignements techniques donnés ci-après, les offres reçues seront considérées comme étant établies en pleine et entière connaissance du CCTP.

Les deux membres du groupement privilégient la saisie faite par les demandeurs directement sur le logiciel, contrairement aux solutions où les intéressés s'adresseraient à un service centralisé pour que leur demande soit saisie. Pour des raisons de commodité de gestion, le groupement préfère une tarification de type « site » ou « fonctionnalité », plutôt qu'une tarification utilisateur.

### 1.4. Objet du Marché

Ce marché a pour objet de doter les deux membres du groupement d'une solution de réservation de ressources.

Cette solution devra :
- être full web
- avoir une interface de réservation ergonomique et intuitive, utilisable sans formation présentielle
- gérer divers types de ressources fixes et mobiles : au minimum des salles de réunion, des salles événementielles, des voitures, des bicyclettes et des ordinateurs portables.
- communiquer sur les évènements associés aux réservations : confirmation, annulation...
- baser la réservation sur des « workflows » (circuits de validation) prédéfinis

### 1.5. Durée du marché

Le marché aura une durée de validité allant de sa date de notification à la fin de la période de garantie et pourra être renouvelé 3 fois par périodes de un an. La période de garantie sera d'un an à compter de la réception de la VSR.
Si le candidat propose une solution « achat de licence » les renouvellements concerneront la maintenance. Si la solution proposée est de type SAAS les renouvellements porteront sur le droit d'usage du logiciel, maintenance incluse.

### 1.6. Personnes en charge du marché

Service chargé de la procédure et de donner les renseignements prévus au Code des Marchés Publics :
- Direction de la commande publique de la Ville de Saint-Denis
- Madame Amina Merhoum
- Téléphone : 01 49 33 66 84
- Courriel : amina.merhoum@mairie-saint-denis.fr/ mp_achats@ville-saint-denis.fr

### 1.7. Architecture technique du groupement

Le réseau local de Plaine Commune est composé de 2 cœurs de réseau HP 7500 et de différents types d'éléments actifs HP dans les sous répartiteurs. L'architecture est redondante et le « Spanning tree » est implémenté.

L'infrastructure de production est complètement virtuelle sous Vsphère 4.1, cela représente une centaine de serveurs sous Windows majoritairement. L'hyperviseur Vmware gère 9 serveurs ESX, cet environnement virtuel est basé sur un châssis DELL Blade M1000e avec des lames M610 et un SAN Compellent.

Informations techniques sur les différents sites :

| Entités | Plaine Commune | Saint-Denis |
|---------|----------------|-------------|
| Serveurs AD | 2008 R2 | 2003 et 2003 R2 |
| Nombre de DC | 2 DC | 2 DC Mairie-Saint-Denis.local <br> 2 DC Saint-Denis.ad <br> 2 DC Ville.Saint-Denis.ad |
| Messagerie | Exchange 2007 | Lotus Notes 6.5.4 |

Et quelques données en chiffres :

| Entités | Plaine Commune | Saint-Denis |
|---------|----------------|-------------|
| Nombre d'utilisateurs | 1500 | 3000 |
| Nombre de postes | 1000 | 1000 |

Chacun des 2 organismes possède son propre AD.
Les postes client fonctionnent sous des systèmes d'exploitation Windows (XP, vista, seven, 8). Les utilisateurs de la communauté d'agglomération Plaine Commune disposent de Outlook 2010 ou OWA. Les utilisateurs de la Ville de Saint-Denis disposeront de ces mêmes messageries courant 2014.

### 1.8. Volumétrie

A titre indicatif, voici une estimation des volumes de ressources que le « groupement » se propose de gérer compte tenu de ses connaissances au moment de la rédaction du présent document. Ces informations ne sont en aucun cas contractuelles, elles sont fournies afin de permettre aux candidats d'établir leur offre et au « coordinateur » de les analyser.

Recensement des besoins identifiés à ce jour par organisme :

| Salles organisme | Salles | sites | Groupes de gestionnaires (*) |
|------------------|--------|-------|------------------------------|
| CA Plaine Commune | 25 | 3 | 5 |
| Ville de Saint-Denis | 25 | 4 | 5 |

| Type de ressource | Nombre (Plaine Commune + Saint-Denis) | Sites | Groupes de gestionnaires(*) |
|-------------------|--------------------------------------|-------|------------------------------|
| voitures | 60 | 2 | 5 |
| bicyclettes | 10 | 2 | 2 |
| ordinateurs | 10 | 2 | 2 |
| téléphones portables | 10 | 2 | 2 |
| clés 3G | 10 | 2 | 2 |
| vidéoprojecteurs | 6 | 2 | 2 |

(*) Un groupe de gestionnaires est un ensemble de personnes qui gère et valide les réservations d'un ensemble de ressources.

Recensement du nombre d'utilisateurs de chaque organisme :

| organisme | Nb d'utilisateurs potentiels | Nb d'utilisateurs effectifs | Gestionnaires différents |
|-----------|------------------------------|----------------------------|--------------------------|
| CA Plaine Commune | 3000 (tout l'AD) | 330 | 5 |
| Ville de Saint-Denis | 200 | 200 | 5 |

Commentaires sur la volumétrie :
- Cette liste n'est pas exhaustive et d'autres types de ressources pourraient s'ajouter pendant la durée du marché.

## 2. DISPOSITIONS GÉNÉRALES

### 2.1. Engagement de confidentialité

Dans le cadre de ces interventions sur le logiciel et afin de garantir le secret, la sécurité et la confidentialité des données, le Titulaire s'engage à :
- prendre toutes les précautions nécessaires afin de préserver la sécurité des données, notamment empêcher qu'elles ne soient déformées ou endommagées et empêcher tout accès qui ne serait pas préalablement autorisé par le coordinateur;
- ne traiter les données que dans le cadre des instructions et de l'autorisation reçues du coordinateur;
- ne traiter les informations qu'entièrement et exclusivement en interne et dans le cadre de la présente consultation;
- s'assurer de la licéité des traitements réalisés dans le cadre de la mission confiée;
- préciser s'il a recours aux services d'un sous-traitant sauf à ce que ce dernier soit préalablement et expressément mandaté par le coordinateur ou son représentant. Dans ce cas le sous-traitant agira sous la responsabilité du groupement et le contrôle du titulaire.
- respecter son obligation de secret, de sécurité et de confidentialité, à l'occasion de toute opération de maintenance et de télémaintenance, réalisée au sein de ses locaux ou de toute société intervenant dans le cadre des traitements;
- prendre toutes les mesures de sécurité, notamment matérielle et logique, pour assurer la conservation et l'intégrité des données traitées;
- prendre toutes les dispositions permettant d'empêcher toute utilisation détournée, malveillante ou frauduleuse des données traitées;
- procéder, en fin de contrat, à la destruction des accès figurant sur tout support.
- ne pas divulguer, sous quelque forme que ce soit, tout ou partie des informations contenues dans des fichiers informatisés ou manuels, ou figurant sur tout support transmis par la collectivité ou concernant les informations recueillies au cours de l'exécution du présent contrat;
- ne pas utiliser les supports ou documents qui lui ont été confiés, par quelque moyen ou finalité que ce soit, pour son compte ou pour le compte de tiers, à des fins professionnelles, personnelles ou privées autres que celles définies au présent contrat;

### 2.2. Responsabilités du candidat

Le Titulaire devra assurer les prestations même non mentionnées, mais nécessaires à la bonne mise en œuvre de la solution.
Le Titulaire ne pourra se prévaloir d'omissions ou d'oublis dans sa proposition et devra se renseigner auprès du coordinateur pour tout ce qui lui paraitrait incomplet ou imprécis.
En cas de difficulté d'interprétation, les prestations exigibles seront celles assurant les meilleures performances de fonctionnement et de coût, au choix des membres du groupement.
Toute dérogation ne faisant pas l'objet d'un point du présent C.C.T.P. devra impérativement recevoir l'accord du groupement.

## 3. LA SOLUTION DE RÉSERVATION DE RESSOURCES

Le coordinateur demande la fourniture d'une solution complète et opérationnelle et répondant aux spécifications du présent cahier des charges. La solution sera mise à disposition dans un environnement de production et un environnement de développement pour les deux membres du groupement.

### 3.1. Gestion et profils des utilisateurs

Le Titulaire décrira son module de gestion des profils d'utilisateurs. Pour chaque collectivité et par type de flux, les profils pourraient être identifiés ainsi :

- **Administrateurs**. Ils ont accès à toutes les fonctionnalités du progiciel, notamment le paramétrage, la création des utilisateurs, des ressources, et la gestion des droits d'accès aux différentes fonctionnalités
- **Gestionnaires de ressources**. Ils sont chargés de définir et de veiller au bon déroulement des processus de réservation des ressources dont ils ont la charge. Ils pourront rendre indisponible ou bloquer à la réservation une ressource pendant une période. Ils devront valider les réservations des ressources soumises à validation ou communiquer le motif du refus au demandeur. Ils devront arbitrer en cas de conflit et chercher des solutions alternatives en accord avec les demandeurs. Le gestionnaire pour réserver directement les ressources qu'il gère sans validation.
- **Demandeurs de ressources**. Ils ont accès en consultation à un planning de réservation des ressources qui leur ont été mises à disposition. Ils peuvent poser une demande de réservation de ressource pour validation de la part d'un gestionnaire ou bien réserver directement les ressources non soumises à validation.
- **Agent d'accueil**. Ce profil ne concerne que les salles ou les équipements qui accueillent du public. Les agents d'accueil ont accès en consultation à des informations sur les réunions afin de renseigner les participants lors de leur arrivée (nombre et noms des participants, des sociétés, horaires, salles, objet). Il peut s'agir d'hôtesses aux accueils des sites ou de gardiens des installations.
- **Pilote de réunion**. Personne qui conduit une réunion. Il peut être renseigné en tant que donnée lors de la réservation d'une salle. Ce profil ne nécessite pas des droits spécifiques sur le logiciel.

- Eventuellement un profil **Service support** qui a accès aux réservations qui le concernent pour participer au processus de préparation, d'accueil et de restitution de la ressource.

Le logiciel doit permettre de définir des groupes d'utilisateurs ayant les mêmes droits.

### 3.2. Ressources traitées, fonctionnalités attendues

Le SRR devra gérer au minimum toutes les ressources évoquées dans le point « objet du marché » et à terme tous ceux évoqués dans la point « volumétrie ».
Le prestataire devra être en mesure de proposer l'intégration de nouveaux types de ressources non identifiées lors de la rédaction du présent CCTP.
Le cas échéant, le candidat détaillera les autres flux que la plateforme sera à même de supporter et qui ne sont pas décrits ici. Les prestations proposées seront décrites par le candidat dans son mémoire technique dans le cadre de son offre.
Pour l'intégration des types de ressources non prises en compte par la solution de base, le candidat expliquera quelle est la procédure pour les intégrer. Notamment si un développent spécifique est nécessaire ou bien si l'intégration peut se faire par le biais d'un paramétrage du logiciel.

Les ressources, selon leur disponibilité, peuvent être classées comme suit :
- **Ressources libres**, quand la réservation est faite par de demandeur (sans validation)
- **Ressources soumises à validation**. Une validation de la part du gestionnaire est nécessaire pour que la réservation soit effective. Cette catégorie inclut les salles des élus ou protocolaires pour lesquelles la validation est faite par les secrétariats correspondants.

Fonctionnalités attendues :

- full web
- interface de réservation ergonomique et intuitive. Les utilisateurs potentiels du SRR sont trop nombreux et la plupart d'entre eux ne l'utilisera que très sporadiquement d'où le besoin de disposer d'un SRR qui permette de faire des réservations sans avoir reçu de formation spécifique.
- réservation de salles aidée par des informations pertinentes pour rendre la réservation de la ressource plus aisée (photo, nombre de places, configuration dans le cas d'une salle)
- possibilité de gestion d'autres ressources fixes (salles des élus, équipements sportifs) avec des informations et des filtres adaptés à chaque type de ressource. Par exemple un gymnase peut avoir comme informations adresse, numéro de téléphone de l'accueil, capacité de personnes debout, ouvert/couvert et ces deux dernières informations peuvent être des critères de filtrage.
- possibilité de gestion d'autres ressources mobiles (voitures, PC portables, téléphones, écrans...) avec des informations et des filtres adaptés selon chaque type de ressource. Par exemple un ordinateur portable peut avoir comme informations numéro d'inventaire, marque, taille d'écran et la taille d'écran peut être un critère de recherche.
- définition de groupes d'utilisateurs gestionnaires des ressources.
- définition de circuits de validation distincts pour chaque sous-ensemble de ressources : la réservation d'une salle de réunion interne, d'une salle des fêtes et d'un équipement sportif ne devraient pas être validées par le même groupe de gestionnaires. Le logiciel doit permettre de définir deux types de workflows selon le type de ressource :
  1) pour les ressources ne nécessitant pas de validation,  
     - réservation de la part du demandeur.
  2) pour les ressources soumises à validation,  
     - demande de réservation de la part du demandeur
     - approbation ou refus de la part d'un des gestionnaires de la ressource
- produire des statistiques d'utilisation des ressources ;

### 3.3. Intégration avec l'architecture en place

Le Candidat déclare connaître les éléments de l'environnement informatique du groupement nécessaires à l'établissement de son offre (matériel, logiciel, réseau, poste de travail).
Il garantit la compatibilité, de la solution aux environnements informatiques des membres du groupement. Dans ce cadre, le candidat est libre de proposer l'architecture qu'il jugera la plus pertinente en tenant compte les impératifs de sécurité et de continuité du service ainsi que le coût total sur la durée du marché.

Le Candidat :
- confirmera que la configuration du groupement (serveurs, postes de travail) est adaptée à la solution qu'il propose et décrira la configuration minimale requise,
- indiquera et fournira s'il y a lieu, les couches progicielles à installer en complément,
- précisera les moyens de protection mis en œuvre par la solution pour interdire les accès frauduleux.

### 3.4. Intégration avec des logiciels tiers

Le logiciel proposé devra s'intégrer avec les deux AD des organismes du groupement.

Les deux organismes disposeront de serveurs « Exchange ». Il est fortement souhaitable que le SRR envoie des notifications à la messagerie, et qu'il soit accessible à partir des intranets des deux collectivités à travers NTLM 2.

### 3.5. Ecran d'accueil pour le public

Le groupement souhaite disposer d'un grand écran d'information adressé aux visiteurs avec les horaires et emplacements des réunions de la journée. Le besoin a été identifié pour le site « siège de la Communauté d'Agglomération Plaine Commune » mais le groupement se réserve la possibilité d'étendre cette prestation à d'autres sites.
Le candidat devra proposer une solution clé en main pour doter l'accueil des sites d'un grand écran pour afficher ces informations. La DSIM mettra à disposition du Titulaire une prise RJ45 connectée au réseau ainsi que trois prises électriques dans la salle ou se trouvera le poste qui contrôlera l'écran. Cette salle se trouvera au même étage et à proximité de l'accueil. Le reste des fournitures, ainsi que l'installation du dispositif, seront à la charge du Titulaire. Ceci inclut, le moniteur et son support, les câbles et prises, le poste informatique installé et paramétré ainsi que tout autre élément ou prestation nécessaire à la mise à disposition d'une solution clé en main.
Le candidat assurera la maintenance de l'ensemble matériel plus logiciel ainsi que le maintien de mode opérationnel de la solution.

### 3.6. Mise à disposition de la solution et vérifications qualitatives

La mise en ordre de marche de solution devra être faite dans les 50 jours qui suivront la notification du marché pour que le groupement puisse procéder à la vérification d'aptitude et puis à la vérification de service régulier.

Étant donné que la ville de Saint-Denis compte mettre à disposition de l'ensemble des utilisateurs une messagerie Exchange/Outlook/OWA courant 2014, les fonctionnalités du SRR qui ne sont exploitables que pour des utilisateurs Exchange/Outlook/OWA seront mises en place 30 jours après la date où le groupement informera le titulaire de la mise en exploitation de la nouvelle solution de messagerie.

### 3.7. Fonctionnalités supplémentaires

A partir de la mise en service de la solution, la DSIM pourra, si elle en avait besoin, faire appel au Titulaire pour mettre en place la réservation de types de ressources supplémentaires.
La DSIM décrira le contexte, les modifications, l'existant en service, la cible à atteindre, les exigences, les contraintes, et les délais.
Si le prestataire juge la demande réalisable il fournira un devis forfaitaire. Avec ce devis, il détaillera les caractéristiques de la solution nouvelle, l'ensemble des livrables et services et les étapes de conception, développement, tests, formations, installation et mise en œuvre.

### 3.8. Documentation

Les documentations fonctionnelles et techniques font partie intégrante de la fourniture de la solution. Elles seront rédigées en français.
Pour l'ensemble des modules composants la solution, la documentation fonctionnelle décrira les fonctionnalités disponibles, leur mode d'accès et leurs conditions d'utilisation.
La documentation technique doit préciser au minimum :
- L'environnement et les contraintes techniques liées au produit ;
- Les modalités d'intégration dans la chaîne d'exploitation interne (seulement si la solution proposée est internalisée) ;
- Les modalités de paramétrage ;
- Les limites et contraintes d'utilisation ;
- Une matrice des flux précisant les ports de communication et la bande passante conseillée.

Le Titulaire précisera les supports utilisés pour la documentation (papier, aide en ligne...). Il est souhaité que celle-ci soit également fournie sur un support informatique, au format PDF de préférence.
Il précisera les modalités et les fréquences de mises à jour de sa documentation, le nombre d'exemplaires de documentation fournis gratuitement avec la solution.
Le titulaire indiquera l'existence éventuelle d'un club utilisateur et les membres qui y participent.

### 3.9. Disponibilité

Si la solution proposée est hébergée par le titulaire (mode SAAS), la plateforme et ses services doivent être accessibles au minimum tous les jours ouvrés de l'administration sans exception de 8 heures à 24 heures. Le Titulaire indiquera les horaires de disponibilité de la plateforme sur lesquels il s'engage et fournira la description détaillée de l'environnement technique. Il explicitera les services complémentaires qu'il propose dans le cadre de la solution.
Il s'engagera sur les moyens et les modalités proposées pour faire face aux :
- dysfonctionnements,
- intrusions,
- indisponibilités

Le Titulaire assurera :
- Un suivi de la connexion et du fonctionnement des serveurs,
- Une haute disponibilité ;
- Une protection contre les attaques extérieures avec des tests périodiques ;
- Une prise en compte de la sécurité des données en termes de disponibilité, intégrité, confidentialité et traçabilité ;
- La mise en place d'un dispositif de serveurs de secours ;
- La mise en place d'un environnement de test et éventuellement un autre de pré-production où les membres du groupement puissent y accéder de façon simultanée et indépendante;
- La mise en place d'un dispositif fonctionnel, technique et d'accompagnement pour, le cas échant, basculer la solution vers le logiciel d'un autre prestataire, cf. « réversibilité ».
- Un taux minimal de disponibilité de 97 % (calculé sur la base d'une tentative toutes les 2 minutes sur une période de 3 jours ouvrables consécutifs) ;
- La garantie des temps de réponse : en cas de solution hébergée, le temps moyen d'envoi d'une page (80ko et 5 fichiers image) en HTML par le serveur web devra être inférieur à 2 secondes ; le temps maximum devra être inférieur à 10 secondes. Ce temps est mesuré entre l'arrivé de la requête sur le réseau du prestataire et la sortie complète de la page demandée.

### 3.10. Les prestations de réversibilité

Le titulaire s'engage à avoir mis en place avant la présentation de son offre, tous les éléments matériels logiciels et organisationnels nécessaires à la réversibilité de la prestation et à les maintenir durant toute la durée du contrat.
Chaque membre du groupement reste seul propriétaire des données et des métadonnées de son SRR.
Le groupement pourra demander la réversibilité en avisant le Titulaire, trois mois avant l'échéance attendue, en envoyant un courrier recommandé. La prestation de réversibilité sera ensuite démarrée avec un bon de commande au Titulaire qui mentionnera les modalités et étapes à suivre.
Les candidats devront détailler clairement dans leur offre les moyens disponibles et les conditions de délais, matérielles et financières de cette prestation, en particulier :
- le délai nécessaire entre la demande de réversibilité et sa réalisation complète. Ce délai ne pourra pas dépasser trois mois calendrier.
- le prix de la prestation complète pour le groupement entier et pour un des intégrants.
- les moyens que doit mettre en œuvre le groupement pour mener à bien la prestation  
- un planning type de réversibilité.
- le(s) format des données restituées, qui devra être un format universel exploitable par tout prestataire SRR.

Le non-respect de l'exécution de la prestation de réversibilité dans délais contractuels engendrera des pénalités qui s'appliqueront selon les modalités prévues dans le CCAG et le CCAP.

## 4. CONTRAINTES TECHNIQUES

### 4.1. Pré requis des postes de travail

Le Titulaire communiquera les prérequis techniques matériels et logiciels pour le bon fonctionnement de la solution sur les postes de travail du groupement. Il indiquera :
- La configuration matérielle minimale supportée par la solution sur les postes de travail ;
- la liste des systèmes d'exploitation supportés ainsi que leurs versions ;
- la liste des navigateurs standards supportés ainsi que leurs versions ;
- les prérequis de configuration des éléments précédents, avec, le cas échéant, les procédures de paramétrage associées.

Il détaillera la liste des applications nécessaires à installer sur le poste de travail pour pouvoir utiliser correctement la solution.
Il détaillera dans son offre toutes les applications bureautiques, applications métiers ou éléments de configuration du système ou du navigateur du poste de travail susceptibles d'être incompatibles ou d'interférer avec la solution.

### 4.2. Prérequis réseau

Le titulaire décrira les prérequis et contraintes réseau nécessaires au bon fonctionnement de la solution, notamment :
- les débits réseau minimum et recommandé pour l'exploitation de la solution ;
- Les ouvertures de ports ou filtrages nécessaires

## 5. MISE EN ŒUVRE DE LA SOLUTION

Pour les prestations liées à la mise en œuvre de l'outil, le titulaire, proposera un prix forfaitaire dans son BPU.

### 5.1. Formation

Le Titulaire assurera sur site, la formation nécessaire aux gestionnaires et aux administrateurs. Les formations auront lieu dans les sièges des membres du groupement. Il n'est pas envisagé de dispenser des formations pour les éventuels demandeurs de ressources, d'où la nécessité d'une interface intuitive permettant une prise en main immédiate de la part des demandeurs de ressources.
Il proposera des experts ayant une expérience éprouvée de contact avec des utilisateurs.

Le Titulaire précisera, le cas échéant, les connaissances préalables requises et proposera des formations adaptées aux différents profils d'usager de la plateforme. Le groupement validera le plan de formation ainsi que l'organisation des formations proposées par le Titulaire.

Ce plan de formation devra mentionner :
- Les éventuels prérequis logistiques ou techniques nécessaires (salle de formation, configuration des postes...) ;
- Les contenus précis des modules.

Pour chaque formation, Le Titulaire procurera à la collectivité, un support de formation en français sur support informatique, au moins 4 jours ouvrables avant le début de la première séance. La détermination de l'effectif de chaque formation sera faite par le coordinateur.

### 5.2. Expertise

Le Titulaire assurera sur site, à la demande de la DSIM, les prestations suivantes :
- expertise,
- assistance,
- transfert de compétences,
- animation de réunions de pilotage ou techniques visant à faire les choix stratégiques pour la mise en place de la solution et pour optimiser son exploitation et améliorer le confort d'utilisation des logiciels.

Il proposera des experts ayant une expérience éprouvée de contact avec des utilisateurs finaux.

### 5.3. Planning

Pour la première phase de la mise en place, les deux organismes souhaitent commencer par la ressource « salles de réunion ». Concernant les ressources qui ne sont pas prises en compte par le logiciel de base de l'offre, le candidat indiquera le délai nécessaire pour mise à disposition de ces nouvelles ressources dans l'outil.

Le Titulaire détaillera les phases et le planning de mise en œuvre de la solution. Il détaillera la méthodologie projet et l'organisation retenue avec les directions et services pour implémenter la solution et la rendre opérationnelle.

Le Coordinateur proposera, sous deux semaines après la notification du marché, une réunion de lancement avec le groupe projet.
Lors de cette réunion de lancement, un planning plus précis sera mis en place pour définir les chantiers de travail proposés aux directions et services;

## 6. GARANTIE, MAINTENANCE ET GESTION DES INCIDENTS

### 6.1. Garantie et maintenance

La commande inclut la maintenance, qui sera gratuite pendant la période de vérification d'aptitude, de vérification de service régulier. La maintenance sera préventive, curative et évolutive.

Le Titulaire s'engage à maintenir l'application pendant la durée du marché. Cette prestation est incluse dans le présent marché. Elle concerne la maintenance corrective de l'application, la mise à disposition de nouvelles versions et l'assistance téléphonique.

Le groupement informera le titulaire des noms des personnes habilitées à faire appel à l'assistance téléphonique. Elles seront issues de la DSI pour les aspects techniques et seront limitées aux correspondants fonctionnels des deux organismes pour le volet fonctionnel.
Le Titulaire indiquera précisément les modalités de maintenance fonctionnelle et technique.

### 6.2. Gestion des incidents

En cas de d'interruption du Service pour cause de maintenance ou de mise à jour du Service, le Titulaire planifiera les interventions en commun accord avec le groupement.

L'assistance téléphonique ou Hotline devra être accessible au moins de 9h à 18h tous les jours ouvrables.
Il indiquera les modalités de contact de sa hotline fonctionnelle et technique et le type de demandes prises en compte. Il énoncera précisément ses heures ouvrées, les conditions de signalement d'incidents ainsi que leurs délais et modalités de résolution.

Les délais sur lesquels s'engagera le candidat ne devront pas dépasser ceux qui sont indiqués dans le tableau qui suit.

| Type d'incident | Délai de prise en charge | Délai de résolution |
|-----------------|--------------------------|---------------------|
| Bloquant (*) | 4 heures ouvrées de l'administration | 1 jour ouvré pour résolution ou contournement |
| Non bloquant (*) | 8 heures ouvrées de l'administration | 1 semaine calendrier |
| Exploitation d'une solution de contournement (*) | | 1 semaine calendrier |

(*)
Typologie des incidents.
Incident bloquant :
- incident ne permettant pas l'aboutissement d'une fonction nécessaire au bon fonctionnement de l'application ;
- résultats incohérents par rapport aux paramètres définis.

Incident non bloquant :
- arrêt d'un traitement sans préjudice majeur sur le résultat à obtenir ;
- arrêt ou incident ne remettant pas en cause la réalisation de la fonction.

Solution de contournement en exploitation :
Suite à un incident bloquant, le prestataire, ne pouvant pas le corriger dans les délais, installe une solution de contournement qui permet d'exploiter toutes les fonctionnalités de l'application, éventuellement en mode dégradé ou limité. La période pendant laquelle la solution de contournement est en exploitation est vue comme un incident dans la mesure où le problème source n'est pas corrigé.

Le non-respect des délais précisés dans l'offre du Titulaire, engendrera des pénalités qui s'appliqueront selon les modalités prévues dans le CCAG et le CCAP.

## 7. MODALITÉS ADMINISTRATIVES

### 7.1. Cadre de réponse

Les candidats trouveront avec le présent document, un cadre de réponse auquel ils devront se conformer pour présenter leur offre. Ce cadre de réponse a pour but de permettre une réponse formatée de la part des candidats afin de faciliter l'analyse des offres. Bien entendu, ce cadre ne constitue qu'un minimum de réponse et chaque candidat aura loisir de compléter celui-ci par toute information, ou descriptif qu'il jugera utile à la présentation de son offre.
Nous attirons toutefois l'attention des soumissionnaires sur l'importance de se conformer au minimum à ce cadre de réponse pour garantir une analyse objective de leur réponse.

Le cadre de réponse du présent marché se compose :
- Cadre de Réponse Technique et Fonctionnelle (CRTF)
- d'un Bordereau des Prix Unitaires (BPU) faisant office de Devis Quantitatif Estimatif (DQE)

La valeur financière de l'offre sera évaluée sur le DQE.

Document à signer par le candidat en y ajoutant date, nom et qualité du signataire.

*Fin du document*
