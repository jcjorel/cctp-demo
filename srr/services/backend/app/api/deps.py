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
# Fournit des dépendances réutilisables pour l'injection de dépendances FastAPI.
# Ce module centralise les fonctions qui peuvent être utilisées comme dépendances
# dans les routes FastAPI, particulièrement pour l'authentification, la gestion
# des sessions de base de données, et les vérifications de permissions.
###############################################################################
# [Source file design principles]
# - Réutilisation du code pour les dépendances communes
# - Séparation claire des préoccupations
# - Utilisation du système d'injection de dépendances de FastAPI
# - Gestion appropriée des ressources (sessions DB, etc.)
# - Vérifications de sécurité centralisées
###############################################################################
# [Source file constraints]
# - Les dépendances doivent être facilement testables
# - Éviter la duplication de la logique d'authentification/autorisation
# - Les erreurs doivent être gérées de manière cohérente (exceptions HTTP)
# - Les ressources créées doivent être correctement libérées
###############################################################################
# [Dependencies]
# - fastapi: Depends, HTTPException, status
# - fastapi.security: OAuth2PasswordBearer
# - sqlalchemy.orm: Session
# - jose: jwt, JWTError
# - pydantic: ValidationError
# - app/db/session: SessionLocal
# - app/core/config: settings
# - app/utils/mock_ad: fonctions mock pour le développement
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:12:00Z : Création initiale du module des dépendances par CodeAssistant
# * Implémentation de get_db pour l'injection de session de base de données
# * Configuration du système OAuth2 pour l'authentification
# * Implémentation des vérifications de rôles utilisateur
###############################################################################

from typing import Generator, Optional, List, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.core.security import verify_password

# Configuration du schéma OAuth2 pour l'authentification par token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    scheme_name="JWT"
)


def get_db() -> Generator:
    """
    [Function intent]
    Fournit une session de base de données et assure sa fermeture après utilisation.
    
    [Design principles]
    Pattern Unit-of-Work pour isolation des transactions.
    Gestion des ressources via générateur Python.
    
    [Implementation details]
    Utilisation du contexte Python pour garantir la fermeture de session.
    Implémentée comme un générateur pour l'injection de dépendances FastAPI.
    
    Yields:
        Session: Session SQLAlchemy pour interagir avec la base de données
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Type pour représenter un utilisateur, à remplacer par le vrai modèle une fois défini
User = Dict[str, Any]


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> User:
    """
    [Function intent]
    Récupère l'utilisateur authentifié à partir du token JWT.
    
    [Design principles]
    Validation systématique du token avant accès aux ressources protégées.
    Gestion adaptative selon l'environnement (mock ou production).
    
    [Implementation details]
    Décodage du token JWT et récupération de l'utilisateur.
    Utilise le service mock AD en environnement de développement.
    
    Args:
        token: Token JWT d'authentification
        
    Returns:
        User: Utilisateur authentifié
        
    Raises:
        HTTPException: Si le token est invalide ou l'utilisateur n'existe pas
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token d'authentification invalide",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token d'authentification invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # En mode développement, utilise le service mock
    if settings.MOCK_AUTH:
        from app.utils.mock_ad import get_mock_user
        user = get_mock_user(username)
    else:
        # Code pour récupérer l'utilisateur depuis la base de données
        # À implémenter lorsque les modèles seront définis
        user = None  # get_user_by_username(db, username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    [Function intent]
    Vérifie que l'utilisateur courant est actif.
    
    [Design principles]
    Séparation de la validation de token et de la vérification d'activité.
    
    [Implementation details]
    Vérifie le champ "active" de l'utilisateur retourné par l'authentification.
    
    Args:
        current_user: Utilisateur obtenu via get_current_user
        
    Returns:
        User: Utilisateur authentifié et actif
        
    Raises:
        HTTPException: Si l'utilisateur est inactif
    """
    if not current_user.get("active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Utilisateur inactif",
        )
    return current_user


def check_user_role(required_roles: List[str]):
    """
    [Function intent]
    Crée un validateur de rôle utilisateur pour contrôler l'accès aux ressources.
    
    [Design principles]
    Factory function pour créer des dépendances de vérification de rôle réutilisables.
    
    [Implementation details]
    Renvoie une fonction de dépendance qui vérifie si l'utilisateur a au moins un des rôles requis.
    
    Args:
        required_roles: Liste des rôles autorisés
        
    Returns:
        Callable: Fonction de dépendance FastAPI
    """
    
    def _has_required_role(current_user: User = Depends(get_current_active_user)) -> User:
        """
        [Function intent]
        Vérifie si l'utilisateur a au moins un des rôles requis.
        
        [Design principles]
        Vérification des rôles de manière non-bloquante (un seul rôle suffit).
        
        [Implementation details]
        Compare les rôles de l'utilisateur avec la liste des rôles requis.
        
        Args:
            current_user: Utilisateur obtenu via get_current_active_user
            
        Returns:
            User: Utilisateur si autorisé
            
        Raises:
            HTTPException: Si l'utilisateur n'a pas les rôles requis
        """
        user_roles = current_user.get("roles", [])
        
        # Vérification si l'utilisateur a au moins un des rôles requis
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès non autorisé. Un des rôles suivants est requis: {', '.join(required_roles)}",
            )
        return current_user
    
    return _has_required_role


# Dépendances préconfigurées pour les rôles courants
get_current_admin = check_user_role(["admin"])
get_current_manager = check_user_role(["admin", "resource_manager"])
get_current_normal_user = check_user_role(["user", "admin", "resource_manager"])
