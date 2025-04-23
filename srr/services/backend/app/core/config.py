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
# Gère la configuration de l'application via variables d'environnement et valeurs par défaut.
# Ce module centralise tous les paramètres configurables du backend, facilitant le déploiement
# dans différents environnements (développement, test, production) via les variables d'environnement.
###############################################################################
# [Source file design principles]
# - Utilisation de Pydantic pour la validation des variables d'environnement
# - Valeurs par défaut sécurisées pour le développement
# - Organisation claire des paramètres par catégories (sécurité, base de données, etc.)
# - Point unique de configuration pour toute l'application
# - Hiérarchie de priorité: variables système > .env > valeurs par défaut
###############################################################################
# [Source file constraints]
# - Certains paramètres sensibles ne devraient jamais être définis en dur dans ce fichier
# - Toutes les valeurs par défaut doivent être appropriées pour un environnement de développement
# - Les valeurs par défaut ne doivent pas être utilisées en production
###############################################################################
# [Dependencies]
# - pydantic-settings
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:06:00Z : Création initiale du fichier de configuration par CodeAssistant
# * Définition de la classe Settings basée sur BaseSettings de Pydantic
# * Configuration des paramètres d'API, de sécurité, de base de données et de Redis
# * Paramètres spécifiques à l'environnement de développement
###############################################################################

from pydantic_settings import BaseSettings
import secrets
from typing import List, Optional, Union, Dict, Any


class Settings(BaseSettings):
    """
    [Class intent]
    Gère la configuration de l'application via variables d'environnement et valeurs par défaut.
    
    [Design principles]
    Utilisation de Pydantic pour la validation des variables d'environnement.
    Valeurs par défaut sécurisées pour le développement.
    
    [Implementation details]
    Les variables sont lues depuis .env ou variables d'environnement système.
    Utilisation de hiérarchie de priorité: variables système > .env > valeurs par défaut.
    """
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Système de Réservation de Ressources"
    
    # SECURITY
    SECRET_KEY: str = secrets.token_urlsafe(32)
    REFRESH_TOKEN_SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080", "http://localhost"]
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@postgres:5432/srr_dev"
    DATABASE_MAX_CONNECTIONS: int = 32
    DATABASE_CONNECT_RETRY: int = 3
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_CACHE_EXPIRE_IN_SECONDS: int = 60 * 5  # 5 minutes
    
    # Mock Settings
    MOCK_AUTH: bool = True
    MOCK_EXCHANGE: bool = True
    MOCK_USERS_FILE: Optional[str] = "/app/data/users.json"
    MOCK_RESOURCES_FILE: Optional[str] = "/app/data/resources.json"
    
    # Environment
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Logging
    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"


# Instance singleton de Settings
settings = Settings()
