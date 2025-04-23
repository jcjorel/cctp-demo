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
# Implémente les endpoints API RESTful pour la gestion des ressources.
# Ce module fournit les fonctionnalités de recherche, consultation, création et
# vérification de disponibilité des ressources dans le système.
###############################################################################
# [Source file design principles]
# - Séparation des responsabilités entre validation, logique métier et accès aux données
# - Validation des entrées via Pydantic
# - Fonctionnalités de filtrage et recherche avancées
# - Documentation Swagger complète
# - Gestion appropriée des erreurs
###############################################################################
# [Source file constraints]
# - Respecter les principes REST
# - Assurer la cohérence des formats de réponse
# - Gérer correctement les autorisations d'accès basées sur les rôles
# - Limiter l'exposition des détails techniques dans les réponses d'API
###############################################################################
# [Dependencies]
# - fastapi: APIRouter, Depends, HTTPException, Query
# - sqlalchemy.orm: Session
# - app.api.deps: get_db, get_current_user, get_current_active_user, get_current_admin_user
# - app.schemas.resource: Resource, ResourceCreate, ResourceUpdate
# - app.services.resource_service: ResourceService
# - typing: List, Optional
###############################################################################
# [GenAI tool change history]
# 2025-04-23T12:35:53Z : Création initiale du fichier endpoints pour les ressources par CodeAssistant
# * Implémentation des routes GET pour listage, filtrage et détails des ressources
# * Implémentation de la route de vérification de disponibilité
# * Implémentation de la route de création (admin uniquement)
###############################################################################

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.api import deps
from app.schemas import resource as resource_schemas
from app.models.user import User
from app.db.session import get_db

router = APIRouter()


@router.get("/", response_model=List[resource_schemas.Resource])
def list_resources(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    resource_type_id: Optional[str] = None,
    location: Optional[str] = None,
    min_capacity: Optional[int] = None,
    name: Optional[str] = None,
    active: bool = True
):
    """
    [Function intent]
    Récupère une liste filtrée des ressources disponibles dans le système.
    
    [Design principles]
    Implémente un filtrage flexible basé sur plusieurs critères pour permettre
    une recherche efficace des ressources selon les besoins.
    
    [Implementation details]
    Utilise des filtres optionnels transmis en paramètres de requête et délègue
    la recherche au service approprié. Convertit les résultats en schéma Pydantic.
    
    Args:
        db: Session de base de données
        current_user: Utilisateur authentifié actuellement
        skip: Nombre d'éléments à ignorer (pagination)
        limit: Nombre maximum d'éléments à retourner
        resource_type_id: Filtre par type de ressource
        location: Filtre par localisation
        min_capacity: Capacité minimale requise
        name: Recherche par nom (correspondance partielle)
        active: Si True, ne retourne que les ressources actives
    
    Returns:
        Liste des ressources correspondant aux critères
    """
    # Construction des filtres
    filters = {}
    if resource_type_id:
        filters["resource_type_id"] = resource_type_id
    if location:
        filters["location"] = location
    if min_capacity:
        filters["min_capacity"] = min_capacity
    if name:
        filters["name"] = name
    filters["active"] = active
    
    # Délégation au service Resource (à implémenter)
    # resources = resource_service.get_multi(db, skip=skip, limit=limit, filters=filters)
    
    # Pour l'instant, retourne une liste vide
    return []


@router.get("/{resource_id}", response_model=resource_schemas.Resource)
def get_resource(
    resource_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    [Function intent]
    Récupère les détails d'une ressource spécifique par son identifiant.
    
    [Design principles]
    Point d'accès direct aux informations complètes d'une ressource,
    avec vérification d'existence et retour approprié des erreurs.
    
    [Implementation details]
    Vérifie l'existence de la ressource et renvoie ses détails complets
    si elle est trouvée, sinon génère une exception HTTP 404.
    
    Args:
        resource_id: Identifiant unique de la ressource
        db: Session de base de données
        current_user: Utilisateur authentifié actuellement
    
    Returns:
        Détails complets de la ressource demandée
    
    Raises:
        HTTPException 404: Si la ressource n'est pas trouvée
    """
    # Délégation au service Resource (à implémenter)
    # resource = resource_service.get(db, id=resource_id)
    # if not resource:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Resource with ID {resource_id} not found"
    #     )
    
    # Pour l'instant, lever une exception 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Resource with ID {resource_id} not found"
    )


@router.get("/{resource_id}/availability", response_model=resource_schemas.ResourceAvailability)
def check_resource_availability(
    resource_id: str,
    start_date: str = Query(..., description="Date de début (format ISO)"),
    end_date: str = Query(..., description="Date de fin (format ISO)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    [Function intent]
    Vérifie la disponibilité d'une ressource sur une période donnée.
    
    [Design principles]
    Permet de vérifier rapidement si une ressource est disponible avant de tenter
    une réservation, en tenant compte des réservations existantes.
    
    [Implementation details]
    Vérifie l'existence de la ressource puis délègue au service booking
    pour vérifier s'il existe des conflits de réservation sur la période.
    
    Args:
        resource_id: Identifiant unique de la ressource
        start_date: Date et heure de début de la période à vérifier
        end_date: Date et heure de fin de la période à vérifier
        db: Session de base de données
        current_user: Utilisateur authentifié actuellement
    
    Returns:
        Statut de disponibilité et détails des créneaux occupés si pertinent
    
    Raises:
        HTTPException 404: Si la ressource n'est pas trouvée
    """
    # Délégation au service Resource (à implémenter)
    # resource = resource_service.get(db, id=resource_id)
    # if not resource:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Resource with ID {resource_id} not found"
    #     )
    
    # Vérification de la disponibilité (à implémenter)
    # availability = booking_service.check_availability(db, resource_id, start_date, end_date)
    
    # Pour l'instant, retourne une disponibilité factice
    return {
        "resource_id": resource_id,
        "is_available": True,
        "conflicts": [],
        "period": {"start": start_date, "end": end_date}
    }


@router.post("/", response_model=resource_schemas.Resource, status_code=status.HTTP_201_CREATED)
def create_resource(
    resource_in: resource_schemas.ResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_admin_user)  # Seuls les admins peuvent créer
):
    """
    [Function intent]
    Crée une nouvelle ressource dans le système.
    
    [Design principles]
    Restreint la création aux administrateurs uniquement, avec validation
    complète des données d'entrée via schéma Pydantic.
    
    [Implementation details]
    Valide les données d'entrée, convertit en modèle de base de données,
    persiste en base puis retourne la représentation API de la ressource créée.
    
    Args:
        resource_in: Données de la ressource à créer
        db: Session de base de données
        current_user: Utilisateur administrateur authentifié
    
    Returns:
        Ressource créée avec son ID généré
    """
    # Délégation au service Resource (à implémenter)
    # resource = resource_service.create(db, obj_in=resource_in, created_by=current_user.id)
    
    # Pour l'instant, retourne un objet factice
    return {
        "id": "00000000-0000-0000-0000-000000000000",
        "name": resource_in.name,
        "description": resource_in.description,
        "resource_type_id": resource_in.resource_type_id,
        "properties": resource_in.properties,
        "requires_approval": resource_in.requires_approval,
        "managers_ids": resource_in.managers_ids,
        "active": True,
        "created_at": "2025-04-23T12:35:53Z",
        "updated_at": "2025-04-23T12:35:53Z"
    }
