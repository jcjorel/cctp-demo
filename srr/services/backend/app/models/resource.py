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
# Définit le modèle SQLAlchemy pour les ressources réservables dans le système.
# Ce modèle représente les instances concrètes des différents types de ressources,
# avec leurs propriétés dynamiques spécifiques stockées en JSON et leurs relations
# aux utilisateurs qui les gèrent et aux réservations qui les concernent.
###############################################################################
# [Source file design principles]
# - Propriétés de base communes à toutes les ressources
# - Propriétés spécifiques flexibles via JSON pour chaque type
# - Relation explicite avec le type de ressource pour la validation
# - Support de l'approbation conditionnelle des réservations
# - Relations many-to-many avec les gestionnaires
###############################################################################
# [Source file constraints]
# - Les propriétés JSON doivent respecter le schéma défini par le type
# - Chaque ressource doit avoir un type de ressource valide
# - Les noms de ressources doivent être significatifs (non vides)
# - Les relations doivent maintenir l'intégrité référentielle
###############################################################################
# [Dependencies]
# - app/db/base: Modèle de base et mixins
# - app/models/resource_type: Type de ressource associé
# - sqlalchemy: Bibliothèque ORM
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:16:20Z : Création initiale du modèle Resource par CodeAssistant
# * Définition du modèle avec propriétés dynamiques JSON
# * Configuration de la table d'association pour les gestionnaires
# * Mise en place des relations avec les autres entités
###############################################################################

import uuid
from typing import Dict, List, Any, Optional

from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base


# Table d'association pour les gestionnaires de ressources
resource_managers = Table(
    "resource_managers",
    Base.metadata,
    Column("resource_id", UUID(as_uuid=True), ForeignKey("resources.id"), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
)


class Resource(Base):
    """
    [Class intent]
    Représente une ressource réservable dans le système SRR.
    
    [Design principles]
    Combine des propriétés de base communes avec des propriétés dynamiques 
    spécifiques au type stockées en JSON.
    
    [Implementation details]
    Les propriétés JSON sont validées contre le schéma défini dans le type de ressource.
    Les gestionnaires sont associés via une table d'association many-to-many.
    """
    __tablename__ = "resources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    resource_type_id = Column(UUID(as_uuid=True), ForeignKey("resource_types.id"), nullable=False)
    properties = Column(JSONB, nullable=False, default={})
    requires_approval = Column(Boolean, nullable=False, default=False)
    
    # Relations - définies plus tard pour éviter les dépendances circulaires
    resource_type = relationship("ResourceType", back_populates="resources")
    # bookings = relationship("Booking", back_populates="resource")
    managers = relationship("User", secondary=resource_managers, backref="managed_resources")

    def __repr__(self):
        """
        [Function intent]
        Fournit une représentation textuelle de l'objet pour le débogage.
        
        [Design principles]
        Inclut les attributs essentiels pour l'identification.
        
        [Implementation details]
        Format simple et lisible pour faciliter le débogage.
        """
        return f"Resource(id={self.id}, name={self.name}, type={self.resource_type_id})"
    
    def validate(self) -> bool:
        """
        [Function intent]
        Vérifie si les propriétés de la ressource sont conformes au schéma de son type.
        
        [Design principles]
        Délégation de la validation au type de ressource associé.
        
        [Implementation details]
        Utilise la méthode validate_properties du type de ressource.
        Version simplifiée pour l'environnement de développement.
        
        Returns:
            bool: True si les propriétés sont valides, False sinon
        """
        if hasattr(self, 'resource_type') and self.resource_type:
            return self.resource_type.validate_properties(self.properties)
        return False
