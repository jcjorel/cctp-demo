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
# Définit le modèle SQLAlchemy pour les types de ressources du système.
# Ce modèle définit les catégories de ressources disponibles et leurs propriétés
# spécifiques via un schéma JSON dynamique, permettant une grande flexibilité
# dans la définition des attributs des ressources.
###############################################################################
# [Source file design principles]
# - Schéma flexible via JSON pour des propriétés dynamiques par type
# - Centralisation des définitions et contraintes par type de ressource
# - Séparation claire entre type de ressource et instances de ressource
# - Support de la validation avec propriétés requises explicites
# - Extensibilité du modèle sans modification du schéma de base
###############################################################################
# [Source file constraints]
# - Les noms de types de ressources doivent être uniques
# - Le schéma JSON doit être valide et bien formé
# - Les propriétés requises doivent exister dans le schéma
# - Maintenir la compatibilité avec les fonctionnalités de validation
###############################################################################
# [Dependencies]
# - app/db/base: Modèle de base et mixins
# - sqlalchemy: Bibliothèque ORM
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:15:40Z : Création initiale du modèle ResourceType par CodeAssistant
# * Définition du schéma flexible avec propriétés JSON
# * Configuration des contraintes sur les noms de types
# * Préparation des relations avec les ressources
###############################################################################

import uuid
from typing import Dict, List, Any

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship

from app.db.base import Base


class ResourceType(Base):
    """
    [Class intent]
    Définit les différents types de ressources disponibles dans le système.
    
    [Design principles]
    Utilise un schéma JSON flexible pour permettre des propriétés dynamiques selon le type.
    Centralise la définition des propriétés et contraintes par type de ressource.
    
    [Implementation details]
    Les ressources héritent des propriétés et contraintes définies dans leur type.
    Le schéma JSON définit les types, valeurs possibles et validations pour les propriétés.
    """
    __tablename__ = "resource_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    schema = Column(JSONB, nullable=False, default={})
    required_properties = Column(ARRAY(String), nullable=False, default=[])
    
    # Relations - définies plus tard pour éviter les dépendances circulaires
    # resources = relationship("Resource", back_populates="resource_type")

    def __repr__(self):
        """
        [Function intent]
        Fournit une représentation textuelle de l'objet pour le débogage.
        
        [Design principles]
        Inclut les attributs essentiels pour l'identification.
        
        [Implementation details]
        Format simple et lisible pour faciliter le débogage.
        """
        return f"ResourceType(id={self.id}, name={self.name})"
    
    def validate_properties(self, properties: Dict[str, Any]) -> bool:
        """
        [Function intent]
        Vérifie si les propriétés d'une ressource sont conformes au schéma du type.
        
        [Design principles]
        Encapsulation de la logique de validation dans le type de ressource.
        
        [Implementation details]
        Vérifie la présence des propriétés requises et la conformité au schéma.
        Version simplifiée pour l'environnement de développement.
        
        Args:
            properties: Dictionnaire des propriétés à valider
            
        Returns:
            bool: True si les propriétés sont valides, False sinon
        """
        # Vérification des propriétés requises
        for prop in self.required_properties:
            if prop not in properties:
                return False
                
        # Version simplifiée pour le développement
        # Une vraie implémentation utiliserait un validateur JSON Schema
        return True
