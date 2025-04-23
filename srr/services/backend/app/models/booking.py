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
# Définit le modèle SQLAlchemy pour les réservations de ressources.
# Ce modèle représente les demandes de réservation effectuées par les utilisateurs
# pour des ressources spécifiques, avec leurs plages horaires, statut et motif.
###############################################################################
# [Source file design principles]
# - Gestion des périodes de temps avec validation stricte
# - Implémentation d'un workflow d'états pour le cycle de vie des réservations
# - Relations explicites avec l'utilisateur, la ressource et les approbations
# - Contraintes explicites pour garantir l'intégrité des données
# - Annotations pour optimiser les requêtes fréquentes
###############################################################################
# [Source file constraints]
# - La date de fin doit être postérieure à la date de début
# - Une réservation doit être associée à un utilisateur et une ressource
# - Le statut doit être l'une des valeurs autorisées
# - Le motif ne peut pas être vide
# - Les relations doivent maintenir l'intégrité référentielle
###############################################################################
# [Dependencies]
# - app/db/base: Modèle de base et mixins
# - app/models/user: Modèle utilisateur
# - app/models/resource: Modèle ressource
# - sqlalchemy: Bibliothèque ORM
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:17:15Z : Création initiale du modèle Booking par CodeAssistant
# * Définition du modèle avec contrainte de validation des dates
# * Configuration des statuts possibles et du workflow
# * Mise en place des relations avec les utilisateurs et ressources
###############################################################################

import uuid
import enum
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import Column, String, Text, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from app.db.base import Base


class BookingStatus(enum.Enum):
    """
    [Class intent]
    Définit les états possibles d'une réservation dans son cycle de vie.
    
    [Design principles]
    Utilisation d'une énumération pour garantir la cohérence des statuts.
    
    [Implementation details]
    Chaque statut représente une étape distincte dans le workflow.
    """
    PENDING = "pending"        # En attente de validation
    CONFIRMED = "confirmed"    # Validée
    REJECTED = "rejected"      # Refusée
    CANCELLED = "cancelled"    # Annulée par l'utilisateur
    COMPLETED = "completed"    # Terminée (après la date de fin)


class Booking(Base):
    """
    [Class intent]
    Représente une réservation de ressource par un utilisateur.
    
    [Design principles]
    Implémente un workflow d'état permettant de suivre le cycle de vie complet d'une réservation.
    Utilise des contraintes SQL pour garantir la validité des données temporelles.
    
    [Implementation details]
    Une réservation a toujours un utilisateur, une ressource, des dates et un statut.
    La contrainte check_booking_end_after_start garantit une plage horaire valide.
    Des index optimisent les requêtes de recherche par ressource et dates.
    """
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_id = Column(UUID(as_uuid=True), ForeignKey("resources.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False, index=True)
    status = Column(String(20), nullable=False, default=BookingStatus.PENDING.value, index=True)
    purpose = Column(Text, nullable=False)
    
    # Relations - définies plus tard pour éviter les dépendances circulaires
    resource = relationship("Resource", back_populates="bookings")
    user = relationship("User", back_populates="bookings")
    approvals = relationship("BookingApproval", back_populates="booking", cascade="all, delete-orphan")
    
    # Contraintes
    __table_args__ = (
        CheckConstraint('end_time > start_time', name='check_booking_end_after_start'),
    )

    def __repr__(self):
        """
        [Function intent]
        Fournit une représentation textuelle de l'objet pour le débogage.
        
        [Design principles]
        Inclut les attributs essentiels pour l'identification.
        
        [Implementation details]
        Format simple et lisible pour faciliter le débogage.
        """
        return (f"Booking(id={self.id}, resource_id={self.resource_id}, "
                f"user_id={self.user_id}, start={self.start_time}, end={self.end_time}, "
                f"status={self.status})")
    
    @property
    def duration(self) -> timedelta:
        """
        [Function intent]
        Calcule la durée de la réservation.
        
        [Design principles]
        Propriété calculée pour simplifier l'accès aux informations dérivées.
        
        [Implementation details]
        Soustraction simple entre fin et début.
        
        Returns:
            timedelta: Durée de la réservation
        """
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return timedelta(0)
    
    def is_active(self) -> bool:
        """
        [Function intent]
        Vérifie si la réservation est active (confirmée et non terminée).
        
        [Design principles]
        Logic métier encapsulée dans le modèle.
        
        [Implementation details]
        Utilise le statut et les dates pour déterminer si la réservation est active.
        
        Returns:
            bool: True si la réservation est active, False sinon
        """
        now = datetime.now()
        return (self.status == BookingStatus.CONFIRMED.value and 
                self.end_time >= now)
    
    def overlaps_with(self, other: 'Booking') -> bool:
        """
        [Function intent]
        Vérifie si cette réservation chevauche une autre réservation.
        
        [Design principles]
        Encapsulation de la logique de validation de chevauchement.
        
        [Implementation details]
        Algorithme standard de détection de chevauchement de périodes.
        
        Args:
            other: Autre réservation à comparer
            
        Returns:
            bool: True s'il y a chevauchement, False sinon
        """
        # Chevauchement si l'une des réservations commence pendant l'autre
        return (self.resource_id == other.resource_id and
                self.start_time < other.end_time and 
                self.end_time > other.start_time)
