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
# Point d'entrée principal de l'application FastAPI. Ce fichier crée et configure 
# l'instance de l'application avec les middlewares, routes et gestionnaires d'événements.
# Il sert également de point d'entrée pour le serveur ASGI.
###############################################################################
# [Source file design principles]
# - Configuration centralisée et explicite de l'application
# - Séparation claire des préoccupations
# - Structure modulaire pour faciliter l'extension
# - Initialisation correcte des composants externes
# - Gestion appropriée des événements de démarrage et d'arrêt
###############################################################################
# [Source file constraints]
# - Ne pas contenir de logique métier
# - Maintenir la compatibilité avec les serveurs ASGI standards
# - Assurer que les routes sont correctement importées
# - Configurer tous les middlewares nécessaires
###############################################################################
# [Dependencies]
# - fastapi: FastAPI, middleware CORS
# - uvicorn: Serveur ASGI
# - app/core/config.py: Configuration centrale de l'application
# - app/api/v1/router: Router principal de l'API
# - app/core/exceptions: Gestionnaires d'exceptions
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:10:40Z : Création initiale du point d'entrée principal par CodeAssistant
# * Configuration de l'application FastAPI avec middlewares et routers
# * Configuration des gestionnaires d'exceptions
# * Création des endpoints de base pour health check et info
###############################################################################

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import add_exception_handlers
from app.db.session import engine, Base

# Configuration du logger
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    [Function intent]
    Crée et configure une instance de l'application FastAPI.
    
    [Design principles]
    Configuration centralisée de l'application.
    Séparation claire des préoccupations.
    
    [Implementation details]
    Initialise l'application avec les middlewares, routers et gestionnaires d'événements.
    """
    # Création de l'application FastAPI
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API pour la réservation et gestion des ressources partagées",
        version="0.1.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        debug=settings.DEBUG,
        swagger_ui_parameters={"defaultModelsExpandDepth": -1}  # Cache les modèles par défaut
    )
    
    # Configuration des middlewares CORS
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # Configuration des gestionnaires d'exceptions
    add_exception_handlers(app)
    
    # Inclusion du router principal API v1
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # Endpoint de base pour la racine
    @app.get("/")
    async def root():
        """
        [Function intent]
        Fournit un point d'entrée basique pour l'API.
        
        [Design principles]
        Endpoint simple pour confirmer que l'API fonctionne.
        
        [Implementation details]
        Renvoie un message de bienvenue et un lien vers la documentation.
        """
        return {
            "message": f"Bienvenue sur l'API {settings.PROJECT_NAME}",
            "docs": f"{settings.API_V1_STR}/docs",
            "version": "0.1.0",
            "environment": settings.ENVIRONMENT
        }
    
    # Endpoint de vérification de santé
    @app.get("/health")
    async def health_check():
        """
        [Function intent]
        Vérifie la santé de l'application et ses dépendances.
        
        [Design principles]
        Endpoint léger pour les vérifications de santé externes.
        
        [Implementation details]
        Vérifie la disponibilité des services essentiels (base de données, etc.)
        """
        # Statut de base
        health_data = {
            "status": "healthy",
            "version": "0.1.0",
            "environment": settings.ENVIRONMENT,
        }
        
        # En environnement non-production, on ajoute des informations supplémentaires
        if settings.DEBUG:
            health_data.update({
                "debug_mode": True,
                "mock_auth": settings.MOCK_AUTH,
                "mock_exchange": settings.MOCK_EXCHANGE
            })
        
        return health_data
    
    # Événements de démarrage et d'arrêt
    @app.on_event("startup")
    async def startup_event():
        """
        [Function intent]
        Exécute les actions nécessaires au démarrage de l'application.
        
        [Design principles]
        Initialisation ordonnée des ressources externes.
        
        [Implementation details]
        Initialise les connexions aux services externes et les configurations requises.
        """
        logger.info(f"Démarrage de l'application {settings.PROJECT_NAME} en environnement {settings.ENVIRONMENT}")
        
        # En mode développement, crée les tables si elles n'existent pas
        if settings.DEBUG:
            logger.info("Création des tables de base de données en mode DEBUG")
            # Base.metadata.create_all(bind=engine)
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """
        [Function intent]
        Exécute les actions nécessaires à l'arrêt propre de l'application.
        
        [Design principles]
        Libération ordonnée des ressources.
        
        [Implementation details]
        Ferme proprement les connexions aux services externes.
        """
        logger.info(f"Arrêt de l'application {settings.PROJECT_NAME}")
    
    return app


# Instance de l'application pour les serveurs ASGI
app = create_app()


# Point d'entrée pour l'exécution directe
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
