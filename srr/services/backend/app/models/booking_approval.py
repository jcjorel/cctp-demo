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
# Définit le modèle SQLAlchemy pour les approbations de réservations.
# Ce modèle représente les décisions prises par les gestionnaires sur les
# demandes de réservation qui nécessitent une validation.
###############################################################################
# [Source file design principles]
# - Traçabilité complète du processus d'approbation
# - Association explicite avec la réservation et l'approbateur
# - Support des commentaires pour justifier les décisions
# - Horodatage précis des décisions
# - Workflow d'états aligné avec celui des réservations
###############################################################################
# [Source file constraints]
# - Une approbation doit être associée à une réservation et un approbateur
# - Le statut doit être l'une des valeurs autorisées
# - Une réservation peut avoir plusieurs approbations (historique)
# - Les relations doivent maintenir l'intégrité référentielle
###############################################################################
# [Dependencies]
# - app/db/base: Modèle de base et mixins
# - app/models/booking: Modèle de réservation associée
# - app/models/user: Modèle utilisateur (approbateur)
# - sqlalchemy: Bibliothèque ORM
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:18:10Z : Création initiale du modèle BookingApproval par CodeAssistant
# * Définition du modèle avec les statuts d'approbation
# * Configuration des relations avec les réservations et utilisateurs
# * Implémentation de l'horodatage des décisions
###############################################################################

import uuid
import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, Text, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class ApprovalStatus(enum.Enum):
    """
    [Class intent]
    Définit les états possibles d'une approbation de réservation.
    
    [Design principles]
    Utilisation d'une énumération pour garantir la cohérence des statuts.
    
    [Implementation details]
    Les statuts reflètent les différentes décisions possibles dans le workflow.
    """
    PENDING = "pending"      # En attente de décision
    APPROVED = "approved"    # Approuvée
    REJECTED = "rejected"    # Refusée
    CANCELLED = "cancelled"  # Annulée (processus d'approbation abandonné)


class BookingApproval(Base):
    """
    [Class intent]
    Représente la validation d'une réservation par un gestionnaire.
    
    [Design principles]
    Implémente le processus d'approbation pour les ressources nécessitant validation.
    Conserve une trace auditable des décisions et leurs justifications.
    
    [Implementation details]
    Chaque approbation est liée à un booking et maintient son propre statut.
    L'horodatage automatique permet de tracer précisément le moment de la décision.
    """
    __tablename__ = "booking_approvals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"), nullable=False, index=True)
    approver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(String(20), nullable=False, default=ApprovalStatus.PENDING.value)
    comment = Column(Text)
    decision_time = Column(DateTime(timezone=True), nullable=False, default=func.now())
    
    # Relations - définies plus tard pour éviter les dépendances circulaires
    booking = relationship("Booking", back_populates="approvals")
    approver = relationship("User", back_populates="approvals")

    def __repr__(self):
        """
        [Function intent]
        Fournit une représentation textuelle de l'objet pour le débogage.
        
        [Design principles]
        Inclut les attributs essentiels pour l'identification.
        
        [Implementation details]
        Format simple et lisible pour faciliter le débogage.
        """
        return (f"BookingApproval(id={self.id}, booking_id={self.booking_id}, "
                f"approver_id={self.approver_id}, status={self.status})")
    
    def update_status(self, status: str, comment: Optional[str] = None) -> None:
        """
        [Function intent]
        Met à jour le statut de l'approbation avec un commentaire optionnel.
        
        [Design principles]
        Encapsulation de la logique de modification de statut.
        
        [Implementation details]
        Met à jour le statut et l'horodatage de la décision.
        
        Args:
            status: Nouveau statut de l'approbation
            comment: Commentaire optionnel justifiant la décision
        """
        try:
            # Validation du statut via l'énumération
            ApprovalStatus(status)
            self.status = status
            self.decision_time = datetime.now()
            if comment:
                self.comment = comment
        except ValueError:
            raise ValueError(f"Statut d'approbation non valide: {status}")
