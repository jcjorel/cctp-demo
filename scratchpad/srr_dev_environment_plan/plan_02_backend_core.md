# Plan du Backend Core - Environnement de Développement SRR

## Objectifs Spécifiques

Ce plan détaille la structure et les composants principaux du backend FastAPI pour l'environnement de développement minimaliste du SRR. L'objectif est de mettre en place une architecture backend modulaire, maintenable et extensible qui servira de fondation pour implémenter les fonctionnalités du système.

## Dépendances

- [plan_01_infrastructure.md](./plan_01_infrastructure.md) : Infrastructure Docker et services
- Référence aux principes définis dans [DESIGN.md](/doc/DESIGN.md), section "7. ARCHITECTURE BACKEND"
- Référence au modèle défini dans [DATA_MODEL.md](/doc/DATA_MODEL.md)

## Structure du Projet Backend

```
backend/
├── alembic/                  # Migrations de base de données
│   ├── versions/             # Scripts de migration
│   ├── env.py                # Configuration Alembic
│   └── script.py.mako        # Template de migration
├── app/
│   ├── api/                  # Endpoints API
│   │   ├── __init__.py
│   │   ├── deps.py           # Dépendances partagées (injection)
│   │   └── v1/               # Version 1 de l'API
│   │       ├── __init__.py
│   │       ├── endpoints/     # Endpoints groupés par domaine
│   │       │   ├── __init__.py
│   │       │   ├── auth.py   # Authentication endpoints
│   │       │   ├── resources.py  # Resource endpoints
│   │       │   └── bookings.py   # Booking endpoints
│   │       └── router.py      # Router principal v1
│   ├── core/                  # Configuration et utilitaires centraux
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration et variables d'environnement
│   │   ├── security.py        # Utils d'authentification et sécurité
│   │   └── exceptions.py      # Exceptions personnalisées
│   ├── db/                    # Connexion et utilitaires DB
│   │   ├── __init__.py
│   │   ├── session.py         # Configuration Session SQLAlchemy
│   │   └── base.py            # Classe Base des modèles
│   ├── models/                # Modèles SQLAlchemy
│   │   ├── __init__.py
│   │   ├── user.py            # Modèle User 
│   │   ├── resource.py        # Modèle Resource et ResourceType
│   │   └── booking.py         # Modèle Booking
│   ├── schemas/               # Schémas Pydantic
│   │   ├── __init__.py
│   │   ├── base.py            # Schémas de base
│   │   ├── user.py            # Schémas User
│   │   ├── resource.py        # Schémas Resource
│   │   └── booking.py         # Schémas Booking
│   ├── services/              # Services/Logique métier
│   │   ├── __init__.py
│   │   ├── auth.py            # Service d'authentification
│   │   ├── resource.py        # Service de gestion des ressources
│   │   └── booking.py         # Service de réservation 
│   └── utils/                 # Utilitaires
│       ├── __init__.py
│       ├── mock_ad.py         # Mock du service AD/LDAP
│       └── mock_exchange.py   # Mock du service Exchange
├── tests/                     # Tests
│   ├── __init__.py
│   ├── conftest.py            # Fixtures de test
│   ├── api/                   # Tests des endpoints API
│   └── services/              # Tests des services
├── .env                        # Variables d'environnement locales
├── alembic.ini                 # Configuration Alembic
├── main.py                     # Point d'entrée de l'application
├── requirements.txt            # Dépendances
└── README.md                   # Documentation
```

## Composants à Implémenter

### 1. Configuration de l'Application

La configuration sera gérée via un module dédié avec chargement des variables d'environnement et valeurs par défaut.

```python
# app/core/config.py
from pydantic_settings import BaseSettings
import secrets
from typing import List, Optional

class Settings(BaseSettings):
    """
    [Class intent]
    Gère la configuration de l'application via variables d'environnement et valeurs par défaut.
    
    [Design principles]
    Utilisation de Pydantic pour la validation des variables d'environnement.
    Valeurs par défaut sécurisées pour le développement.
    
    [Implementation details]
    Les variables sont lues depuis .env ou variables d'environnement système.
    Utilisation de hiérarchie de priorité: variables système > .env > valeurs par défaut.
    """
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Système de Réservation de Ressources"
    
    # SECURITY
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@db:5432/srr_dev"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Mock Settings
    MOCK_AUTH: bool = True
    MOCK_EXCHANGE: bool = True
    
    # Environment
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 2. Point d'Entrée Principal

Le point d'entrée créera et configurera l'application FastAPI.

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.v1.router import api_router
from app.core.config import settings

def create_app() -> FastAPI:
    """
    [Function intent]
    Crée et configure une instance de l'application FastAPI.
    
    [Design principles]
    Configuration centralisée de l'application.
    Séparation claire des préoccupations.
    
    [Implementation details]
    Initialise l'application avec les middlewares, routers et gestionnaires d'événements.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API pour la réservation et gestion des ressources partagées",
        version="0.1.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        debug=settings.DEBUG,
    )
    
    # Set up CORS
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    @app.get("/")
    def root():
        return {"message": "Welcome to SRR API. See /api/v1/docs for documentation."}
    
    @app.get("/health")
    def health_check():
        return {"status": "healthy", "version": "0.1.0"}
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### 3. Router Principal

Le router principal aggrège les différents endpoints de l'API.

```python
# app/api/v1/router.py
from fastapi import APIRouter

from app.api.v1.endpoints import auth, resources, bookings

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(resources.router, prefix="/resources", tags=["resources"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
```

### 4. Dépendances Partagées

Module centralisant les dépendances partagées pour l'injection de dépendances FastAPI.

```python
# app/api/deps.py
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.services.auth import get_user_by_username
from app.schemas.user import UserInDB, TokenPayload

# Réutilisation de la session de base de données
def get_db() -> Generator:
    """
    [Function intent]
    Fournit une session de base de données et assure sa fermeture.
    
    [Design principles]
    Pattern Unit-of-Work pour isolation des transactions.
    
    [Implementation details]
    Utilisation du contexte Python pour garantir la fermeture de session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Système d'authentification OAuth2
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

# Dépendance pour obtenir l'utilisateur courant
def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    [Function intent]
    Récupère l'utilisateur authentifié à partir du token JWT.
    
    [Design principles]
    Validation systématique du token avant accès aux ressources protégées.
    
    [Implementation details]
    Décodage du token JWT et vérification de l'existence de l'utilisateur.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Informations d'identification invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if settings.MOCK_AUTH:
        # Mode développement avec mock utilisateurs
        from app.utils.mock_ad import get_mock_user
        user = get_mock_user(token_data.sub)
    else:
        user = get_user_by_username(db, username=token_data.sub)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Utilisateur non trouvé"
        )
    return user

# Vérification des rôles/permissions
def get_current_active_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    [Function intent]
    Vérifie que l'utilisateur courant a des droits d'administrateur.
    
    [Design principles]
    Séparation des préoccupations pour l'autorisation.
    
    [Implementation details]
    Validation du rôle 'admin' dans la liste des rôles de l'utilisateur.
    """
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Droits d'administration requis",
        )
    return current_user
```

### 5. Security

Module gérant l'authentification, génération de tokens, et validation.

```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Any, Union, Optional

from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    [Function intent]
    Génère un token JWT d'authentification.
    
    [Design principles]
    Sécurisation des tokens avec temps d'expiration.
    
    [Implementation details]
    Encodage des claims standards JWT avec la bibliothèque jose.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
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
    
    [Implementation details]
    Délègue la comparaison au contexte de hachage.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    [Function intent]
    Génère un hash sécurisé pour un mot de passe.
    
    [Design principles]
    Utilisation de bcrypt pour un hachage fort.
    
    [Implementation details]
    Délègue le hachage au contexte de hachage configuré.
    """
    return pwd_context.hash(password)
```

### 6. Gestion des Exceptions

Configuration personnalisée des exceptions et des réponses d'erreur.

```python
# app/core/exceptions.py
from typing import Any, Dict, Optional

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from pydantic import ValidationError

class APIError(Exception):
    """
    [Class intent]
    Exception personnalisée pour les erreurs de l'API.
    
    [Design principles]
    Standardisation des réponses d'erreur à travers l'API.
    
    [Implementation details]
    Permet de spécifier un code d'erreur, un message et des détails.
    """
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

def add_exception_handlers(app: FastAPI) -> None:
    """
    [Function intent]
    Configure les gestionnaires d'exceptions pour l'application FastAPI.
    
    [Design principles]
    Centralisation des formats de réponse d'erreur.
    
    [Implementation details]
    Enregistre des gestionnaires pour les exceptions courantes et personnalisées.
    """
    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Erreur de validation des données",
                    "details": {
                        "errors": exc.errors()
                    }
                }
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": f"HTTP_ERROR_{exc.status_code}",
                    "message": exc.detail,
                    "details": {}
                }
            },
            headers=exc.headers
        )

# Exemple d'utilisation dans un endpoint:
# raise APIError(
#     status_code=400,
#     code="RESOURCE_NOT_AVAILABLE",
#     message="La ressource n'est pas disponible",
#     details={"resource_id": resource_id, "conflict": conflict_info}
# )
```

### 7. Session Base de Données

Configuration de la connexion à la base de données.

```python
# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL en mode debug
    pool_pre_ping=True,   # Vérification de connexion
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

### 8. Exemple d'Endpoint Minimal

Endpoint d'authentification simplifié.

```python
# app/api/v1/endpoints/auth.py
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.user import Token, UserResponse
from app.services.auth import authenticate_user

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    [Function intent]
    Authentifie un utilisateur et génère un token JWT.
    
    [Design principles]
    Utilisation du flow standard OAuth2 pour compatibilité.
    
    [Implementation details]
    Validation des identifiants et génération d'un token avec durée de validité.
    """
    if settings.MOCK_AUTH:
        # Mode développement avec mock utilisateurs
        from app.utils.mock_ad import authenticate_mock_user
        user = authenticate_mock_user(form_data.username, form_data.password)
    else:
        user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            subject=user.username, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
```

### 9. Utilitaire de Mock pour AD/LDAP

Simulation simplifiée des services externes pour le développement.

```python
# app/utils/mock_ad.py
from typing import Dict, List, Optional
import json
import os

# Utilisateurs simulés
MOCK_USERS = [
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "Admin Système",
        "roles": ["admin", "user"],
        "department": "DSI",
        "position": "Administrateur système",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "username": "user",
        "email": "user@example.com",
        "full_name": "Utilisateur Standard",
        "roles": ["user"],
        "department": "Marketing",
        "position": "Chef de projet",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "username": "manager",
        "email": "manager@example.com",
        "full_name": "Gestionnaire de Ressources",
        "roles": ["resource_manager", "user"],
        "department": "Services Généraux",
        "position": "Responsable logistique",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
    },
]

# Charge les utilisateurs depuis un fichier si spécifié
if os.environ.get("MOCK_USERS_FILE"):
    try:
        with open(os.environ["MOCK_USERS_FILE"], "r") as f:
            MOCK_USERS = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback sur les utilisateurs par défaut
        pass

def get_mock_user(username: str) -> Optional[Dict]:
    """
    [Function intent]
    Récupère un utilisateur simulé par son nom d'utilisateur.
    
    [Design principles]
    Simulation simple pour le développement sans dépendance externe.
    
    [Implementation details]
    Recherche dans une liste en mémoire, pas de persistance.
    """
    for user in MOCK_USERS:
        if user["username"] == username:
            return user
    return None

def authenticate_mock_user(username: str, password: str) -> Optional[Dict]:
    """
    [Function intent]
    Authentifie un utilisateur simulé avec son nom d'utilisateur et mot de passe.
    
    [Design principles]
    Simulation simple pour le développement sans dépendance externe.
    
    [Implementation details]
    En mode dev, accepte "password" pour tous les utilisateurs.
    """
    user = get_mock_user(username)
    if user and password == "password":  # Simplification pour le développement
        return user
    return None

def get_all_mock_users() -> List[Dict]:
    """
    [Function intent]
    Récupère tous les utilisateurs simulés.
    
    [Design principles]
    Fournit des données de test complètes pour le développement.
    
    [Implementation details]
    Retourne une copie de la liste pour éviter les modifications accidentelles.
    """
    return MOCK_USERS.copy()
```

## Dépendances Python

Liste des dépendances requises pour le backend.

```
# requirements.txt
fastapi==0.103.1
uvicorn[standard]==0.23.2
sqlalchemy==2.0.20
alembic==1.12.0
pydantic==2.3.0
pydantic-settings==2.0.3
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
psycopg2-binary==2.9.7
redis==4.6.0
pytest==7.4.2
httpx==0.24.1
```

## Implémentation Étape par Étape

1. **Création de la structure**
   - Mettre en place la structure de répertoires décrite ci-dessus
   - Créer les fichiers `__init__.py` pour définir les packages Python

2. **Configuration de base**
   - Implémenter le module de configuration (`config.py`)
   - Créer le point d'entrée principal (`main.py`)
   - Configurer les dépendances partagées (`deps.py`)

3. **Connexion à la base de données**
   - Configurer SQLAlchemy (`session.py`, `base.py`)
   - Préparer Alembic pour les migrations

4. **Services de base**
   - Implémenter le module de sécurité (`security.py`)
   - Configurer la gestion des exceptions (`exceptions.py`)
   - Créer les premiers endpoints d'authentification

5. **Services mock**
   - Implémenter les mocks AD/LDAP et Exchange pour le développement

## Considérations de Sécurité

- Ne pas inclure de secrets dans le code source
- Utiliser des variables d'environnement ou dotenv pour la configuration
- Sécuriser les endpoints avec des validations appropriées
- Implémenter la validation JWT pour les endpoints protégés
- Utiliser HTTPS même en développement local (CORS correctement configuré)

## Critères de Validation

- ✅ L'application FastAPI démarre correctement
- ✅ Les endpoints de base sont accessibles
- ✅ La documentation OpenAPI est générée correctement
- ✅ Les tests unitaires de base passent
- ✅ La connexion à la base de données fonctionne
- ✅ Le système d'authentification de base fonctionne

## Notes Importantes

- Le code fourni est un squelette et nécessite des implémentations complètes
- En mode développement, les mocks remplacent les services externes
- Les modèles complets seront définis dans le plan de base de données
- L'implémentation des règles métier complexes n'est pas incluse à ce stade (focus sur l'architecture)

## Références

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation SQLAlchemy](https://docs.sqlalchemy.org/en/14/)
- [DESIGN.md](/doc/DESIGN.md), section "7. ARCHITECTURE BACKEND"
- [DATA_MODEL.md](/doc/DATA_MODEL.md) pour les modèles de données
