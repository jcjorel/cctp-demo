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
# Fournit une simulation du service AD/LDAP pour l'environnement de développement.
# Ce module permet de tester les fonctionnalités d'authentification et d'autorisation
# sans nécessiter une connexion à un véritable service d'annuaire en phase de développement.
###############################################################################
# [Source file design principles]
# - Simulation simple mais réaliste du comportement d'AD/LDAP
# - Données de test représentatives des différents profils d'utilisateurs
# - Configuration flexible via variables d'environnement
# - Séparation complète avec le code de production
# - Interface compatible avec celle qui serait utilisée pour un vrai service AD
###############################################################################
# [Source file constraints]
# - Utilisation réservée à l'environnement de développement uniquement
# - Ne doit pas être utilisé en production
# - Les mots de passe de test doivent être clairement identifiés comme tels
# - Les données de test doivent couvrir tous les cas d'utilisation nécessaires
###############################################################################
# [Dependencies]
# - app/core/config.py: Configuration centrale (paramètres MOCK_*)
# - json: Parsing des fichiers de données
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:09:40Z : Création initiale du module mock_ad par CodeAssistant
# * Implémentation des fonctions de simulation AD/LDAP
# * Configuration du chargement des données depuis fichiers ou mémoire
# * Création des utilisateurs de test par défaut
###############################################################################

import json
import logging
import os
from typing import Dict, List, Optional, Any

from app.core.config import settings
from app.core.security import verify_password

# Configuration du logger
logger = logging.getLogger(__name__)

# Utilisateurs de test par défaut (utilisés si aucun fichier n'est spécifié)
DEFAULT_MOCK_USERS = [
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "Admin Système",
        "roles": ["admin", "user"],
        "department": "DSI",
        "organization": "Mairie",
        "position": "Administrateur système",
        "active": True,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "username": "user",
        "email": "user@example.com",
        "full_name": "Utilisateur Standard",
        "roles": ["user"],
        "department": "Service culturel",
        "organization": "Mairie",
        "position": "Agent administratif",
        "active": True,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "username": "manager",
        "email": "manager@example.com",
        "full_name": "Gestionnaire de Ressources",
        "roles": ["resource_manager", "user"],
        "department": "Services Généraux",
        "organization": "Mairie",
        "position": "Responsable logistique",
        "active": True,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440003",
        "username": "inactive",
        "email": "inactive@example.com",
        "full_name": "Compte Désactivé",
        "roles": ["user"],
        "department": "Service technique",
        "organization": "Mairie",
        "position": "Agent technique",
        "active": False,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
    },
]

# Cache des utilisateurs chargés
_mock_users = None


def _load_mock_users() -> List[Dict[str, Any]]:
    """
    [Function intent]
    Charge les utilisateurs mock depuis un fichier ou utilise les valeurs par défaut.
    
    [Design principles]
    Lazy loading des données de test.
    Priorité au fichier de configuration externe si disponible.
    
    [Implementation details]
    Tente de charger depuis un fichier JSON, avec fallback sur les utilisateurs par défaut.
    Met en cache les utilisateurs pour éviter de multiples chargements.
    """
    global _mock_users
    
    if _mock_users is not None:
        return _mock_users
        
    if settings.MOCK_USERS_FILE and os.path.exists(settings.MOCK_USERS_FILE):
        try:
            with open(settings.MOCK_USERS_FILE, "r", encoding="utf-8") as f:
                logger.info(f"Chargement des utilisateurs mock depuis {settings.MOCK_USERS_FILE}")
                _mock_users = json.load(f)
                return _mock_users
        except Exception as e:
            logger.warning(f"Erreur lors du chargement des utilisateurs mock depuis fichier: {e}")
            
    logger.info("Utilisation des utilisateurs mock par défaut")
    _mock_users = DEFAULT_MOCK_USERS
    return _mock_users


def get_mock_user(username: str) -> Optional[Dict[str, Any]]:
    """
    [Function intent]
    Récupère un utilisateur simulé par son nom d'utilisateur.
    
    [Design principles]
    Interface simple simulant un service d'annuaire.
    
    [Implementation details]
    Recherche dans la liste des utilisateurs chargée depuis le fichier ou par défaut.
    
    Args:
        username: Nom d'utilisateur à rechercher
        
    Returns:
        Dict | None: Données utilisateur si trouvé, None sinon
    """
    users = _load_mock_users()
    for user in users:
        if user["username"].lower() == username.lower():
            return user
    return None


def authenticate_mock_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    [Function intent]
    Authentifie un utilisateur simulé avec son nom d'utilisateur et mot de passe.
    
    [Design principles]
    Simulation réaliste du processus d'authentification.
    
    [Implementation details]
    Vérifie l'existence de l'utilisateur, son état actif et son mot de passe.
    
    Args:
        username: Nom d'utilisateur
        password: Mot de passe en clair
        
    Returns:
        Dict | None: Données utilisateur si authentification réussie, None sinon
    """
    user = get_mock_user(username)
    
    # Vérifications de base
    if not user:
        logger.warning(f"Tentative d'authentification pour un utilisateur inexistant: {username}")
        return None
        
    if not user.get("active", True):
        logger.warning(f"Tentative d'authentification pour un compte inactif: {username}")
        return None
    
    # En mode développement, on peut simplifier avec un mot de passe commun
    if settings.DEBUG and password == "password":
        logger.info(f"Authentification simplifiée en mode DEBUG pour: {username}")
        return user
    
    # Vérification normale du mot de passe
    if not verify_password(password, user["hashed_password"]):
        logger.warning(f"Échec d'authentification (mot de passe incorrect): {username}")
        return None
        
    logger.info(f"Authentification réussie pour: {username}")
    return user


def get_all_mock_users() -> List[Dict[str, Any]]:
    """
    [Function intent]
    Récupère tous les utilisateurs simulés.
    
    [Design principles]
    Fournit une liste complète pour les fonctionnalités d'administration.
    
    [Implementation details]
    Retourne une copie des données pour éviter les modifications accidentelles.
    
    Returns:
        List[Dict]: Liste de tous les utilisateurs simulés
    """
    users = _load_mock_users()
    return users.copy()


def get_mock_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """
    [Function intent]
    Récupère un utilisateur simulé par son ID.
    
    [Design principles]
    Complétion de l'API mock pour la recherche par différents critères.
    
    [Implementation details]
    Recherche dans la liste des utilisateurs chargée depuis le fichier ou par défaut.
    
    Args:
        user_id: ID de l'utilisateur à rechercher
        
    Returns:
        Dict | None: Données utilisateur si trouvé, None sinon
    """
    users = _load_mock_users()
    for user in users:
        if user["id"] == user_id:
            return user
    return None


def search_mock_users(query: str = "", department: str = None, role: str = None) -> List[Dict[str, Any]]:
    """
    [Function intent]
    Recherche des utilisateurs selon différents critères.
    
    [Design principles]
    Simulation des fonctionnalités de recherche d'annuaire.
    
    [Implementation details]
    Filtre la liste des utilisateurs selon les critères fournis.
    
    Args:
        query: Texte à rechercher dans username, email ou full_name
        department: Filtrer par département
        role: Filtrer par rôle
        
    Returns:
        List[Dict]: Liste des utilisateurs correspondant aux critères
    """
    users = _load_mock_users()
    results = []
    
    query = query.lower()
    
    for user in users:
        # Filtre par recherche textuelle
        if query:
            if not (
                query in user.get("username", "").lower() or
                query in user.get("email", "").lower() or
                query in user.get("full_name", "").lower()
            ):
                continue
                
        # Filtre par département
        if department and user.get("department") != department:
            continue
            
        # Filtre par rôle
        if role and role not in user.get("roles", []):
            continue
            
        results.append(user.copy())
        
    return results
