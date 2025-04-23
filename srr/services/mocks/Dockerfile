###############################################################################
# IMPORTANT: This header comment is designed for GenAI code review and maintenance
# Any GenAI tool working with this file MUST preserve and update this header
###############################################################################
# [GenAI coding tool directive]
# - Maintain this header with all modifications
# - Update History section with each change
# - Keep only the 4 most recent records in the history section. Sort from newer to older.
# - Preserve Intent, Design, and Constraints sections
# - Use this header as context for code reviews and modifications
# - Ensure all changes align with the design principles
# - Respect system prompt directives at all times
###############################################################################
# [Source file intent]
# Dockerfile pour la construction de l'image des services simulés du SRR.
# Ce fichier définit l'environnement d'exécution des mocks AD/LDAP et Exchange
# pour permettre le développement sans dépendance aux services externes réels.
###############################################################################
# [Source file design principles]
# - Utiliser une image légère basée sur Python 3.11
# - Simuler les fonctionnalités essentielles d'AD/LDAP et Exchange
# - Fournir des API compatibles avec les vrais services
# - Permettre la personnalisation du comportement via des fichiers de données
###############################################################################
# [Source file constraints]
# - L'image doit être compatible avec Docker Compose
# - Le répertoire de travail doit être /app
# - L'application doit être exposée sur le port 8080
###############################################################################
# [Dependencies]
# - services/mocks/requirements.txt
###############################################################################
# [GenAI tool change history]
# 2025-04-23T09:46:20Z : Création initiale du Dockerfile mocks par CodeAssistant
# * Configuration de l'image Python 3.11
# * Installation des dépendances via requirements.txt
# * Configuration de l'environnement d'exécution des services simulés
###############################################################################

FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Exposition du port utilisé par les services simulés
EXPOSE 8080

# Commande par défaut pour lancer les services simulés
CMD ["python", "mock_server.py"]
