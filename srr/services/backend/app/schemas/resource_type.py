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
# Définition des schémas Pydantic pour les types de ressources du SRR.
# Ces schémas permettent la validation et sérialisation des données
# pour les opérations CRUD liées aux types de ressources.
###############################################################################
# [Source file design principles]
# - Séparation claire des modèles de données (SQLAlchemy) et schémas API (Pydantic)
# - Structure hiérarchique des schémas pour maximiser la réutilisation
# - Validation stricte des données d'entrée
# - Contrôle précis des données exposées via l'API
###############################################################################
# [Source file constraints]
# - Doit respecter la structure du modèle SQLAlchemy correspondant
# - Ne doit pas contenir de logique métier complexe
# - Focalisé sur la validation et sérialisation
###############################################################################
# [Dependencies]
# - pydantic: BaseModel, Field, validator
# - typing: Optional, List
# - app.models.resource_type: ResourceType (modèle SQLAlchemy)
###############################################################################
# [GenAI tool change history]
# 2025-04-23T12:04:30Z : Création initiale des schémas Pydantic pour les types de ressources par CodeAssistant
# * Définition des schémas ResourceTypeBase, ResourceTypeCreate, ResourceTypeUpdate et ResourceType
###############################################################################

from pydantic import BaseModel, Field, validator
from typing import Optional, List


class ResourceTypeBase(BaseModel):
    """
    [Class intent]
    Schéma de base pour les types de ressources contenant les attributs communs.
    
    [Design principles]
    Définition des attributs partagés par tous les schémas de types de ressources.
    Utilisation de la validation Pydantic pour garantir l'intégrité des données.
    
    [Implementation details]
    Utilise des Field pour ajouter des contraintes et des descriptions aux champs.
    """
    name: str = Field(..., description="Nom du type de ressource", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Description détaillée du type de ressource")
    icon: Optional[str] = Field(None, description="Icône représentative du type de ressource")
    color: Optional[str] = Field(None, description="Couleur associée au type de ressource (format hex: #RRGGBB)")
    
    @validator('color')
    def validate_color_format(cls, v):
        """
        [Function intent]
        Valide que le format de la couleur est un code hexadécimal valide.
        
        [Design principles]
        Validation proactive des données pour éviter les erreurs en aval.
        
        [Implementation details]
        Utilise un validator Pydantic pour vérifier le format de la couleur.
        """
        if v is None:
            return v
        if not (v.startswith('#') and len(v) == 7):
            raise ValueError('La couleur doit être au format hexadécimal: #RRGGBB')
        try:
            int(v[1:], 16)
        except ValueError:
            raise ValueError('La couleur doit être au format hexadécimal: #RRGGBB')
        return v


class ResourceTypeCreate(ResourceTypeBase):
    """
    [Class intent]
    Schéma pour la création d'un nouveau type de ressource.
    
    [Design principles]
    Hérite du schéma de base et peut ajouter des champs spécifiques à la création.
    
    [Implementation details]
    Actuellement identique au schéma de base, pourrait être étendu à l'avenir.
    """
    pass


class ResourceTypeUpdate(BaseModel):
    """
    [Class intent]
    Schéma pour la mise à jour d'un type de ressource existant.
    
    [Design principles]
    Tous les champs sont optionnels pour permettre les mises à jour partielles.
    
    [Implementation details]
    Définit les mêmes champs que ResourceTypeBase mais tous en Optional.
    """
    name: Optional[str] = Field(None, description="Nom du type de ressource", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Description détaillée du type de ressource")
    icon: Optional[str] = Field(None, description="Icône représentative du type de ressource")
    color: Optional[str] = Field(None, description="Couleur associée au type de ressource (format hex: #RRGGBB)")
    
    @validator('color')
    def validate_color_format(cls, v):
        """
        [Function intent]
        Valide que le format de la couleur est un code hexadécimal valide.
        
        [Design principles]
        Validation proactive des données pour éviter les erreurs en aval.
        
        [Implementation details]
        Utilise un validator Pydantic pour vérifier le format de la couleur.
        """
        if v is None:
            return v
        if not (v.startswith('#') and len(v) == 7):
            raise ValueError('La couleur doit être au format hexadécimal: #RRGGBB')
        try:
            int(v[1:], 16)
        except ValueError:
            raise ValueError('La couleur doit être au format hexadécimal: #RRGGBB')
        return v


class ResourceTypeInDBBase(ResourceTypeBase):
    """
    [Class intent]
    Schéma pour représenter un type de ressource tel que stocké en base de données.
    
    [Design principles]
    Ajoute les champs générés par le système comme l'ID.
    
    [Implementation details]
    Utilise la configuration ORM de Pydantic pour lire depuis les modèles SQLAlchemy.
    """
    id: int = Field(..., description="Identifiant unique du type de ressource")
    
    class Config:
        orm_mode = True


class ResourceType(ResourceTypeInDBBase):
    """
    [Class intent]
    Schéma complet pour l'exposition d'un type de ressource via l'API.
    
    [Design principles]
    Représentation publique complète d'un type de ressource.
    
    [Implementation details]
    Hérite de ResourceTypeInDBBase et pourrait être enrichi avec des informations supplémentaires.
    """
    pass
