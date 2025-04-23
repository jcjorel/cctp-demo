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
# Dockerfile pour la construction de l'image du service frontend React du SRR.
# Ce fichier définit l'environnement d'exécution du frontend avec Node.js 18.
###############################################################################
# [Source file design principles]
# - Utiliser une image légère basée sur Node.js Alpine
# - Installer uniquement les dépendances nécessaires
# - Séparer les étapes d'installation des dépendances et de copie du code pour optimiser le cache
# - Exposer le port utilisé par l'application React
###############################################################################
# [Source file constraints]
# - L'image doit être compatible avec Docker Compose
# - Le répertoire de travail doit être /app
# - L'application doit être exposée sur le port 3000
###############################################################################
# [Dependencies]
# - services/frontend/package.json
###############################################################################
# [GenAI tool change history]
# 2025-04-23T09:44:50Z : Création initiale du Dockerfile frontend par CodeAssistant
# * Configuration de l'image Node.js 18
# * Installation des dépendances via npm ci
# * Configuration de l'environnement d'exécution React
###############################################################################

FROM node:18-alpine

WORKDIR /app

# Installation des dépendances
COPY package.json package-lock.json ./
RUN npm ci

# Copie du code source
COPY . .

# Exposition du port utilisé par l'application
EXPOSE 3000

# Commande par défaut pour lancer l'application en mode développement
CMD ["npm", "start"]
