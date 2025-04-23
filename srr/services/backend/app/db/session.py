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
# Configure la connexion à la base de données PostgreSQL et fournit les utilitaires
# de session SQLAlchemy. Ce module centralise la gestion des connexions à la base
# de données pour toute l'application.
###############################################################################
# [Source file design principles]
# - Séparation de la configuration de connexion et de l'utilisation
# - Utilisation d'un pool de connexions pour optimiser les performances
# - Configuration centralisée via les paramètres d'environnement
# - Gestion appropriée des ressources de base de données
# - Facilitation des tests avec possibilité d'injection de dépendances
###############################################################################
# [Source file constraints]
# - Le moteur de base de données doit être configurable
# - La session doit être thread-safe
# - Utilisation de la configuration centrale pour les paramètres
# - Pas de logique métier dans ce module
###############################################################################
# [Dependencies]
# - app/core/config.py: Configuration centrale de l'application
# - sqlalchemy: Bibliothèque ORM pour la base de données
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:08:20Z : Création initiale du module de session DB par CodeAssistant
# * Configuration de l'engine SQLAlchemy avec paramètres de pool
# * Création du SessionLocal pour les sessions de base de données
# * Définition de la classe Base pour les modèles
###############################################################################

import logging
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Configuration du logger
logger = logging.getLogger(__name__)

# Création de l'engine SQLAlchemy avec configuration de pool
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Vérifie la connexion avant utilisation
    pool_recycle=300,    # Recycle les connexions après 5 minutes
    pool_size=settings.DATABASE_MAX_CONNECTIONS,
    max_overflow=10,     # Permet 10 connexions supplémentaires au-delà de pool_size
    echo=settings.DEBUG, # Log SQL en mode debug
    connect_args={} if 'sqlite' not in settings.DATABASE_URL else {"check_same_thread": False}
)

# Création de la session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base déclarative pour les modèles
Base = declarative_base()

# Logging des opérations SQL en mode debug
if settings.DEBUG:
    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(event.get_current_time())

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = event.get_current_time() - conn.info['query_start_time'].pop(-1)
        logger.debug(f"SQL temps d'exécution: {total:.3f}s - {statement}")


def get_db() -> Generator:
    """
    [Function intent]
    Fournit une session de base de données et assure sa fermeture après utilisation.
    
    [Design principles]
    Pattern Unit-of-Work pour isolation des transactions.
    Gestion des ressources via générateur Python.
    
    [Implementation details]
    Utilisation du contexte Python pour garantir la fermeture de session.
    Implémentée comme un générateur pour l'injection de dépendances FastAPI.
    
    Yields:
        Session: Session SQLAlchemy pour interagir avec la base de données
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
