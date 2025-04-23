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
# Fournit des classes de base et utilitaires pour les modèles SQLAlchemy.
# Ce module contient la classe de base commune à tous les modèles de l'application,
# avec des fonctionnalités partagées comme les timestamps de création/modification.
###############################################################################
# [Source file design principles]
# - Ne pas répéter les fonctionnalités communes dans chaque modèle (DRY)
# - Standardisation du comportement des modèles
# - Séparation claire des préoccupations
# - Facilitation de la maintenance et de l'extension des modèles
# - Utilisation des mixins pour une composition flexible
###############################################################################
# [Source file constraints]
# - Ne pas inclure de logique métier spécifique
# - Rester compatible avec les futures versions de SQLAlchemy
# - Ne pas créer de dépendances cycliques entre les modèles
###############################################################################
# [Dependencies]
# - app/db/session.py: Définition de la base déclarative
# - sqlalchemy: Bibliothèque ORM
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:09:00Z : Création initiale du module des modèles de base par CodeAssistant
# * Création de la classe de base pour tous les modèles avec timestamps
# * Ajout des mixins pour les fonctionnalités courantes des modèles
# * Définition des fonctions utilitaires pour la manipulation des modèles
###############################################################################

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


@as_declarative()
class Base:
    """
    [Class intent]
    Classe de base pour tous les modèles SQLAlchemy avec fonctionnalités communes.
    
    [Design principles]
    Fournit des fonctionnalités partagées via une classe de base.
    Convention over configuration pour les noms de tables.
    
    [Implementation details]
    Génère automatiquement les noms de table en fonction du nom de classe.
    """
    id: Any
    
    # Génère automatiquement le nom de table à partir du nom de classe
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    # Fonction helper pour la conversion en dictionnaire
    def dict(self) -> Dict[str, Any]:
        """
        [Function intent]
        Convertit l'objet modèle en dictionnaire pour sérialisation.
        
        [Design principles]
        Méthode standardisée pour les conversions.
        
        [Implementation details]
        Utilise __table__ pour extraire les colonnes et leurs valeurs.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TimestampMixin:
    """
    [Class intent]
    Mixin ajoutant des timestamps de création et modification aux modèles.
    
    [Design principles]
    Séparation des préoccupations via mixins réutilisables.
    
    [Implementation details]
    Utilise les fonctions SQL pour les valeurs par défaut et les mises à jour.
    """
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class UUIDMixin:
    """
    [Class intent]
    Mixin ajoutant un identifiant UUID aux modèles.
    
    [Design principles]
    Utilisation d'UUID pour les identifiants uniques globalement.
    
    [Implementation details]
    Génère automatiquement un UUID v4 pour chaque nouvel enregistrement.
    """
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))


# Classe combinant tous les mixins de base
class BaseModel(Base, UUIDMixin, TimestampMixin):
    """
    [Class intent]
    Classe de base complète pour tous les modèles de l'application.
    
    [Design principles]
    Composition de fonctionnalités via l'héritage multiple.
    
    [Implementation details]
    Combine la base déclarative avec les mixins UUID et Timestamp.
    """
    __abstract__ = True


# Importation de tous les modèles pour SQLAlchemy
from app.models.user import User
from app.models.resource_type import ResourceType
from app.models.resource import Resource, resource_managers
from app.models.booking import Booking, BookingStatus
from app.models.booking_approval import BookingApproval, ApprovalStatus

# Activation des relations bidirectionnelles maintenant que tous les modèles sont définis
User.bookings = relationship("Booking", back_populates="user")
User.approvals = relationship("BookingApproval", back_populates="approver")

ResourceType.resources = relationship("Resource", back_populates="resource_type")

Resource.bookings = relationship("Booking", back_populates="resource")
