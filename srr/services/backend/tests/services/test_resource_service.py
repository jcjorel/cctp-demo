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
# Tests unitaires pour le service de gestion des ressources du système SRR.
# Ce fichier valide le comportement du service de ressources en isolation,
# en testant les différentes fonctionnalités de CRUD et règles métier.
###############################################################################
# [Source file design principles]
# - Tests isolés utilisant des mocks pour les dépendances externes
# - Structure Arrange-Act-Assert pour la clarté des tests
# - Couverture complète des cas normaux et cas d'erreur
# - Vérifications explicites des comportements attendus
###############################################################################
# [Source file constraints]
# - Ne doit pas dépendre d'une base de données réelle
# - Les tests doivent être déterministes et reproductibles
# - Chaque test doit être indépendant des autres
###############################################################################
# [Dependencies]
# - app/services/resource_type_service.py
# - app/models/resource.py
# - app/models/resource_type.py
# - app/schemas/resource.py
# - doc/DATA_MODEL.md
###############################################################################
# [GenAI tool change history]
# 2025-04-23T12:43:00Z : Création initiale des tests unitaires pour le service de ressources par CodeAssistant
# * Implémentation des tests pour les opérations CRUD
# * Tests des cas d'erreur et validations
# * Mock des dépendances externes
###############################################################################

import pytest
import uuid
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock

from app.services.resource_service import ResourceService
from app.models.resource import Resource
from app.models.resource_type import ResourceType
from app.schemas.resource import ResourceCreate, ResourceUpdate


class TestResourceService:
    """
    [Class intent]
    Suite de tests unitaires pour valider le comportement du service de ressources.
    
    [Design principles]
    Tests isolés avec mocks pour toutes les dépendances externes.
    Organisation claire des tests par fonctionnalité.
    
    [Implementation details]
    Mock du repository et des dépendances pour tester le service en isolation.
    """

    @pytest.fixture
    def resource_repository(self):
        """
        [Class method intent]
        Crée un mock du repository de ressources pour les tests.
        
        [Design principles]
        Centralisation de la création des mocks pour assurer la cohérence.
        
        [Implementation details]
        Utilise AsyncMock pour simuler les méthodes asynchrones du repository.
        """
        return AsyncMock()

    @pytest.fixture
    def resource_service(self, resource_repository):
        """
        [Class method intent]
        Crée une instance du service de ressources avec des dépendances mockées.
        
        [Design principles]
        Service isolé pour tests unitaires avec dépendances injectées.
        
        [Implementation details]
        Instancie le service avec le repository mocké.
        """
        return ResourceService(repository=resource_repository)

    @pytest.fixture
    def sample_resource(self):
        """
        [Class method intent]
        Fournit un exemple de ressource pour les tests.
        
        [Design principles]
        Données de test cohérentes et réutilisables.
        
        [Implementation details]
        Crée un objet Resource avec des valeurs de test représentatives.
        """
        resource_type = ResourceType(
            id=str(uuid.uuid4()),
            name="Salle de réunion",
            description="Espace pour réunions",
            icon="meeting_room",
            color="#4285F4"
        )
        
        return Resource(
            id=str(uuid.uuid4()),
            name="Salle Neptune",
            description="Grande salle de réunion",
            resource_type_id=resource_type.id,
            resource_type=resource_type,
            location="Bâtiment A, 2ème étage",
            capacity=20,
            is_active=True,
            properties={"has_projector": True, "has_whiteboard": True},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    @pytest.mark.asyncio
    async def test_get_resource_by_id_found(self, resource_service, resource_repository, sample_resource):
        """
        [Function intent]
        Vérifie que la méthode get_by_id retourne correctement une ressource lorsqu'elle existe.
        
        [Design principles]
        Test du cas nominal avec vérification explicite du résultat.
        
        [Implementation details]
        Configure le mock du repository pour retourner une ressource spécifique et vérifie le retour.
        """
        # Arrange
        resource_id = sample_resource.id
        resource_repository.get.return_value = sample_resource
        
        # Act
        result = await resource_service.get_by_id(resource_id)
        
        # Assert
        resource_repository.get.assert_called_once_with(resource_id)
        assert result == sample_resource
        assert result.name == "Salle Neptune"
        assert result.capacity == 20

    @pytest.mark.asyncio
    async def test_get_resource_by_id_not_found(self, resource_service, resource_repository):
        """
        [Function intent]
        Vérifie que la méthode get_by_id retourne None lorsque la ressource n'existe pas.
        
        [Design principles]
        Test du cas d'erreur avec vérification explicite du résultat.
        
        [Implementation details]
        Configure le mock du repository pour retourner None et vérifie le comportement.
        """
        # Arrange
        resource_id = str(uuid.uuid4())
        resource_repository.get.return_value = None
        
        # Act
        result = await resource_service.get_by_id(resource_id)
        
        # Assert
        resource_repository.get.assert_called_once_with(resource_id)
        assert result is None

    @pytest.mark.asyncio
    async def test_create_resource(self, resource_service, resource_repository, sample_resource):
        """
        [Function intent]
        Vérifie que la méthode create crée correctement une nouvelle ressource.
        
        [Design principles]
        Test de création avec vérification des données transmises au repository.
        
        [Implementation details]
        Crée un objet ResourceCreate, simule la création et vérifie les appels et le résultat.
        """
        # Arrange
        resource_data = ResourceCreate(
            name="Nouvelle Salle",
            description="Salle pour tests",
            resource_type_id=str(uuid.uuid4()),
            location="Bâtiment B",
            capacity=15,
            properties={"has_projector": False}
        )
        resource_repository.create.return_value = Resource(
            id=str(uuid.uuid4()),
            **resource_data.dict(),
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Act
        result = await resource_service.create(resource_data)
        
        # Assert
        resource_repository.create.assert_called_once()
        assert result.name == resource_data.name
        assert result.description == resource_data.description
        assert result.capacity == resource_data.capacity
        assert result.is_active == True

    @pytest.mark.asyncio
    async def test_update_resource(self, resource_service, resource_repository, sample_resource):
        """
        [Function intent]
        Vérifie que la méthode update met à jour correctement une ressource existante.
        
        [Design principles]
        Test de mise à jour avec vérification des modifications appliquées.
        
        [Implementation details]
        Crée un objet ResourceUpdate, simule la mise à jour et vérifie les changements.
        """
        # Arrange
        resource_id = sample_resource.id
        update_data = ResourceUpdate(
            name="Salle Neptune - Rénovée",
            capacity=25
        )
        
        # Simuler que la ressource existe
        resource_repository.get.return_value = sample_resource
        
        # Simuler la mise à jour
        updated_resource = Resource(
            **sample_resource.__dict__,
            name=update_data.name,
            capacity=update_data.capacity,
            updated_at=datetime.now()
        )
        resource_repository.update.return_value = updated_resource
        
        # Act
        result = await resource_service.update(resource_id, update_data)
        
        # Assert
        resource_repository.get.assert_called_once_with(resource_id)
        resource_repository.update.assert_called_once()
        assert result.name == update_data.name
        assert result.capacity == update_data.capacity
        # Vérifier que les autres champs n'ont pas changé
        assert result.description == sample_resource.description
        assert result.is_active == sample_resource.is_active

    @pytest.mark.asyncio
    async def test_update_nonexistent_resource(self, resource_service, resource_repository):
        """
        [Function intent]
        Vérifie que la méthode update renvoie None lorsque la ressource à mettre à jour n'existe pas.
        
        [Design principles]
        Test de cas d'erreur avec vérification explicite du comportement.
        
        [Implementation details]
        Configure le mock pour simuler une ressource inexistante et vérifie le retour.
        """
        # Arrange
        resource_id = str(uuid.uuid4())
        update_data = ResourceUpdate(name="Nouvelle Salle")
        resource_repository.get.return_value = None
        
        # Act
        result = await resource_service.update(resource_id, update_data)
        
        # Assert
        resource_repository.get.assert_called_once_with(resource_id)
        resource_repository.update.assert_not_called()
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_resource(self, resource_service, resource_repository, sample_resource):
        """
        [Function intent]
        Vérifie que la méthode delete supprime correctement une ressource existante.
        
        [Design principles]
        Test de suppression avec vérification du comportement et du retour.
        
        [Implementation details]
        Simule la suppression d'une ressource existante et vérifie le résultat.
        """
        # Arrange
        resource_id = sample_resource.id
        resource_repository.get.return_value = sample_resource
        resource_repository.delete.return_value = True
        
        # Act
        result = await resource_service.delete(resource_id)
        
        # Assert
        resource_repository.get.assert_called_once_with(resource_id)
        resource_repository.delete.assert_called_once_with(resource_id)
        assert result == True

    @pytest.mark.asyncio
    async def test_delete_nonexistent_resource(self, resource_service, resource_repository):
        """
        [Function intent]
        Vérifie que la méthode delete renvoie False lorsque la ressource à supprimer n'existe pas.
        
        [Design principles]
        Test de cas d'erreur avec vérification explicite du comportement.
        
        [Implementation details]
        Configure le mock pour simuler une ressource inexistante et vérifie le retour.
        """
        # Arrange
        resource_id = str(uuid.uuid4())
        resource_repository.get.return_value = None
        
        # Act
        result = await resource_service.delete(resource_id)
        
        # Assert
        resource_repository.get.assert_called_once_with(resource_id)
        resource_repository.delete.assert_not_called()
        assert result == False

    @pytest.mark.asyncio
    async def test_get_all_resources(self, resource_service, resource_repository, sample_resource):
        """
        [Function intent]
        Vérifie que la méthode get_all retourne correctement la liste des ressources.
        
        [Design principles]
        Test de récupération de liste avec pagination.
        
        [Implementation details]
        Configure le mock pour retourner une liste de ressources et vérifie le comportement.
        """
        # Arrange
        resources = [sample_resource, Resource(
            id=str(uuid.uuid4()),
            name="Salle Mars",
            description="Petite salle de réunion",
            resource_type_id=sample_resource.resource_type_id,
            resource_type=sample_resource.resource_type,
            location="Bâtiment A, 1er étage",
            capacity=8,
            is_active=True,
            properties={"has_projector": False, "has_whiteboard": True},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )]
        resource_repository.get_all.return_value = (resources, 2)
        
        # Act
        result, count = await resource_service.get_all(skip=0, limit=10)
        
        # Assert
        resource_repository.get_all.assert_called_once_with(skip=0, limit=10)
        assert len(result) == 2
        assert count == 2
        assert result[0].name == "Salle Neptune"
        assert result[1].name == "Salle Mars"

    @pytest.mark.asyncio
    async def test_search_resources(self, resource_service, resource_repository, sample_resource):
        """
        [Function intent]
        Vérifie que la méthode search filtre correctement les ressources selon les critères.
        
        [Design principles]
        Test de recherche avec filtres multiples.
        
        [Implementation details]
        Configure le mock pour retourner des résultats filtrés et vérifie le comportement.
        """
        # Arrange
        filters = {
            "resource_type_id": sample_resource.resource_type_id,
            "capacity_min": 15,
            "is_active": True
        }
        resource_repository.search.return_value = ([sample_resource], 1)
        
        # Act
        result, count = await resource_service.search(**filters)
        
        # Assert
        resource_repository.search.assert_called_once_with(**filters)
        assert len(result) == 1
        assert count == 1
        assert result[0].name == "Salle Neptune"
        assert result[0].capacity >= filters["capacity_min"]
