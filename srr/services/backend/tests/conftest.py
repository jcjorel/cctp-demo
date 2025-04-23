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
# Configuration du framework de test pour les tests unitaires et d'intégration du backend SRR.
# Ce fichier définit les fixtures Pytest communes pour tous les tests backend, permettant
# l'isolation et la réutilisation des composants de test.
###############################################################################
# [Source file design principles]
# - Centralisation des fixtures communes pour maximiser la réutilisation
# - Isolation des tests pour garantir qu'ils n'interfèrent pas entre eux
# - Séparation claire des fixtures unitaires et d'intégration
# - Utilisation de mocks pour isoler les composants dans les tests unitaires
###############################################################################
# [Source file constraints]
# - Doit prendre en charge les tests asynchrones pour FastAPI
# - Doit fournir des fixtures pour les sessions de base de données isolées
# - Doit supporter les tests en parallèle sans interférence
###############################################################################
# [Dependencies]
# - app/db/base.py
# - app/core/config.py
# - app/models/*
# - doc/DESIGN.md
# - doc/DATA_MODEL.md
###############################################################################
# [GenAI tool change history]
# 2025-04-23T12:42:00Z : Création initiale du fichier de configuration de tests par CodeAssistant
# * Implémentation des fixtures pour les tests unitaires et d'intégration
# * Configuration de la base de données de test
# * Configuration des mocks pour l'authentification
###############################################################################

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db.base import Base
from app.core.config import settings
from app.db.session import get_db
from app.main import app


# ---------------------------------- #
# Fixtures globales pour tous tests  #
# ---------------------------------- #

@pytest.fixture(scope="session")
def event_loop():
    """
    [Function intent]
    Fournit une boucle d'événements asyncio pour les tests asynchrones.
    
    [Design principles]
    Utilisation d'une seule boucle d'événements pour tous les tests afin de maximiser la performance.
    
    [Implementation details]
    Crée et partage une boucle d'événements au niveau de la session de test.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ---------------------------------- #
# Fixtures pour tests unitaires      #
# ---------------------------------- #

@pytest.fixture
def mock_db_session():
    """
    [Function intent]
    Fournit une session de base de données simulée pour les tests unitaires.
    
    [Design principles]
    Isolation complète des tests de la base de données réelle pour les tests unitaires.
    
    [Implementation details]
    Utilise AsyncMock pour simuler les opérations asynchrones de la base de données.
    """
    return AsyncMock()


@pytest.fixture
def mock_user():
    """
    [Function intent]
    Fournit un utilisateur simulé pour les tests d'authentification.
    
    [Design principles]
    Simulation cohérente des utilisateurs à travers les tests.
    
    [Implementation details]
    Crée un objet mock avec les attributs nécessaires pour l'authentification.
    """
    return Mock(
        id=str(uuid.uuid4()),
        username="testuser",
        email="test@example.com",
        roles=["user"],
        is_active=True,
        is_admin=False
    )


@pytest.fixture
def mock_admin_user():
    """
    [Function intent]
    Fournit un utilisateur administrateur simulé pour les tests nécessitant des privilèges élevés.
    
    [Design principles]
    Simulation cohérente des administrateurs à travers les tests.
    
    [Implementation details]
    Crée un objet mock avec les attributs nécessaires pour un administrateur.
    """
    return Mock(
        id=str(uuid.uuid4()),
        username="admin",
        email="admin@example.com",
        roles=["admin", "user"],
        is_active=True,
        is_admin=True
    )


# ---------------------------------- #
# Fixtures pour tests d'intégration  #
# ---------------------------------- #

# Base de données de test
TEST_DATABASE_URL = settings.DATABASE_URL.replace("/srr", "/srr_test")
engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="session")
async def setup_db():
    """
    [Function intent]
    Configure et prépare la base de données pour les tests d'intégration.
    
    [Design principles]
    Base de données isolée et propre pour chaque session de tests.
    
    [Implementation details]
    Crée le schéma, exécute les tests, puis nettoie la base de données.
    """
    # Création des tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Nettoyage
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(setup_db):
    """
    [Function intent]
    Fournit une session de base de données pour les tests d'intégration.
    
    [Design principles]
    Session de base de données isolée pour chaque test.
    
    [Implementation details]
    Utilise une transaction qui est annulée après chaque test pour garantir l'isolation.
    """
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
def client(db_session):
    """
    [Function intent]
    Fournit un client de test FastAPI avec une session de base de données injectée.
    
    [Design principles]
    Client de test isolé pour chaque test avec les dépendances substituées.
    
    [Implementation details]
    Remplace la dépendance get_db par une session de test dédiée.
    """
    async def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}
