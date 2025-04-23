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
# Tests d'intégration pour les endpoints API de gestion des ressources du système SRR.
# Ce fichier teste l'intégration complète entre l'API, les services et la base de données
# pour les opérations CRUD sur les ressources.
###############################################################################
# [Source file design principles]
# - Tests qui valident le flux complet de l'API jusqu'à la base de données
# - Vérification des réponses HTTP et des données retournées
# - Tests des autorisations et contrôles d'accès
# - Organisation par scénarios d'utilisation
###############################################################################
# [Source file constraints]
# - Utilise une base de données de test isolée
# - Chaque test doit réinitialiser les données qu'il modifie
# - Dépend des fixtures définies dans conftest.py
###############################################################################
# [Dependencies]
# - app/api/v1/endpoints/resources.py
# - app/services/resource_service.py
# - app/models/resource.py
# - app/models/resource_type.py
# - app/schemas/resource.py
# - app/core/security.py
# - tests/conftest.py
# - doc/API.md
###############################################################################
# [GenAI tool change history]
# 2025-04-23T12:44:00Z : Création initiale des tests d'intégration pour l'API des ressources par CodeAssistant
# * Implémentation des tests pour les opérations CRUD via l'API
# * Tests des contrôles d'accès administrateur/utilisateur
# * Tests des validations de données
###############################################################################

import pytest
import uuid
import json
from httpx import AsyncClient
from datetime import datetime

from app.core.security import create_access_token
from app.models.resource import Resource
from app.models.resource_type import ResourceType
from app.models.user import User
from app.main import app


class TestResourcesAPI:
    """
    [Class intent]
    Suite de tests d'intégration pour l'API de gestion des ressources.
    
    [Design principles]
    Tests d'intégration complets validant le comportement de l'API avec la base de données.
    
    [Implementation details]
    Utilise un client de test AsyncClient et une base de données réelle isolée.
    """

    @pytest.fixture
    async def test_resource_type(self, db_session):
        """
        [Class method intent]
        Crée un type de ressource de test dans la base de données.
        
        [Design principles]
        Données de test isolées pour chaque suite de tests.
        
        [Implementation details]
        Crée et persiste un objet ResourceType dans la base de données de test.
        """
        resource_type = ResourceType(
            name="Salle de réunion",
            description="Espace pour réunions",
            icon="meeting_room",
            color="#4285F4"
        )
        db_session.add(resource_type)
        await db_session.commit()
        await db_session.refresh(resource_type)
        yield resource_type
        
        # Nettoyage
        await db_session.delete(resource_type)
        await db_session.commit()

    @pytest.fixture
    async def test_resource(self, db_session, test_resource_type):
        """
        [Class method intent]
        Crée une ressource de test dans la base de données.
        
        [Design principles]
        Données de test isolées pour chaque suite de tests.
        
        [Implementation details]
        Crée et persiste un objet Resource lié à un ResourceType dans la base de données de test.
        """
        resource = Resource(
            name="Salle Neptune",
            description="Grande salle de réunion",
            resource_type_id=test_resource_type.id,
            location="Bâtiment A, 2ème étage",
            capacity=20,
            is_active=True,
            properties={"has_projector": True, "has_whiteboard": True}
        )
        db_session.add(resource)
        await db_session.commit()
        await db_session.refresh(resource)
        yield resource
        
        # Nettoyage
        await db_session.delete(resource)
        await db_session.commit()

    @pytest.fixture
    async def test_user(self, db_session):
        """
        [Class method intent]
        Crée un utilisateur standard de test dans la base de données.
        
        [Design principles]
        Utilisateur de test avec droits limités pour tester les contrôles d'accès.
        
        [Implementation details]
        Crée et persiste un objet User avec rôle standard dans la base de données de test.
        """
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="$2b$12$IKEQb00u5eZ5sJSPy1tRQuECdFy7RB0gfQApyYV/L78mZdemClnAS",  # 'password'
            is_active=True,
            is_admin=False,
            full_name="Test User",
            roles=["user"]
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        yield user
        
        # Nettoyage
        await db_session.delete(user)
        await db_session.commit()

    @pytest.fixture
    async def test_admin(self, db_session):
        """
        [Class method intent]
        Crée un utilisateur administrateur de test dans la base de données.
        
        [Design principles]
        Utilisateur de test avec droits d'administration pour tester les contrôles d'accès.
        
        [Implementation details]
        Crée et persiste un objet User avec rôle admin dans la base de données de test.
        """
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password="$2b$12$IKEQb00u5eZ5sJSPy1tRQuECdFy7RB0gfQApyYV/L78mZdemClnAS",  # 'password'
            is_active=True,
            is_admin=True,
            full_name="Admin User",
            roles=["admin", "user"]
        )
        db_session.add(admin)
        await db_session.commit()
        await db_session.refresh(admin)
        yield admin
        
        # Nettoyage
        await db_session.delete(admin)
        await db_session.commit()

    @pytest.fixture
    def user_token_headers(self, test_user):
        """
        [Class method intent]
        Fournit des en-têtes HTTP avec un token JWT pour un utilisateur standard.
        
        [Design principles]
        Facilite les tests authentifiés en tant qu'utilisateur standard.
        
        [Implementation details]
        Génère un token JWT valide pour l'utilisateur de test.
        """
        access_token = create_access_token(
            data={"sub": test_user.username, "roles": test_user.roles}
        )
        return {"Authorization": f"Bearer {access_token}"}

    @pytest.fixture
    def admin_token_headers(self, test_admin):
        """
        [Class method intent]
        Fournit des en-têtes HTTP avec un token JWT pour un administrateur.
        
        [Design principles]
        Facilite les tests authentifiés en tant qu'administrateur.
        
        [Implementation details]
        Génère un token JWT valide pour l'administrateur de test.
        """
        access_token = create_access_token(
            data={"sub": test_admin.username, "roles": test_admin.roles}
        )
        return {"Authorization": f"Bearer {access_token}"}

    @pytest.mark.asyncio
    async def test_get_resources_list_unauthenticated(self, client):
        """
        [Function intent]
        Vérifie que l'accès non authentifié à la liste des ressources est interdit.
        
        [Design principles]
        Test des règles de sécurité de base de l'API.
        
        [Implementation details]
        Appelle l'API sans token d'authentification et vérifie la réponse 401.
        """
        response = await client.get("/api/v1/resources/")
        assert response.status_code == 401
        assert "WWW-Authenticate" in response.headers

    @pytest.mark.asyncio
    async def test_get_resources_list_as_user(self, client, test_resource, user_token_headers):
        """
        [Function intent]
        Vérifie qu'un utilisateur authentifié peut accéder à la liste des ressources.
        
        [Design principles]
        Test du cas d'utilisation standard avec authentification correcte.
        
        [Implementation details]
        Appelle l'API avec un token utilisateur et vérifie la réponse et les données.
        """
        response = await client.get("/api/v1/resources/", headers=user_token_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1
        assert "pagination" in data
        
        # Vérifier que notre ressource de test est dans les résultats
        resource_ids = [resource["id"] for resource in data["data"]]
        assert str(test_resource.id) in resource_ids

    @pytest.mark.asyncio
    async def test_get_resource_by_id(self, client, test_resource, user_token_headers):
        """
        [Function intent]
        Vérifie qu'un utilisateur peut récupérer les détails d'une ressource spécifique.
        
        [Design principles]
        Test d'accès aux détails d'une entité spécifique via son identifiant.
        
        [Implementation details]
        Appelle l'API avec l'ID d'une ressource et vérifie les données retournées.
        """
        response = await client.get(f"/api/v1/resources/{test_resource.id}", headers=user_token_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_resource.id)
        assert data["name"] == test_resource.name
        assert data["capacity"] == test_resource.capacity
        assert data["location"] == test_resource.location
        
        # Vérifier que le type de ressource est inclus dans la réponse
        assert "resource_type" in data
        assert data["resource_type"]["name"] == "Salle de réunion"

    @pytest.mark.asyncio
    async def test_get_nonexistent_resource(self, client, user_token_headers):
        """
        [Function intent]
        Vérifie que la requête d'une ressource inexistante renvoie une erreur 404.
        
        [Design principles]
        Test de gestion des erreurs pour les ressources inexistantes.
        
        [Implementation details]
        Appelle l'API avec un ID inexistant et vérifie la réponse 404.
        """
        nonexistent_id = str(uuid.uuid4())
        response = await client.get(f"/api/v1/resources/{nonexistent_id}", headers=user_token_headers)
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_create_resource_as_admin(self, client, admin_token_headers, test_resource_type):
        """
        [Function intent]
        Vérifie qu'un administrateur peut créer une nouvelle ressource.
        
        [Design principles]
        Test de création d'entité avec authentification administrative.
        
        [Implementation details]
        Soumet une requête POST avec les données d'une nouvelle ressource et vérifie la création.
        """
        new_resource = {
            "name": "Nouvelle Salle",
            "description": "Salle pour tests d'intégration",
            "resource_type_id": str(test_resource_type.id),
            "location": "Bâtiment B, 3ème étage",
            "capacity": 15,
            "properties": {"has_projector": False, "has_whiteboard": True}
        }
        
        response = await client.post(
            "/api/v1/resources/",
            headers=admin_token_headers,
            json=new_resource
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == new_resource["name"]
        assert data["description"] == new_resource["description"]
        assert data["capacity"] == new_resource["capacity"]
        assert data["is_active"] == True  # Par défaut
        
        # Vérifier que l'ID a été généré
        assert "id" in data
        assert uuid.UUID(data["id"], version=4)

    @pytest.mark.asyncio
    async def test_create_resource_as_user(self, client, user_token_headers, test_resource_type):
        """
        [Function intent]
        Vérifie qu'un utilisateur standard ne peut pas créer de ressource (action admin).
        
        [Design principles]
        Test de contrôle d'accès basé sur les rôles.
        
        [Implementation details]
        Tente de créer une ressource avec un token utilisateur standard et vérifie le refus.
        """
        new_resource = {
            "name": "Salle Interdite",
            "resource_type_id": str(test_resource_type.id),
            "location": "Bâtiment C",
            "capacity": 10
        }
        
        response = await client.post(
            "/api/v1/resources/",
            headers=user_token_headers,
            json=new_resource
        )
        
        assert response.status_code == 403
        data = response.json()
        assert "detail" in data
        assert "permission" in data["detail"].lower() or "forbidden" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_update_resource_as_admin(self, client, test_resource, admin_token_headers):
        """
        [Function intent]
        Vérifie qu'un administrateur peut modifier une ressource existante.
        
        [Design principles]
        Test de mise à jour d'entité avec authentification administrative.
        
        [Implementation details]
        Soumet une requête PUT pour mettre à jour une ressource et vérifie les modifications.
        """
        update_data = {
            "name": "Salle Neptune - Mise à jour",
            "capacity": 25,
            "properties": {"has_projector": True, "has_whiteboard": True, "has_videoconf": True}
        }
        
        response = await client.put(
            f"/api/v1/resources/{test_resource.id}",
            headers=admin_token_headers,
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_resource.id)
        assert data["name"] == update_data["name"]
        assert data["capacity"] == update_data["capacity"]
        assert data["properties"]["has_videoconf"] == True
        
        # Vérifier que les champs non mentionnés n'ont pas changé
        assert data["description"] == test_resource.description
        assert data["location"] == test_resource.location

    @pytest.mark.asyncio
    async def test_delete_resource_as_admin(self, client, admin_token_headers, db_session):
        """
        [Function intent]
        Vérifie qu'un administrateur peut supprimer une ressource.
        
        [Design principles]
        Test de suppression d'entité avec authentification administrative.
        
        [Implementation details]
        Crée une ressource temporaire, puis la supprime via l'API et vérifie la suppression.
        """
        # Créer une ressource temporaire pour la supprimer
        resource_type = await db_session.query(ResourceType).first()
        temp_resource = Resource(
            name="Ressource Temporaire",
            description="À supprimer",
            resource_type_id=resource_type.id,
            location="Temporaire",
            capacity=5,
            is_active=True
        )
        db_session.add(temp_resource)
        await db_session.commit()
        await db_session.refresh(temp_resource)
        resource_id = temp_resource.id
        
        # Supprimer la ressource
        response = await client.delete(
            f"/api/v1/resources/{resource_id}",
            headers=admin_token_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        
        # Vérifier que la ressource n'existe plus
        check_response = await client.get(
            f"/api/v1/resources/{resource_id}",
            headers=admin_token_headers
        )
        assert check_response.status_code == 404

    @pytest.mark.asyncio
    async def test_search_resources(self, client, test_resource, test_resource_type, user_token_headers, db_session):
        """
        [Function intent]
        Vérifie que la recherche de ressources avec filtres fonctionne correctement.
        
        [Design principles]
        Test des capacités de recherche et filtrage de l'API.
        
        [Implementation details]
        Crée plusieurs ressources avec différentes caractéristiques puis effectue des recherches ciblées.
        """
        # Créer une deuxième ressource pour les tests de recherche
        second_resource = Resource(
            name="Salle Mars",
            description="Petite salle de réunion",
            resource_type_id=test_resource_type.id,
            location="Bâtiment A, 1er étage",
            capacity=8,
            is_active=True,
            properties={"has_projector": False}
        )
        db_session.add(second_resource)
        await db_session.commit()
        
        try:
            # Test 1: Recherche par type de ressource
            response = await client.get(
                f"/api/v1/resources/search?resource_type_id={test_resource_type.id}",
                headers=user_token_headers
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "data" in data
            assert len(data["data"]) >= 2
            
            # Test 2: Recherche par capacité minimale
            response = await client.get(
                "/api/v1/resources/search?capacity_min=15",
                headers=user_token_headers
            )
            
            assert response.status_code == 200
            data = response.json()
            resource_names = [r["name"] for r in data["data"]]
            assert "Salle Neptune" in resource_names
            assert "Salle Mars" not in resource_names
            
            # Test 3: Recherche par nom
            response = await client.get(
                "/api/v1/resources/search?name=Mars",
                headers=user_token_headers
            )
            
            assert response.status_code == 200
            data = response.json()
            resource_names = [r["name"] for r in data["data"]]
            assert "Salle Mars" in resource_names
            assert "Salle Neptune" not in resource_names
            
        finally:
            # Nettoyage
            await db_session.delete(second_resource)
            await db_session.commit()
