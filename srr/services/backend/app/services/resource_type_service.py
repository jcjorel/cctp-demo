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
# Service pour la gestion des types de ressources dans le SRR.
# Ce service fournit les fonctionnalités de création, lecture, mise à jour
# et suppression (CRUD) pour les types de ressources.
###############################################################################
# [Source file design principles]
# - Séparation entre la couche API et la couche d'accès aux données
# - Encapsulation des opérations de base de données
# - Gestion des erreurs avec des exceptions spécifiques
# - Service sans état pour faciliter les tests et la scalabilité
###############################################################################
# [Source file constraints]
# - Utilisation exclusive de SQLAlchemy pour l'accès aux données
# - Ne pas contenir de logique de présentation ou d'API
# - Respecter les contraintes de sécurité (pas de requêtes SQL brutes)
###############################################################################
# [Dependencies]
# - sqlalchemy: Session
# - typing: List, Optional, Dict, Any
# - app.models.resource_type: ResourceType (modèle SQLAlchemy)
# - app.schemas.resource_type: ResourceTypeCreate, ResourceTypeUpdate (schémas Pydantic)
# - app.core.exceptions: exceptions métier
###############################################################################
# [GenAI tool change history]
# 2025-04-23T12:17:04Z : Création initiale du service pour les types de ressources par CodeAssistant
# * Implémentation des méthodes CRUD pour les types de ressources
# * Ajout de la validation et gestion des erreurs
###############################################################################

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status

from app.models.resource_type import ResourceType
from app.schemas.resource_type import ResourceTypeCreate, ResourceTypeUpdate


class ResourceTypeService:
    """
    [Class intent]
    Service pour la gestion des types de ressources, fournissant les opérations CRUD.
    
    [Design principles]
    Encapsule les opérations de base de données et fournit une interface claire pour
    manipuler les types de ressources.
    
    [Implementation details]
    Utilise SQLAlchemy pour interagir avec la base de données et gère les erreurs
    avec des exceptions spécifiques.
    """
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[ResourceType]:
        """
        [Function intent]
        Récupère tous les types de ressources avec pagination.
        
        [Design principles]
        Utilisation de la pagination pour éviter de surcharger la mémoire
        avec trop de résultats.
        
        [Implementation details]
        Requête simple avec offset et limit pour la pagination.
        
        Args:
            db: Session SQLAlchemy pour accéder à la base de données
            skip: Nombre d'éléments à ignorer (pour pagination)
            limit: Nombre maximum d'éléments à retourner
            
        Returns:
            Liste des types de ressources
        """
        return db.query(ResourceType).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, resource_type_id: int) -> Optional[ResourceType]:
        """
        [Function intent]
        Récupère un type de ressource par son identifiant.
        
        [Design principles]
        Accès direct par identifiant pour une récupération efficace.
        
        [Implementation details]
        Utilise la méthode get de SQLAlchemy qui retourne None si non trouvé.
        
        Args:
            db: Session SQLAlchemy pour accéder à la base de données
            resource_type_id: Identifiant du type de ressource à récupérer
            
        Returns:
            Le type de ressource ou None si non trouvé
        """
        return db.query(ResourceType).filter(ResourceType.id == resource_type_id).first()
    
    @staticmethod
    def create(db: Session, resource_type_data: ResourceTypeCreate) -> ResourceType:
        """
        [Function intent]
        Crée un nouveau type de ressource.
        
        [Design principles]
        Validation des données d'entrée avec Pydantic avant création.
        
        [Implementation details]
        Conversion du schéma Pydantic en modèle SQLAlchemy et gestion des erreurs d'intégrité.
        
        Args:
            db: Session SQLAlchemy pour accéder à la base de données
            resource_type_data: Données du type de ressource à créer
            
        Returns:
            Le type de ressource créé
            
        Raises:
            HTTPException: Si le type de ressource existe déjà ou autre erreur d'intégrité
        """
        try:
            db_resource_type = ResourceType(
                name=resource_type_data.name,
                description=resource_type_data.description,
                icon=resource_type_data.icon,
                color=resource_type_data.color
            )
            db.add(db_resource_type)
            db.commit()
            db.refresh(db_resource_type)
            return db_resource_type
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce type de ressource existe déjà ou viole une contrainte d'intégrité"
            )
    
    @staticmethod
    def update(
        db: Session,
        resource_type_id: int,
        resource_type_data: ResourceTypeUpdate
    ) -> Optional[ResourceType]:
        """
        [Function intent]
        Met à jour un type de ressource existant.
        
        [Design principles]
        Ne modifie que les champs fournis dans les données de mise à jour.
        
        [Implementation details]
        Récupère d'abord l'entité, puis applique les modifications et gère les erreurs.
        
        Args:
            db: Session SQLAlchemy pour accéder à la base de données
            resource_type_id: Identifiant du type de ressource à modifier
            resource_type_data: Données de mise à jour
            
        Returns:
            Le type de ressource mis à jour ou None si non trouvé
            
        Raises:
            HTTPException: Si le type de ressource n'existe pas ou erreur d'intégrité
        """
        db_resource_type = ResourceTypeService.get_by_id(db, resource_type_id)
        if not db_resource_type:
            return None
        
        try:
            update_data = resource_type_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_resource_type, key, value)
            
            db.commit()
            db.refresh(db_resource_type)
            return db_resource_type
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La mise à jour viole une contrainte d'intégrité"
            )
    
    @staticmethod
    def delete(db: Session, resource_type_id: int) -> bool:
        """
        [Function intent]
        Supprime un type de ressource par son identifiant.
        
        [Design principles]
        Vérification de l'existence avant suppression pour éviter les erreurs silencieuses.
        
        [Implementation details]
        Récupère d'abord l'entité pour vérifier qu'elle existe, puis la supprime.
        
        Args:
            db: Session SQLAlchemy pour accéder à la base de données
            resource_type_id: Identifiant du type de ressource à supprimer
            
        Returns:
            True si supprimé, False si non trouvé
            
        Raises:
            HTTPException: Si des ressources dépendent encore de ce type
        """
        db_resource_type = ResourceTypeService.get_by_id(db, resource_type_id)
        if not db_resource_type:
            return False
        
        try:
            db.delete(db_resource_type)
            db.commit()
            return True
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible de supprimer ce type de ressource car des ressources y sont associées"
            )
