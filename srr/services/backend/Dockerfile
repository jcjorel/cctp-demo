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
# Dockerfile pour la construction de l'image du service backend FastAPI du SRR.
# Ce fichier définit l'environnement d'exécution du backend avec Python 3.11.
###############################################################################
# [Source file design principles]
# - Utiliser une image légère basée sur Python 3.11
# - Installer uniquement les dépendances nécessaires pour l'exécution
# - Séparer les étapes d'installation des dépendances et de copie du code pour optimiser le cache
# - Exposer le port utilisé par l'application FastAPI
###############################################################################
# [Source file constraints]
# - L'image doit être compatible avec Docker Compose
# - Le répertoire de travail doit être /app
# - L'application doit être exposée sur le port 8000
###############################################################################
# [Dependencies]
# - services/backend/requirements.txt
###############################################################################
# [GenAI tool change history]
# 2025-04-23T09:43:00Z : Création initiale du Dockerfile backend par CodeAssistant
# * Configuration de l'image Python 3.11
# * Installation des dépendances via requirements.txt
# * Configuration de l'environnement d'exécution FastAPI
###############################################################################

FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Exposition du port utilisé par l'application
EXPOSE 8000

# Commande par défaut pour lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
