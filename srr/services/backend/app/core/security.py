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
# Fournit les fonctions de sécurité pour l'application, notamment la gestion des tokens JWT
# d'authentification, le hachage et la vérification des mots de passe. Ce module est central 
# pour tous les aspects d'authentification et d'autorisation du système.
###############################################################################
# [Source file design principles]
# - Utilisation de méthodes cryptographiques robustes (bcrypt, JWT)
# - Séparation claire des responsabilités (création de token, vérification mot de passe)
# - Pas de dépendance directe à la base de données ou aux modèles
# - Configuration centralisée des paramètres de sécurité
# - Fonctions pures privilégiées pour faciliter les tests
###############################################################################
# [Source file constraints]
# - Utiliser uniquement des bibliothèques de cryptographie reconnues et maintenues
# - Ne pas stocker ou manipuler de secrets en clair
# - Respecter les bonnes pratiques OWASP pour la sécurité des applications web
# - Les fonctions doivent être thread-safe
###############################################################################
# [Dependencies]
# - app/core/config.py: Configuration centrale de l'application
# - python-jose: Bibliothèque pour JWT
# - passlib: Bibliothèque pour le hachage de mots de passe
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:07:00Z : Création initiale du module de sécurité par CodeAssistant
# * Implémentation des fonctions de génération et validation de tokens JWT
# * Implémentation des fonctions de hachage et vérification de mots de passe
# * Configuration du contexte de hachage avec bcrypt
###############################################################################

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.token import TokenPayload
from app.models.user import User
from app.db.session import get_db
from sqlalchemy.orm import Session

# Configuration du contexte de hachage pour les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Point de terminaison pour l'authentification
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def create_access_token(
    subject: Union[str, Any], 
    expires_delta: Optional[timedelta] = None,
    role: str = "user",
    groups: List[str] = None
) -> str:
    """
    [Function intent]
    Génère un token JWT d'authentification pour un utilisateur.
    
    [Design principles]
    Sécurisation des tokens avec temps d'expiration.
    Utilisation de la configuration centrale pour les paramètres.
    
    [Implementation details]
    Encodage des claims standard JWT avec la bibliothèque jose.
    
    Args:
        subject: Identifiant du sujet du token (généralement username)
        expires_delta: Durée de validité du token (optionnel)
        
    Returns:
        str: Token JWT encodé
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "role": role,
        "groups": groups or []
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    [Function intent]
    Vérifie si un mot de passe en clair correspond au hash stocké.
    
    [Design principles]
    Utilisation de bcrypt pour des comparaisons sécurisées.
    Fonction pure pour faciliter les tests.
    
    [Implementation details]
    Délègue la comparaison au contexte de hachage passlib.
    
    Args:
        plain_password: Mot de passe en clair à vérifier
        hashed_password: Hash du mot de passe stocké
        
    Returns:
        bool: True si le mot de passe correspond, False sinon
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    [Function intent]
    Génère un hash sécurisé pour un mot de passe en clair.
    
    [Design principles]
    Utilisation de bcrypt pour un hachage fort et salé.
    Fonction pure pour faciliter les tests.
    
    [Implementation details]
    Délègue le hachage au contexte de hachage configuré.
    
    Args:
        password: Mot de passe en clair à hacher
        
    Returns:
        str: Hash du mot de passe
    """
    return pwd_context.hash(password)


def create_refresh_token(
    subject: Union[str, Any]
) -> str:
    """
    [Function intent]
    Génère un token JWT de rafraîchissement pour un utilisateur.
    
    [Design principles]
    Token avec durée de vie plus longue pour permettre le rafraîchissement de session.
    Utilise une clé différente de celle des access tokens pour plus de sécurité.
    
    [Implementation details]
    Encodage avec durée de validité plus longue et clé spécifique aux refresh tokens.
    
    Args:
        subject: Identifiant du sujet du token (généralement username)
        
    Returns:
        str: Token JWT encodé pour le rafraîchissement
    """
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode, settings.REFRESH_TOKEN_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    [Function intent]
    Dépendance FastAPI qui extrait et valide l'utilisateur à partir du token JWT.
    
    [Design principles]
    Validation complète du token et récupération de l'utilisateur dans la DB.
    Exceptions HTTP claires en cas d'erreur d'authentification.
    
    [Implementation details]
    Décode le JWT, vérifie sa validité, puis cherche l'utilisateur correspondant.
    
    Args:
        token: Token JWT d'accès
        db: Session de base de données
        
    Returns:
        User: L'utilisateur authentifié
        
    Raises:
        HTTPException: Si le token est invalide ou l'utilisateur non trouvé
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identifiants d'authentification invalides",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            raise credentials_exception
            
    except (JWTError, ValidationError):
        raise credentials_exception
        
    user = db.query(User).filter(User.username == token_data.sub).first()
    
    if not user:
        raise credentials_exception
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte utilisateur désactivé",
        )
        
    return user


def check_permissions(required_role: str = None, required_groups: List[str] = None):
    """
    [Function intent]
    Crée un middleware pour vérifier les permissions d'un utilisateur.
    
    [Design principles]
    Approche flexible permettant de vérifier rôles ou groupes.
    Utilisation comme dépendance FastAPI.
    
    [Implementation details]
    Vérifie si l'utilisateur a le rôle requis ou appartient à l'un des groupes requis.
    
    Args:
        required_role: Rôle nécessaire pour accéder à la ressource
        required_groups: Liste des groupes autorisés à accéder à la ressource
        
    Returns:
        Callable: Fonction de dépendance FastAPI
    """
    async def permission_checker(user: User = Depends(get_current_user)) -> User:
        if required_role and user.role != required_role:
            if required_role == "admin" and user.role != "superadmin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Accès restreint: rôle {required_role} requis",
                )
                
        if required_groups and not any(group in user.groups for group in required_groups):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès restreint: groupe requis",
            )
            
        return user
        
    return permission_checker


def verify_refresh_token(refresh_token: str) -> str:
    """
    [Function intent]
    Vérifie et décode un refresh token JWT.
    
    [Design principles]
    Validation stricte des refresh tokens avec leur clé spécifique.
    
    [Implementation details]
    Décode le JWT avec la clé secrète des refresh tokens et vérifie le type.
    
    Args:
        refresh_token: Token JWT de rafraîchissement à vérifier
        
    Returns:
        str: Identifiant utilisateur contenu dans le token
        
    Raises:
        JWTError: Si le token est invalide ou expiré
    """
    payload = jwt.decode(
        refresh_token, 
        settings.REFRESH_TOKEN_SECRET_KEY, 
        algorithms=[settings.ALGORITHM]
    )
    
    # Vérifie que c'est bien un refresh token
    if payload.get("type") != "refresh":
        raise JWTError("Type de token invalide")
        
    # Vérifie l'expiration
    if datetime.fromtimestamp(payload.get("exp")) < datetime.utcnow():
        raise JWTError("Token expiré")
        
    return payload.get("sub")
