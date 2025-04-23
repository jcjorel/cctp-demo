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
# Endpoints API pour la gestion des types de ressources du SRR.
# Ce fichier définit les routes REST permettant de lister, créer,
# modifier et supprimer des types de ressources dans le système.
###############################################################################
# [Source file design principles]
# - Architecture REST respectant les conventions HTTP
# - Séparation de la logique de routage et de la logique métier
# - Validation des entrées via schémas Pydantic
# - Documentation OpenAPI/Swagger complète
###############################################################################
# [Source file constraints]
# - Ne pas contenir de logique métier complexe (déléguer aux services)
# - Respecter les statuts HTTP appropriés pour chaque opération
# - Assurer la cohérence de la sécurisation des endpoints
###############################################################################
# [Dependencies]
# - fastapi: APIRouter, Depends, HTTPException, status
# - sqlalchemy.orm: Session
# - app.api.deps: get_db, get_current_user, get_current_active_superuser
# - app.services.resource_type_service: ResourceTypeService
# - app.schemas.resource_type: ResourceType, ResourceTypeCreate, ResourceTypeUpdate
###############################################################################
# [GenAI tool change history]
# 2025-04-23T12:18:02Z : Création initiale des endpoints API pour les types de ressources par CodeAssistant
# * Implémentation des routes CRUD (GET, POST, PUT, DELETE)
# * Ajout de la gestion des permissions et de la documentation
###############################################################################

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api import deps
from app.models.user import User
from app.schemas.resource_type import ResourceType, ResourceTypeCreate, ResourceTypeUpdate
from app.services.resource_type_service import ResourceTypeService

router = APIRouter()


@router.get("/", response_model=List[ResourceType])
def get_resource_types(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    [Function intent]
    Récupère la liste des types de ressources avec pagination.
    
    [Design principles]
    Endpoint public accessible à tous les utilisateurs authentifiés.
    
    [Implementation details]
    Délègue la récupération au service et utilise la pagination pour optimiser les performances.
    """
    resource_types = ResourceTypeService.get_all(db, skip=skip, limit=limit)
    return resource_types


@router.get("/{resource_type_id}", response_model=ResourceType)
def get_resource_type(
    resource_type_id: int = Path(..., title="L'identifiant du type de ressource à récupérer", ge=1),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    [Function intent]
    Récupère les détails d'un type de ressource spécifique par son ID.
    
    [Design principles]
    Endpoint public accessible à tous les utilisateurs authentifiés.
    
    [Implementation details]
    Délègue la récupération au service et gère le cas où le type de ressource n'existe pas.
    """
    resource_type = ResourceTypeService.get_by_id(db, resource_type_id)
    if not resource_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Type de ressource avec ID {resource_type_id} non trouvé"
        )
    return resource_type


@router.post("/", response_model=ResourceType, status_code=status.HTTP_201_CREATED)
def create_resource_type(
    resource_type_data: ResourceTypeCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """
    [Function intent]
    Crée un nouveau type de ressource.
    
    [Design principles]
    Endpoint réservé aux administrateurs pour contrôler la taxonomie du système.
    
    [Implementation details]
    Délègue la création au service après validation des données avec Pydantic.
    Retourne un code 201 Created en cas de succès.
    """
    return ResourceTypeService.create(db, resource_type_data)


@router.put("/{resource_type_id}", response_model=ResourceType)
def update_resource_type(
    resource_type_data: ResourceTypeUpdate,
    resource_type_id: int = Path(..., title="L'identifiant du type de ressource à modifier", ge=1),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """
    [Function intent]
    Met à jour un type de ressource existant.
    
    [Design principles]
    Endpoint réservé aux administrateurs pour maintenir la cohérence de la taxonomie.
    
    [Implementation details]
    Délègue la mise à jour au service et gère le cas où le type de ressource n'existe pas.
    """
    resource_type = ResourceTypeService.update(db, resource_type_id, resource_type_data)
    if not resource_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Type de ressource avec ID {resource_type_id} non trouvé"
        )
    return resource_type


@router.delete("/{resource_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource_type(
    resource_type_id: int = Path(..., title="L'identifiant du type de ressource à supprimer", ge=1),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """
    [Function intent]
    Supprime un type de ressource existant.
    
    [Design principles]
    Endpoint réservé aux administrateurs avec vérification préalable de l'absence de dépendances.
    
    [Implementation details]
    Délègue la suppression au service et gère le cas où le type de ressource n'existe pas.
    Retourne un code 204 No Content en cas de succès.
    """
    deleted = ResourceTypeService.delete(db, resource_type_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Type de ressource avec ID {resource_type_id} non trouvé"
        )
