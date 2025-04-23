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
# Implémente les endpoints API RESTful pour la gestion des utilisateurs.
# Ce module fournit principalement des endpoints pour récupérer le profil
# de l'utilisateur courant et potentiellement mettre à jour ses préférences.
###############################################################################
# [Source file design principles]
# - Séparation des responsabilités entre validation, logique métier et accès aux données
# - Protection de la vie privée avec exposition limitée des données utilisateur
# - Validation des entrées via Pydantic
# - Documentation Swagger complète
# - Gestion appropriée des erreurs
###############################################################################
# [Source file constraints]
# - Respecter les principes REST
# - Assurer la cohérence des formats de réponse
# - Ne pas exposer de données sensibles via l'API
# - Limiter l'accès aux données des autres utilisateurs sauf pour les administrateurs
###############################################################################
# [Dependencies]
# - fastapi: APIRouter, Depends, HTTPException
# - sqlalchemy.orm: Session
# - app.api.deps: get_db, get_current_user, get_current_active_user, get_current_admin_user
# - app.schemas.user: User, UserProfile, UserUpdate
# - app.services.user: UserService
# - typing: List, Optional
###############################################################################
# [GenAI tool change history]
# 2025-04-23T12:38:31Z : Création initiale du fichier endpoints pour les utilisateurs par CodeAssistant
# * Implémentation de l'endpoint pour récupérer le profil utilisateur courant
# * Préparation d'endpoints additionnels pour la gestion des utilisateurs (admin)
###############################################################################

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api import deps
from app.schemas import user as user_schemas
from app.models.user import User
from app.db.session import get_db

router = APIRouter()


@router.get("/profile", response_model=user_schemas.UserProfile)
def get_current_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    [Function intent]
    Récupère le profil de l'utilisateur actuellement connecté.
    
    [Design principles]
    Point d'accès unique pour l'utilisateur afin d'obtenir ses propres informations,
    sans nécessiter d'ID utilisateur spécifique pour plus de sécurité.
    
    [Implementation details]
    Utilise le token d'authentification pour identifier l'utilisateur courant,
    récupère ses données complètes puis les filtre selon le schéma UserProfile
    pour ne pas exposer de données sensibles.
    
    Args:
        db: Session de base de données
        current_user: Utilisateur authentifié actuellement (injecté via dépendance)
    
    Returns:
        Profil de l'utilisateur courant sans les données sensibles
    """
    # Les données de l'utilisateur sont déjà disponibles via la dépendance current_user
    # Mais normalement on pourrait vouloir récupérer des informations supplémentaires
    # user_profile = user_service.get_profile(db, user_id=current_user.id)
    
    # Pour l'instant, on utilise directement les données de current_user
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "full_name": getattr(current_user, "full_name", ""),
        "department": getattr(current_user, "department", ""),
        "roles": getattr(current_user, "roles", []),
        "is_active": current_user.is_active,
        "is_admin": getattr(current_user, "is_admin", False),
        "last_login": getattr(current_user, "last_login", None)
    }


@router.put("/profile", response_model=user_schemas.UserProfile)
def update_current_user_profile(
    user_update: user_schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    [Function intent]
    Met à jour les préférences et informations modifiables du profil de l'utilisateur courant.
    
    [Design principles]
    Permet à l'utilisateur de gérer ses propres données tout en respectant
    les contraintes de sécurité sur les champs modifiables.
    
    [Implementation details]
    Limite les champs pouvant être modifiés via validation Pydantic,
    puis applique les modifications au profil de l'utilisateur courant.
    
    Args:
        user_update: Données à mettre à jour dans le profil
        db: Session de base de données
        current_user: Utilisateur authentifié actuellement
    
    Returns:
        Profil mis à jour de l'utilisateur
    """
    # Mise à jour du profil utilisateur (à implémenter)
    # updated_user = user_service.update_profile(
    #     db, user_id=current_user.id, update_data=user_update
    # )
    
    # Pour l'instant, retourne un objet factice
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "full_name": user_update.full_name or getattr(current_user, "full_name", ""),
        "department": getattr(current_user, "department", ""),
        "roles": getattr(current_user, "roles", []),
        "is_active": current_user.is_active,
        "is_admin": getattr(current_user, "is_admin", False),
        "last_login": getattr(current_user, "last_login", None)
    }


# --- Endpoints réservés aux administrateurs ---

@router.get("/", response_model=List[user_schemas.UserAdminView])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_admin_user),
    skip: int = 0,
    limit: int = 100,
    active: Optional[bool] = None,
    search: Optional[str] = None
):
    """
    [Function intent]
    Récupère la liste des utilisateurs du système pour les administrateurs.
    
    [Design principles]
    Fournit aux administrateurs une vue synthétique de tous les utilisateurs
    avec possibilité de filtrage et pagination.
    
    [Implementation details]
    Réservé aux administrateurs uniquement, applique filtrages et pagination
    puis récupère les données utilisateur sans les informations sensibles.
    
    Args:
        db: Session de base de données
        current_user: Administrateur authentifié
        skip: Nombre d'éléments à ignorer (pagination)
        limit: Nombre maximum d'éléments à retourner
        active: Filtrer par statut actif/inactif si spécifié
        search: Recherche textuelle sur username, email, nom
        
    Returns:
        Liste des utilisateurs correspondant aux critères
    """
    # Construction des filtres
    filters = {}
    if active is not None:
        filters["is_active"] = active
    if search:
        filters["search"] = search
    
    # Délégation au service User (à implémenter)
    # users = user_service.get_multi(db, skip=skip, limit=limit, filters=filters)
    
    # Pour l'instant, retourne une liste vide
    return []


@router.get("/{user_id}", response_model=user_schemas.UserAdminView)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_admin_user)
):
    """
    [Function intent]
    Récupère les détails d'un utilisateur spécifique pour les administrateurs.
    
    [Design principles]
    Permet aux administrateurs d'accéder aux détails complets d'un utilisateur
    avec sécurité et contrôle d'accès appropriés.
    
    [Implementation details]
    Réservé aux administrateurs uniquement, vérifie l'existence de l'utilisateur
    puis récupère ses données sans les informations sensibles.
    
    Args:
        user_id: Identifiant unique de l'utilisateur
        db: Session de base de données
        current_user: Administrateur authentifié
        
    Returns:
        Détails de l'utilisateur demandé
        
    Raises:
        HTTPException 404: Si l'utilisateur n'est pas trouvé
    """
    # Délégation au service User (à implémenter)
    # user = user_service.get(db, id=user_id)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"User with ID {user_id} not found"
    #     )
    
    # Pour l'instant, lever une exception 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with ID {user_id} not found"
    )
