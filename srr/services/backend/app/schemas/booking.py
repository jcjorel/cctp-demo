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
# Définition des schémas Pydantic pour les réservations du SRR.
# Ces schémas permettent la validation et sérialisation des données
# pour les opérations CRUD liées aux réservations.
###############################################################################
# [Source file design principles]
# - Séparation claire des modèles de données (SQLAlchemy) et schémas API (Pydantic)
# - Structure hiérarchique des schémas pour maximiser la réutilisation
# - Validation stricte des données d'entrée
# - Gestion précise des relations avec utilisateurs et ressources
###############################################################################
# [Source file constraints]
# - Doit respecter la structure du modèle SQLAlchemy correspondant
# - Ne doit pas contenir de logique métier complexe
# - Focalisé sur la validation et sérialisation
###############################################################################
# [Dependencies]
# - pydantic: BaseModel, Field, validator
# - typing: Optional, List
# - datetime: datetime
# - app.models.booking: Booking (modèle SQLAlchemy)
# - app.schemas.resource: Resource (schéma Pydantic)
# - app.schemas.user: User (schéma Pydantic)
###############################################################################
# [GenAI tool change history]
# 2025-04-23T12:12:53Z : Création initiale des schémas Pydantic pour les réservations par CodeAssistant
# * Définition des schémas BookingBase, BookingCreate, BookingUpdate et Booking
# * Implémentation du schéma BookingStatus pour les états de réservation
###############################################################################

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class BookingStatusEnum(str, Enum):
    """
    [Class intent]
    Énumération des statuts possibles pour une réservation.
    
    [Design principles]
    Utilisation d'une énumération pour garantir la cohérence des valeurs possibles.
    
    [Implementation details]
    Hérite de str et Enum pour permettre la sérialisation directe en JSON.
    """
    PENDING = "pending"
    APPROVED = "approved" 
    REJECTED = "rejected"
    CANCELED = "canceled"
    COMPLETED = "completed"


class BookingBase(BaseModel):
    """
    [Class intent]
    Schéma de base pour les réservations contenant les attributs communs.
    
    [Design principles]
    Définition des attributs partagés par tous les schémas de réservations.
    Utilisation de la validation Pydantic pour garantir l'intégrité des données.
    
    [Implementation details]
    Utilise des Field pour ajouter des contraintes et des descriptions aux champs.
    """
    resource_id: int = Field(..., description="ID de la ressource réservée")
    user_id: int = Field(..., description="ID de l'utilisateur qui fait la réservation")
    title: str = Field(..., description="Titre/objet de la réservation", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Description détaillée du motif de la réservation")
    start_datetime: datetime = Field(..., description="Date et heure de début de la réservation")
    end_datetime: datetime = Field(..., description="Date et heure de fin de la réservation")
    attendees_count: Optional[int] = Field(1, description="Nombre de participants", ge=1)
    is_recurring: bool = Field(False, description="Indique si c'est une réservation récurrente")
    recurrence_pattern: Optional[str] = Field(None, description="Pattern de récurrence (iCal RFC 5545)")
    
    @validator('end_datetime')
    def validate_end_after_start(cls, v, values):
        """
        [Function intent]
        Valide que la date de fin est postérieure à la date de début.
        
        [Design principles]
        Validation proactive des données pour éviter les erreurs en aval.
        
        [Implementation details]
        Utilise un validator Pydantic pour comparer les dates.
        """
        if 'start_datetime' in values and v <= values['start_datetime']:
            raise ValueError('La date de fin doit être postérieure à la date de début')
        return v


class BookingCreate(BookingBase):
    """
    [Class intent]
    Schéma pour la création d'une nouvelle réservation.
    
    [Design principles]
    Hérite du schéma de base et peut ajouter des champs spécifiques à la création.
    
    [Implementation details]
    Permet la spécification du statut initial si nécessaire.
    """
    status: Optional[BookingStatusEnum] = Field(BookingStatusEnum.PENDING, description="Statut initial de la réservation")


class BookingUpdate(BaseModel):
    """
    [Class intent]
    Schéma pour la mise à jour d'une réservation existante.
    
    [Design principles]
    Tous les champs sont optionnels pour permettre les mises à jour partielles.
    
    [Implementation details]
    Définit les mêmes champs que BookingBase mais tous en Optional.
    """
    resource_id: Optional[int] = Field(None, description="ID de la ressource réservée")
    title: Optional[str] = Field(None, description="Titre/objet de la réservation", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Description détaillée du motif de la réservation")
    start_datetime: Optional[datetime] = Field(None, description="Date et heure de début de la réservation")
    end_datetime: Optional[datetime] = Field(None, description="Date et heure de fin de la réservation")
    attendees_count: Optional[int] = Field(None, description="Nombre de participants", ge=1)
    status: Optional[BookingStatusEnum] = Field(None, description="Statut de la réservation")
    is_recurring: Optional[bool] = Field(None, description="Indique si c'est une réservation récurrente")
    recurrence_pattern: Optional[str] = Field(None, description="Pattern de récurrence (iCal RFC 5545)")


class BookingInDBBase(BookingBase):
    """
    [Class intent]
    Schéma pour représenter une réservation telle que stockée en base de données.
    
    [Design principles]
    Ajoute les champs générés par le système comme l'ID et les timestamps.
    
    [Implementation details]
    Utilise la configuration ORM de Pydantic pour lire depuis les modèles SQLAlchemy.
    """
    id: int = Field(..., description="Identifiant unique de la réservation")
    status: BookingStatusEnum = Field(..., description="Statut actuel de la réservation")
    created_at: datetime = Field(..., description="Date et heure de création de la réservation")
    updated_at: Optional[datetime] = Field(None, description="Date et heure de dernière mise à jour de la réservation")
    
    class Config:
        orm_mode = True


class Booking(BookingInDBBase):
    """
    [Class intent]
    Schéma complet pour l'exposition d'une réservation via l'API.
    
    [Design principles]
    Représentation publique complète d'une réservation avec ses relations.
    
    [Implementation details]
    Hérite de BookingInDBBase. Les relations seront ajoutées par composition.
    """
    pass


class BookingWithDetails(Booking):
    """
    [Class intent]
    Schéma enrichi pour l'exposition détaillée d'une réservation avec les informations
    liées à la ressource et à l'utilisateur.
    
    [Design principles]
    Représentation complète incluant toutes les données nécessaires en une seule requête.
    
    [Implementation details]
    Ajoute les relations avec d'autres entités via des champs supplémentaires.
    """
    # Ces champs seront définis après la création des schémas User et Resource
    resource_name: str = Field(..., description="Nom de la ressource réservée")
    resource_location: Optional[str] = Field(None, description="Emplacement de la ressource")
    user_full_name: str = Field(..., description="Nom complet de l'utilisateur")
    user_email: str = Field(..., description="Email de l'utilisateur")
