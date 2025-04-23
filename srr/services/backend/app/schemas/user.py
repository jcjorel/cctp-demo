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
# Définition des schémas Pydantic pour les utilisateurs du SRR.
# Ces schémas permettent la validation et sérialisation des données
# pour les opérations liées aux utilisateurs et leur authentification.
###############################################################################
# [Source file design principles]
# - Séparation claire des modèles de données (SQLAlchemy) et schémas API (Pydantic)
# - Structure hiérarchique des schémas pour maximiser la réutilisation
# - Validation stricte des données d'entrée
# - Protection des données sensibles (mot de passe)
###############################################################################
# [Source file constraints]
# - Doit respecter la structure du modèle SQLAlchemy correspondant
# - Ne doit pas contenir de logique métier complexe
# - Focalisé sur la validation et sérialisation
# - Ne jamais exposer les hachages de mots de passe via l'API
###############################################################################
# [Dependencies]
# - pydantic: BaseModel, Field, validator, EmailStr
# - typing: Optional, List
# - datetime: datetime
# - app.models.user: User (modèle SQLAlchemy)
###############################################################################
# [GenAI tool change history]
# 2025-04-23T12:15:22Z : Création initiale des schémas Pydantic pour les utilisateurs par CodeAssistant
# * Définition des schémas UserBase, UserCreate, UserUpdate et User
# * Implémentation des schémas UserProfile et UserInDB avec sécurité pour les mots de passe
###############################################################################

from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class UserRoleEnum(str, Enum):
    """
    [Class intent]
    Énumération des rôles possibles pour un utilisateur dans le système.
    
    [Design principles]
    Utilisation d'une énumération pour garantir la cohérence des valeurs possibles.
    
    [Implementation details]
    Hérite de str et Enum pour permettre la sérialisation directe en JSON.
    """
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class UserBase(BaseModel):
    """
    [Class intent]
    Schéma de base pour les utilisateurs contenant les attributs communs.
    
    [Design principles]
    Définition des attributs partagés par tous les schémas d'utilisateurs.
    Utilisation de la validation Pydantic pour garantir l'intégrité des données.
    
    [Implementation details]
    Utilise des Field pour ajouter des contraintes et des descriptions aux champs.
    """
    email: EmailStr = Field(..., description="Adresse email de l'utilisateur")
    username: str = Field(..., description="Nom d'utilisateur", min_length=3, max_length=50)
    first_name: str = Field(..., description="Prénom de l'utilisateur")
    last_name: str = Field(..., description="Nom de famille de l'utilisateur")
    department: Optional[str] = Field(None, description="Département ou service de l'utilisateur")
    is_active: bool = Field(True, description="Indique si le compte utilisateur est actif")
    role: UserRoleEnum = Field(UserRoleEnum.USER, description="Rôle de l'utilisateur dans le système")


class UserCreate(UserBase):
    """
    [Class intent]
    Schéma pour la création d'un nouvel utilisateur.
    
    [Design principles]
    Hérite du schéma de base et ajoute les champs nécessaires à la création.
    Protection explicite du mot de passe.
    
    [Implementation details]
    Inclut le champ password qui sera haché avant stockage en base de données.
    """
    password: str = Field(..., description="Mot de passe de l'utilisateur", min_length=8)
    
    @validator('password')
    def password_strength(cls, v):
        """
        [Function intent]
        Vérifie que le mot de passe respecte les règles de sécurité minimales.
        
        [Design principles]
        Validation proactive pour assurer la sécurité des comptes.
        
        [Implementation details]
        Utilise un validator Pydantic pour vérifier le mot de passe.
        """
        if len(v) < 8:
            raise ValueError('Le mot de passe doit contenir au moins 8 caractères')
        # Vérification basique de complexité
        if not any(char.isdigit() for char in v):
            raise ValueError('Le mot de passe doit contenir au moins un chiffre')
        if not any(char.isupper() for char in v):
            raise ValueError('Le mot de passe doit contenir au moins une majuscule')
        return v


class UserUpdate(BaseModel):
    """
    [Class intent]
    Schéma pour la mise à jour d'un utilisateur existant.
    
    [Design principles]
    Tous les champs sont optionnels pour permettre les mises à jour partielles.
    
    [Implementation details]
    Définit les mêmes champs que UserBase mais tous en Optional.
    """
    email: Optional[EmailStr] = Field(None, description="Adresse email de l'utilisateur")
    username: Optional[str] = Field(None, description="Nom d'utilisateur", min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, description="Prénom de l'utilisateur")
    last_name: Optional[str] = Field(None, description="Nom de famille de l'utilisateur")
    department: Optional[str] = Field(None, description="Département ou service de l'utilisateur")
    is_active: Optional[bool] = Field(None, description="Indique si le compte utilisateur est actif")
    role: Optional[UserRoleEnum] = Field(None, description="Rôle de l'utilisateur dans le système")
    password: Optional[str] = Field(None, description="Nouveau mot de passe de l'utilisateur", min_length=8)
    
    @validator('password')
    def password_strength(cls, v):
        """
        [Function intent]
        Vérifie que le mot de passe respecte les règles de sécurité minimales.
        
        [Design principles]
        Validation proactive pour assurer la sécurité des comptes.
        
        [Implementation details]
        Utilise un validator Pydantic pour vérifier le mot de passe.
        """
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError('Le mot de passe doit contenir au moins 8 caractères')
        # Vérification basique de complexité
        if not any(char.isdigit() for char in v):
            raise ValueError('Le mot de passe doit contenir au moins un chiffre')
        if not any(char.isupper() for char in v):
            raise ValueError('Le mot de passe doit contenir au moins une majuscule')
        return v


class UserInDBBase(UserBase):
    """
    [Class intent]
    Schéma pour représenter un utilisateur tel que stocké en base de données.
    
    [Design principles]
    Ajoute les champs générés par le système comme l'ID et les timestamps.
    
    [Implementation details]
    Utilise la configuration ORM de Pydantic pour lire depuis les modèles SQLAlchemy.
    """
    id: int = Field(..., description="Identifiant unique de l'utilisateur")
    ad_distinguished_name: Optional[str] = Field(None, description="Distinguished Name AD de l'utilisateur")
    created_at: datetime = Field(..., description="Date et heure de création du compte")
    updated_at: Optional[datetime] = Field(None, description="Date et heure de dernière mise à jour du compte")

    class Config:
        orm_mode = True


class User(UserInDBBase):
    """
    [Class intent]
    Schéma pour l'exposition d'un utilisateur via l'API.
    
    [Design principles]
    Représentation publique sécurisée d'un utilisateur (sans mot de passe).
    
    [Implementation details]
    Hérite de UserInDBBase sans exposer de données sensibles.
    """
    pass


class UserWithPassword(UserInDBBase):
    """
    [Class intent]
    Schéma interne pour manipuler un utilisateur avec son mot de passe haché.
    Ne doit JAMAIS être exposé via l'API.
    
    [Design principles]
    Séparation stricte entre représentation interne et externe des utilisateurs.
    
    [Implementation details]
    Ajoute le hachage du mot de passe mais uniquement pour usage interne au système.
    """
    hashed_password: str = Field(..., description="Hachage du mot de passe de l'utilisateur")


class UserProfile(BaseModel):
    """
    [Class intent]
    Schéma représentant le profil utilisateur tel qu'exposé à l'utilisateur lui-même.
    
    [Design principles]
    Version enrichie du schéma User avec des informations supplémentaires pertinentes.
    
    [Implementation details]
    Inclut des données statistiques et préférences qui ne sont pas dans le modèle de base.
    """
    id: int = Field(..., description="Identifiant unique de l'utilisateur")
    email: EmailStr = Field(..., description="Adresse email de l'utilisateur")
    username: str = Field(..., description="Nom d'utilisateur")
    first_name: str = Field(..., description="Prénom de l'utilisateur")
    last_name: str = Field(..., description="Nom de famille de l'utilisateur")
    department: Optional[str] = Field(None, description="Département ou service de l'utilisateur")
    role: UserRoleEnum = Field(..., description="Rôle de l'utilisateur dans le système")
    bookings_count: Optional[int] = Field(0, description="Nombre total de réservations effectuées")
    pending_bookings: Optional[int] = Field(0, description="Nombre de réservations en attente")
