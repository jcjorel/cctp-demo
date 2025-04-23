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
# Centralise tous les routers de l'API v1 en un point unique d'inclusion.
# Ce fichier aggège les différents endpoints organisés par domaine fonctionnel,
# facilitant l'inclusion de l'ensemble de l'API dans l'application principale.
###############################################################################
# [Source file design principles]
# - Organisation modulaire des endpoints par domaine
# - Séparation claire des préoccupations
# - Facilitation de l'extension de l'API
# - Structure claire et prévisible des URLs
# - Documentation adaptée à chaque groupe d'endpoints
###############################################################################
# [Source file constraints]
# - Ne pas contenir de logique métier
# - Maintenir la cohérence des tags des endpoints
# - Assurer que les préfixes d'URLs sont cohérents et conformes aux conventions REST
###############################################################################
# [Dependencies]
# - fastapi: APIRouter
# - app/api/v1/endpoints/ modules: routers spécifiques aux domaines
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:11:30Z : Création initiale du router principal de l'API v1 par CodeAssistant
# * Configuration du router principal
# * Inclusion des placeholders pour les endpoints par domaine
###############################################################################

from fastapi import APIRouter

# Import des routers des différents domaines fonctionnels
# Ces imports seront décommentés au fur et à mesure de l'implémentation des endpoints
from app.api.v1.endpoints import auth
# from app.api.v1.endpoints import resources, bookings

# Router principal qui agrège tous les sous-routers
api_router = APIRouter()

# Inclusion des routers spécifiques avec leurs préfixes et tags
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
# api_router.include_router(resources.router, prefix="/resources", tags=["resources"])
# api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])

# Ce router sera progressivement enrichi avec les fonctionnalités
# au fur et à mesure de leur implémentation
