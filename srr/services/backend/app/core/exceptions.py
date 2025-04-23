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
# Fournit un système centralisé de gestion des exceptions et des erreurs pour l'API.
# Ce module assure la cohérence des réponses d'erreur à travers l'ensemble de l'API
# et facilite la fourniture de messages d'erreur pertinents aux clients.
###############################################################################
# [Source file design principles]
# - Standardisation de la structure des réponses d'erreur
# - Centralisation des handlers d'exceptions
# - Hiérarchie d'exceptions personnalisées pour une gestion fine des erreurs métier
# - Séparation entre les exceptions et leur transformation en réponses HTTP
# - Facilité d'extension pour de nouveaux types d'erreurs
###############################################################################
# [Source file constraints]
# - Toutes les exceptions doivent pouvoir être sérialisées en JSON
# - Les messages d'erreur doivent être informatifs mais ne pas exposer de détails sensibles
# - Respecter la norme HTTP pour les codes de statut
# - Assurer la compatibilité avec le middleware CORS de FastAPI
###############################################################################
# [Dependencies]
# - fastapi: FastAPI, HTTPException, Request, status
# - pydantic: ValidationError
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:07:30Z : Création initiale du module d'exceptions par CodeAssistant
# * Définition de la classe APIError pour les erreurs personnalisées
# * Implémentation des handlers d'exceptions pour FastAPI
# * Configuration des réponses d'erreur standardisées
###############################################################################

from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError


class APIError(Exception):
    """
    [Class intent]
    Exception personnalisée pour les erreurs de l'API avec format standardisé.
    
    [Design principles]
    Standardisation des réponses d'erreur à travers l'API.
    Structure cohérente avec code, message et détails.
    
    [Implementation details]
    Permet de spécifier un code d'erreur, un message et des détails additionnels.
    Prend en charge la sérialisation en JSON pour les réponses HTTP.
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
    Centralisation du format de réponse d'erreur.
    Cohérence dans la structure des erreurs renvoyées au client.
    
    [Implementation details]
    Enregistre des handlers pour les exceptions courantes et personnalisées
    avec un format JSON standardisé.
    
    Args:
        app: Application FastAPI à laquelle ajouter les handlers
    """
    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
        """
        [Function intent]
        Gère les exceptions APIError personnalisées et les transforme en réponses JSON.
        
        [Design principles]
        Format standardisé pour toutes les erreurs métier.
        
        [Implementation details]
        Extrait les données de l'exception et construit une réponse au format standard.
        """
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
        """
        [Function intent]
        Gère les erreurs de validation de requête et les transforme en réponses JSON.
        
        [Design principles]
        Format standardisé pour les erreurs de validation.
        Informations détaillées pour faciliter le débogage côté client.
        
        [Implementation details]
        Transforme les erreurs de validation Pydantic en format d'erreur standardisé.
        """
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Erreur de validation des données de la requête",
                    "details": {
                        "errors": format_validation_errors(exc.errors())
                    }
                }
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """
        [Function intent]
        Gère les exceptions HTTP standard et les transforme en réponses JSON.
        
        [Design principles]
        Uniformise le format de toutes les erreurs HTTP.
        
        [Implementation details]
        Convertit les HTTPException en format d'erreur standardisé.
        """
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
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        [Function intent]
        Gère les exceptions non capturées et les transforme en réponses JSON.
        
        [Design principles]
        Capture de sécurité pour toutes les exceptions non gérées.
        
        [Implementation details]
        Transforme les exceptions génériques en erreurs 500 avec message générique.
        """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Une erreur interne s'est produite",
                    "details": {
                        "type": str(type(exc).__name__)
                    }
                }
            }
        )


def format_validation_errors(errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    [Function intent]
    Formate les erreurs de validation Pydantic pour une meilleure lisibilité.
    
    [Design principles]
    Transformation des messages techniques en informations exploitables.
    
    [Implementation details]
    Restructure les erreurs pour fournir des informations claires sur la localisation et la nature de l'erreur.
    
    Args:
        errors: Liste des erreurs de validation Pydantic
        
    Returns:
        Liste formatée des erreurs pour l'API
    """
    formatted_errors = []
    for error in errors:
        formatted_errors.append({
            "location": error.get("loc", []),
            "message": error.get("msg"),
            "type": error.get("type")
        })
    return formatted_errors
