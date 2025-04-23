from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_refresh_token
)
from app.schemas.token import Token, LoginRequest, RefreshRequest
from app.models.user import User
from app.db.session import get_db

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    [Function intent]
    Point d'entrée pour l'authentification des utilisateurs.
    
    [Design principles]
    API RESTful standard avec OAuth2PasswordRequestForm pour compatibilité.
    Séparation claire entre authentification et autorisation.
    
    [Implementation details]
    Vérifie les identifiants, génère et retourne des tokens JWT si valides.
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte utilisateur désactivé",
        )
    
    # Générer un access token avec durée limitée
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username,
        expires_delta=access_token_expires,
        role=user.role,
        groups=user.groups,
    )
    
    # Générer un refresh token si demandé
    refresh_token = create_refresh_token(subject=user.username) if form_data.scopes and "offline_access" in form_data.scopes else None
    
    # Préparer les données utilisateur à retourner
    user_data = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "department": user.department,
        "groups": user.groups
    }
    
    return {
        "token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "refresh_token": refresh_token,
        "user": user_data
    }


@router.post("/login/app", response_model=Token)
async def login_app(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    [Function intent]
    Point d'entrée pour l'authentification via l'interface utilisateur principale.
    
    [Design principles]
    Interface simplifiée avec option remember_me pour rafraîchissement.
    Cohérence avec le point d'entrée OAuth2.
    
    [Implementation details]
    Même logique que login_access_token mais avec LoginRequest personnalisé.
    """
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects"
        )
    
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte utilisateur désactivé"
        )
    
    # Générer un access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username,
        expires_delta=access_token_expires,
        role=user.role,
        groups=user.groups
    )
    
    # Générer un refresh token si remember_me est activé
    refresh_token = create_refresh_token(subject=user.username) if login_data.remember_me else None
    
    # Préparer les données utilisateur à retourner (mêmes données que login_access_token)
    user_data = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "department": user.department,
        "groups": user.groups
    }
    
    return {
        "token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "refresh_token": refresh_token,
        "user": user_data
    }


@router.post("/refresh-token", response_model=Token)
async def refresh_access_token(
    refresh_data: RefreshRequest,
    db: Session = Depends(get_db)
):
    """
    [Function intent]
    Permet de rafraîchir un token d'accès expiré.
    
    [Design principles]
    Validation stricte des refresh tokens pour maintenir la sécurité.
    Réutilisation du format Token comme réponse pour la cohérence.
    
    [Implementation details]
    Vérifie le refresh token, identifie l'utilisateur, puis génère un nouveau token d'accès.
    """
    try:
        # Vérifier et décoder le refresh token
        username = verify_refresh_token(refresh_data.refresh_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalide ou expiré"
        )
    
    # Vérifier que l'utilisateur existe toujours et est actif
    user = db.query(User).filter(User.username == username).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Compte utilisateur non trouvé ou désactivé"
        )
    
    # Générer un nouveau access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username,
        expires_delta=access_token_expires,
        role=user.role,
        groups=user.groups
    )
    
    # Préparer les données utilisateur
    user_data = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "department": user.department,
        "groups": user.groups
    }
    
    return {
        "token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "refresh_token": refresh_data.refresh_token,  # Renvoyer le même refresh token
        "user": user_data
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout():
    """
    [Function intent]
    Point de terminaison pour la déconnexion utilisateur.
    
    [Design principles]
    Endpoint RESTful simple avec statut 204 pour confirmer la réussite.
    
    [Implementation details]
    Aucune action côté serveur car les JWT sont stateless.
    La déconnexion réelle se fait côté client en supprimant les tokens.
    """
    # Les JWT sont stateless, la déconnexion est gérée côté client
    # Cet endpoint existe pour la cohérence de l'API REST
    return {}
