from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    """
    [Class intent]
    Modèle représentant la réponse de l'API d'authentification.
    
    [Design principles]
    Séparation claire entre le token d'accès et les données utilisateur.
    
    [Implementation details]
    Structure retournée après une authentification réussie.
    """
    token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Type du token (toujours 'bearer')")
    expires_in: int = Field(..., description="Durée de validité du token en secondes")
    refresh_token: Optional[str] = Field(None, description="Token de rafraîchissement (optionnel)")
    user: dict = Field(..., description="Informations utilisateur")


class TokenPayload(BaseModel):
    """
    [Class intent]
    Modèle interne représentant le contenu d'un JWT décodé.
    
    [Design principles]
    Structure minimale contenant uniquement les informations nécessaires pour l'identification et l'autorisation.
    
    [Implementation details]
    Utilisé pour extraire et valider les informations du JWT.
    """
    sub: str = Field(..., description="Identifiant utilisateur (username)")
    exp: int = Field(..., description="Timestamp d'expiration du token")
    role: str = Field(..., description="Rôle de l'utilisateur")
    groups: List[str] = Field(default=[], description="Groupes AD de l'utilisateur")


class LoginRequest(BaseModel):
    """
    [Class intent]
    Modèle de requête pour l'authentification utilisateur.
    
    [Design principles]
    Interface simple ne demandant que les informations essentielles.
    
    [Implementation details]
    Contient les identifiants nécessaires à l'authentification.
    """
    username: str = Field(..., description="Nom d'utilisateur")
    password: str = Field(..., description="Mot de passe")
    remember_me: bool = Field(default=False, description="Si vrai, génère un refresh token")


class RefreshRequest(BaseModel):
    """
    [Class intent]
    Modèle de requête pour rafraîchir un token expiré.
    
    [Design principles]
    Simple requête contenant uniquement le refresh token.
    
    [Implementation details]
    Utilisé pour obtenir un nouveau token d'accès sans avoir à se réauthentifier.
    """
    refresh_token: str = Field(..., description="Token de rafraîchissement")


class UserCredentials(BaseModel):
    """
    [Class intent]
    Modèle représentant les informations d'identification d'un utilisateur.
    
    [Design principles]
    Séparation entre les données d'authentification et les informations de profil.
    
    [Implementation details]
    Utilisé en interne par le système d'authentification.
    """
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: str = "user"
    department: Optional[str] = None
    groups: List[str] = []
