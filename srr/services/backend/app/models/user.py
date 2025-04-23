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
# Définit le modèle SQLAlchemy pour les utilisateurs du système. Ce modèle représente
# les attributs essentiels des utilisateurs synchronisés depuis l'Active Directory
# et maintient une représentation locale de leurs propriétés importantes pour l'application.
###############################################################################
# [Source file design principles]
# - Modèle minimal mais suffisant pour le développement initial
# - Stockage des attributs essentiels uniquement (pas de mot de passe car délégué à AD)
# - Utilisation d'UUID pour la compatibilité avec d'autres systèmes
# - Support des rôles multiples via un tableau de chaînes
# - Relations bidirectionnelles vers les entités liées
###############################################################################
# [Source file constraints]
# - Ne pas stocker de données sensibles qui devraient rester dans l'AD
# - Garder la synchronisation avec les données AD aussi simple que possible
# - Les noms d'utilisateur et emails doivent être uniques
# - Le modèle doit rester cohérent avec le schéma de base de données
###############################################################################
# [Dependencies]
# - app/db/base: Modèle de base et mixins
# - sqlalchemy: Bibliothèque ORM
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:14:50Z : Création initiale du modèle User par CodeAssistant
# * Définition des attributs principaux (username, email, roles, etc.)
# * Configuration des relations avec les autres entités
# * Ajout des indices pour optimiser les recherches
###############################################################################

import uuid
from typing import List, Optional

from sqlalchemy import Column, String, Boolean, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    """
    [Class intent]
    Représente un utilisateur du système SRR synchronisé avec l'Active Directory.
    
    [Design principles]
    Fournit une représentation locale des attributs utilisateur essentiels à l'application.
    Ne stocke pas les mots de passe puisque l'authentification est déléguée à l'AD.
    
    [Implementation details]
    Utilise UUID comme clé primaire pour garantir l'unicité globale et faciliter la synchronisation.
    Implémentation minimale pour la phase de développement.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    roles = Column(ARRAY(String), nullable=False, default=["user"])
    department = Column(String(255))
    organization = Column(String(255))
    position = Column(String(255))
    active = Column(Boolean, nullable=False, default=True)
    
    # Champ pour le mode développement uniquement (sera nul en production)
    hashed_password = Column(String(255), nullable=True)
    
    # Relations - définies plus tard pour éviter les dépendances circulaires
    # bookings = relationship("Booking", back_populates="user")
    # approvals = relationship("BookingApproval", back_populates="approver")
    # managed_resources = relationship("Resource", secondary="resource_managers", back_populates="managers")

    def __repr__(self):
        """
        [Function intent]
        Fournit une représentation textuelle de l'objet pour le débogage.
        
        [Design principles]
        Inclut les attributs essentiels pour l'identification.
        
        [Implementation details]
        Format simple et lisible pour faciliter le débogage.
        """
        return f"User(id={self.id}, username={self.username}, email={self.email}, roles={self.roles})"
