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
# Définition des schémas Pydantic pour les ressources du SRR.
# Ces schémas permettent la validation et sérialisation des données
# pour les opérations CRUD et les requêtes de disponibilité des ressources.
###############################################################################
# [Source file design principles]
# - Séparation claire des modèles de données (SQLAlchemy) et schémas API (Pydantic)
# - Structure hiérarchique des schémas pour maximiser la réutilisation
# - Validation stricte des données d'entrée
# - Relations correctement modélisées avec les autres entités
###############################################################################
# [Source file constraints]
# - Doit respecter la structure du modèle SQLAlchemy correspondant
# - Ne doit pas contenir de logique métier complexe
# - Focalisé sur la validation et sérialisation
###############################################################################
# [Dependencies]
# - pydantic: BaseModel, Field, validator
# - typing: Optional, List, Dict
# - datetime: datetime, date, time
# - app.models.resource: Resource (modèle SQLAlchemy)
# - app.schemas.resource_type: ResourceType (schéma Pydantic)
###############################################################################
# [GenAI tool change history]
# 2025-04-23T12:04:53Z : Création initiale des schémas Pydantic pour les ressources par CodeAssistant
# * Définition des schémas ResourceBase, ResourceCreate, ResourceUpdate et Resource
# * Implémentation du schéma ResourceAvailability pour les requêtes de disponibilité
###############################################################################

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from app.schemas.resource_type import ResourceType


class ResourceBase(BaseModel):
    """
    [Class intent]
    Schéma de base pour les ressources contenant les attributs communs.
    
    [Design principles]
    Définition des attributs partagés par tous les schémas de ressources.
    Utilisation de la validation Pydantic pour garantir l'intégrité des données.
    
    [Implementation details]
    Utilise des Field pour ajouter des contraintes et des descriptions aux champs.
    """
    name: str = Field(..., description="Nom de la ressource", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Description détaillée de la ressource")
    location: Optional[str] = Field(None, description="Emplacement physique de la ressource")
    capacity: Optional[int] = Field(None, description="Capacité de la ressource (ex: nombre de personnes)", ge=0)
    resource_type_id: int = Field(..., description="ID du type de ressource associé")
    is_active: bool = Field(True, description="Indique si la ressource est active et disponible à la réservation")
    requires_approval: bool = Field(False, description="Indique si les réservations nécessitent une approbation")
    image_url: Optional[str] = Field(None, description="URL vers l'image de la ressource")
    
    @validator('capacity')
    def validate_capacity(cls, v):
        """
        [Function intent]
        Valide que la capacité est un nombre positif.
        
        [Design principles]
        Validation proactive des données pour éviter les erreurs en aval.
        
        [Implementation details]
        Utilise un validator Pydantic pour vérifier la capacité.
        """
        if v is not None and v < 0:
            raise ValueError('La capacité doit être un nombre positif ou nul')
        return v


class ResourceCreate(ResourceBase):
    """
    [Class intent]
    Schéma pour la création d'une nouvelle ressource.
    
    [Design principles]
    Hérite du schéma de base et peut ajouter des champs spécifiques à la création.
    
    [Implementation details]
    Actuellement identique au schéma de base, pourrait être étendu à l'avenir.
    """
    pass


class ResourceUpdate(BaseModel):
    """
    [Class intent]
    Schéma pour la mise à jour d'une ressource existante.
    
    [Design principles]
    Tous les champs sont optionnels pour permettre les mises à jour partielles.
    
    [Implementation details]
    Définit les mêmes champs que ResourceBase mais tous en Optional.
    """
    name: Optional[str] = Field(None, description="Nom de la ressource", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Description détaillée de la ressource")
    location: Optional[str] = Field(None, description="Emplacement physique de la ressource")
    capacity: Optional[int] = Field(None, description="Capacité de la ressource (ex: nombre de personnes)", ge=0)
    resource_type_id: Optional[int] = Field(None, description="ID du type de ressource associé")
    is_active: Optional[bool] = Field(None, description="Indique si la ressource est active et disponible à la réservation")
    requires_approval: Optional[bool] = Field(None, description="Indique si les réservations nécessitent une approbation")
    image_url: Optional[str] = Field(None, description="URL vers l'image de la ressource")


class ResourceInDBBase(ResourceBase):
    """
    [Class intent]
    Schéma pour représenter une ressource telle que stockée en base de données.
    
    [Design principles]
    Ajoute les champs générés par le système comme l'ID et les timestamps.
    
    [Implementation details]
    Utilise la configuration ORM de Pydantic pour lire depuis les modèles SQLAlchemy.
    """
    id: int = Field(..., description="Identifiant unique de la ressource")
    created_at: datetime = Field(..., description="Date et heure de création de la ressource")
    updated_at: Optional[datetime] = Field(None, description="Date et heure de dernière mise à jour de la ressource")
    
    class Config:
        orm_mode = True


class Resource(ResourceInDBBase):
    """
    [Class intent]
    Schéma complet pour l'exposition d'une ressource via l'API.
    
    [Design principles]
    Représentation publique complète d'une ressource avec ses relations.
    
    [Implementation details]
    Ajoute les relations avec d'autres entités comme le type de ressource.
    """
    resource_type: Optional[ResourceType] = Field(None, description="Type de ressource associé")


class ResourceAvailability(BaseModel):
    """
    [Class intent]
    Schéma pour la vérification et la représentation de la disponibilité d'une ressource.
    
    [Design principles]
    Structure claire pour les requêtes et réponses liées à la disponibilité.
    
    [Implementation details]
    Utilise des structures de données adaptées pour représenter des plages horaires.
    """
    class AvailabilityRequest(BaseModel):
        """
        [Class intent]
        Schéma pour une requête de vérification de disponibilité.
        
        [Design principles]
        Définition des paramètres nécessaires pour vérifier la disponibilité.
        
        [Implementation details]
        Utilise des types date et time pour représenter précisément les plages horaires.
        """
        date_start: date = Field(..., description="Date de début de la période")
        date_end: date = Field(..., description="Date de fin de la période")
        time_start: Optional[time] = Field(None, description="Heure de début (optionnel)")
        time_end: Optional[time] = Field(None, description="Heure de fin (optionnel)")

    class TimeSlot(BaseModel):
        """
        [Class intent]
        Représente un créneau horaire dans le calendrier d'une ressource.
        
        [Design principles]
        Structure simple et claire pour les créneaux horaires.
        
        [Implementation details]
        Utilise datetime pour une précision temporelle complète.
        """
        start: datetime = Field(..., description="Date et heure de début du créneau")
        end: datetime = Field(..., description="Date et heure de fin du créneau")
        is_available: bool = Field(..., description="Indique si le créneau est disponible")
        booking_id: Optional[int] = Field(None, description="ID de la réservation si le créneau est occupé")

    class AvailabilityResponse(BaseModel):
        """
        [Class intent]
        Schéma de réponse pour une requête de disponibilité.
        
        [Design principles]
        Structure claire pour présenter les disponibilités d'une ressource.
        
        [Implementation details]
        Inclut les informations de la ressource et une liste de créneaux disponibles.
        """
        resource_id: int = Field(..., description="ID de la ressource concernée")
        resource_name: str = Field(..., description="Nom de la ressource")
        period_start: datetime = Field(..., description="Début de la période demandée")
        period_end: datetime = Field(..., description="Fin de la période demandée")
        time_slots: List[TimeSlot] = Field([], description="Liste des créneaux horaires disponibles et occupés")
        is_fully_available: bool = Field(..., description="Indique si la ressource est entièrement disponible sur la période")
