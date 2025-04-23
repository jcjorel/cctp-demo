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
# Serveur de services simulés pour le SRR, fournissant des API compatibles avec
# AD/LDAP et Exchange pour permettre le développement sans dépendre des services réels.
# Ce serveur mock expose des endpoints qui imitent le comportement des services externes.
###############################################################################
# [Source file design principles]
# - Simuler les comportements essentiels d'AD/LDAP et Exchange
# - Utiliser des données statiques de test chargées depuis des fichiers JSON
# - Fournir une API REST claire pour faciliter les tests et le développement
# - Implémenter une latence configurable pour simuler des conditions réseau réalistes
###############################################################################
# [Source file constraints]
# - Le serveur doit être compatible avec FastAPI et le reste de l'écosystème SRR
# - Les données de test doivent être chargées depuis les fichiers dans /app/data
# - Le serveur doit écouter sur le port 8080
###############################################################################
# [Dependencies]
# - services/mocks/data/users.json
# - services/mocks/data/resources.json
###############################################################################
# [GenAI tool change history]
# 2025-04-23T09:52:00Z : Création initiale du serveur mock pour AD/LDAP et Exchange par CodeAssistant
# * Implémentation de l'API d'authentification AD simulée
# * Implémentation des endpoints de recherche utilisateurs
# * Implémentation des endpoints de réservation Exchange simulés
###############################################################################

import json
import os
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr

# Définition des modèles de données
class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: str
    department: str
    active: bool
    groups: List[str]
    created_at: datetime

class Group(BaseModel):
    name: str
    description: str
    members: List[str]

class Feature(BaseModel):
    id: str
    name: str
    icon: str

class Resource(BaseModel):
    id: str
    name: str
    type: str
    capacity: int
    location: str
    features: List[str]
    email: EmailStr
    calendar_id: str
    status: str
    created_at: datetime
    manager: str

class Booking(BaseModel):
    id: str
    resource_id: str
    user_id: str
    title: str
    start_time: datetime
    end_time: datetime
    status: str
    attendees: List[str]
    created_at: datetime

class AuthRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    username: str
    success: bool
    token: Optional[str] = None
    error: Optional[str] = None
    user_info: Optional[Dict] = None

class ResourceAvailabilityRequest(BaseModel):
    resource_id: str
    start_time: datetime
    end_time: datetime

class BookingRequest(BaseModel):
    resource_id: str
    title: str
    start_time: datetime
    end_time: datetime
    attendees: List[str]
    description: Optional[str] = None

app = FastAPI(title="SRR Mock Services", description="Simulation des services AD/LDAP et Exchange")

# Configuration des CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, ce serait limité aux origines spécifiques
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales pour stocker les données mockées
USERS_DATA = {}
RESOURCES_DATA = {}
BOOKINGS_DATA = {}

# Paths des fichiers de données
MOCK_USERS_FILE = os.environ.get("MOCK_USERS_FILE", "/app/data/users.json")
MOCK_RESOURCES_FILE = os.environ.get("MOCK_RESOURCES_FILE", "/app/data/resources.json")

# Paramètre pour simuler la latence réseau (en secondes)
SIMULATED_DELAY = float(os.environ.get("SIMULATED_DELAY", "0.2"))

# Middleware pour simuler la latence réseau
@app.middleware("http")
async def add_simulated_delay(request: Request, call_next):
    """Simule une latence réseau pour les requêtes"""
    if SIMULATED_DELAY > 0:
        time.sleep(SIMULATED_DELAY)
    response = await call_next(request)
    return response

def load_mock_data():
    """Charge les données mockées depuis les fichiers JSON"""
    global USERS_DATA, RESOURCES_DATA, BOOKINGS_DATA
    
    # Chargement des données utilisateurs
    try:
        with open(MOCK_USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            USERS_DATA = {
                "users": data.get("users", []),
                "groups": data.get("groups", [])
            }
            print(f"✅ {len(USERS_DATA['users'])} utilisateurs et {len(USERS_DATA['groups'])} groupes chargés")
    except Exception as e:
        print(f"❌ Erreur lors du chargement des utilisateurs: {str(e)}")
        USERS_DATA = {"users": [], "groups": []}
    
    # Chargement des données ressources et réservations
    try:
        with open(MOCK_RESOURCES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            RESOURCES_DATA = {
                "resources": data.get("resources", []),
                "features": data.get("features", [])
            }
            BOOKINGS_DATA = {
                "bookings": data.get("bookings", [])
            }
            print(f"✅ {len(RESOURCES_DATA['resources'])} ressources et {len(BOOKINGS_DATA['bookings'])} réservations chargées")
    except Exception as e:
        print(f"❌ Erreur lors du chargement des ressources: {str(e)}")
        RESOURCES_DATA = {"resources": [], "features": []}
        BOOKINGS_DATA = {"bookings": []}

# Routes pour l'API AD/LDAP simulée
@app.post("/api/auth/login", response_model=AuthResponse)
def login(auth_request: AuthRequest):
    """Simule l'authentification AD"""
    for user in USERS_DATA["users"]:
        if user["username"] == auth_request.username:
            # Mot de passe simulé - dans un environnement réel, 
            # on vérifierait avec le hash bcrypt
            if user["active"]:
                # Token simulé
                token = f"mock_token_{uuid.uuid4()}"
                return {
                    "username": user["username"],
                    "success": True,
                    "token": token,
                    "user_info": {
                        "username": user["username"],
                        "email": user["email"],
                        "full_name": user["full_name"],
                        "role": user["role"],
                        "department": user["department"],
                        "groups": user["groups"]
                    }
                }
            else:
                return {
                    "username": user["username"],
                    "success": False,
                    "error": "Compte utilisateur inactif"
                }
    
    return {
        "username": auth_request.username,
        "success": False,
        "error": "Identifiants invalides"
    }

@app.get("/api/ad/users", response_model=List[User])
def get_users(
    query: Optional[str] = None,
    department: Optional[str] = None,
    active_only: bool = True
):
    """Récupère la liste des utilisateurs depuis AD"""
    filtered_users = []
    
    for user in USERS_DATA["users"]:
        # Filtre sur le statut actif
        if active_only and not user["active"]:
            continue
            
        # Filtre sur le département
        if department and user["department"] != department:
            continue
            
        # Filtre sur la recherche textuelle
        if query:
            query_lower = query.lower()
            if not (query_lower in user["username"].lower() or 
                    query_lower in user["full_name"].lower() or 
                    query_lower in user["email"].lower()):
                continue
                
        filtered_users.append(user)
    
    return filtered_users

@app.get("/api/ad/groups", response_model=List[Group])
def get_groups(name: Optional[str] = None):
    """Récupère la liste des groupes depuis AD"""
    if name:
        return [g for g in USERS_DATA["groups"] if name.lower() in g["name"].lower()]
    return USERS_DATA["groups"]

@app.get("/api/ad/users/{username}")
def get_user(username: str):
    """Récupère les informations d'un utilisateur spécifique depuis AD"""
    for user in USERS_DATA["users"]:
        if user["username"] == username:
            return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Utilisateur '{username}' non trouvé"
    )

@app.get("/api/ad/groups/{group_name}/members")
def get_group_members(group_name: str):
    """Récupère les membres d'un groupe spécifique"""
    for group in USERS_DATA["groups"]:
        if group["name"] == group_name:
            members = []
            for username in group["members"]:
                for user in USERS_DATA["users"]:
                    if user["username"] == username:
                        members.append(user)
                        break
            return members
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Groupe '{group_name}' non trouvé"
    )

# Routes pour l'API Exchange simulée
@app.get("/api/exchange/resources", response_model=List[Resource])
def get_resources(
    type: Optional[str] = None,
    feature: Optional[str] = None,
    capacity_min: Optional[int] = None,
    status: str = "active"
):
    """Récupère la liste des ressources depuis Exchange"""
    filtered_resources = []
    
    for resource in RESOURCES_DATA["resources"]:
        # Filtre sur le statut
        if resource["status"] != status:
            continue
            
        # Filtre sur le type
        if type and resource["type"] != type:
            continue
            
        # Filtre sur la capacité minimale
        if capacity_min and resource["capacity"] < capacity_min:
            continue
            
        # Filtre sur les équipements
        if feature and feature not in resource["features"]:
            continue
                
        filtered_resources.append(resource)
    
    return filtered_resources

@app.get("/api/exchange/resources/{resource_id}")
def get_resource(resource_id: str):
    """Récupère les informations d'une ressource spécifique depuis Exchange"""
    for resource in RESOURCES_DATA["resources"]:
        if resource["id"] == resource_id:
            return resource
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Ressource '{resource_id}' non trouvée"
    )

@app.get("/api/exchange/features")
def get_features():
    """Récupère la liste des équipements disponibles"""
    return RESOURCES_DATA["features"]

@app.post("/api/exchange/availability")
def check_availability(request: ResourceAvailabilityRequest):
    """Vérifie la disponibilité d'une ressource sur une plage horaire"""
    resource_found = False
    for resource in RESOURCES_DATA["resources"]:
        if resource["id"] == request.resource_id:
            resource_found = True
            
            # Vérifie si la ressource est en maintenance
            if resource["status"] != "active":
                return {
                    "available": False,
                    "reason": f"Ressource en {resource['status']}"
                }
            
            break
    
    if not resource_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ressource '{request.resource_id}' non trouvée"
        )
    
    # Vérifie les réservations existantes
    for booking in BOOKINGS_DATA["bookings"]:
        if booking["resource_id"] == request.resource_id and booking["status"] != "cancelled":
            # Vérifie si la plage horaire se chevauche avec une réservation existante
            booking_start = datetime.fromisoformat(booking["start_time"].replace('Z', '+00:00'))
            booking_end = datetime.fromisoformat(booking["end_time"].replace('Z', '+00:00'))
            
            request_start = request.start_time
            request_end = request.end_time
            
            if ((booking_start <= request_start < booking_end) or 
                (booking_start < request_end <= booking_end) or
                (request_start <= booking_start and booking_end <= request_end)):
                return {
                    "available": False,
                    "reason": f"Réservation existante: {booking['title']}",
                    "conflicting_booking": booking
                }
    
    # Aucun conflit trouvé
    return {
        "available": True
    }

@app.get("/api/exchange/bookings")
def get_bookings(
    resource_id: Optional[str] = None,
    user_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    status: Optional[str] = None
):
    """Récupère les réservations selon différents critères"""
    filtered_bookings = []
    
    for booking in BOOKINGS_DATA["bookings"]:
        # Filtre sur la ressource
        if resource_id and booking["resource_id"] != resource_id:
            continue
            
        # Filtre sur l'utilisateur (créateur ou participant)
        if user_id:
            if booking["user_id"] != user_id and user_id not in booking["attendees"]:
                continue
        
        # Filtre sur le statut
        if status and booking["status"] != status:
            continue
            
        # Filtre sur la plage de dates
        booking_start = datetime.fromisoformat(booking["start_time"].replace('Z', '+00:00'))
        booking_end = datetime.fromisoformat(booking["end_time"].replace('Z', '+00:00'))
        
        if start_date and booking_end < start_date:
            continue
            
        if end_date and booking_start > end_date:
            continue
                
        filtered_bookings.append(booking)
    
    return filtered_bookings

@app.get("/api/exchange/bookings/{booking_id}")
def get_booking(booking_id: str):
    """Récupère les détails d'une réservation spécifique"""
    for booking in BOOKINGS_DATA["bookings"]:
        if booking["id"] == booking_id:
            return booking
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Réservation '{booking_id}' non trouvée"
    )

@app.post("/api/exchange/bookings", status_code=status.HTTP_201_CREATED)
def create_booking(booking_request: BookingRequest):
    """Crée une nouvelle réservation (simulée)"""
    # Vérifie si la ressource existe
    resource_found = False
    for resource in RESOURCES_DATA["resources"]:
        if resource["id"] == booking_request.resource_id:
            if resource["status"] != "active":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ressource '{booking_request.resource_id}' non disponible (statut: {resource['status']})"
                )
            resource_found = True
            break
    
    if not resource_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ressource '{booking_request.resource_id}' non trouvée"
        )
    
    # Vérifie la disponibilité
    availability_check = check_availability(ResourceAvailabilityRequest(
        resource_id=booking_request.resource_id,
        start_time=booking_request.start_time,
        end_time=booking_request.end_time
    ))
    
    if not availability_check["available"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=availability_check["reason"]
        )
    
    # Crée une nouvelle réservation
    new_booking = {
        "id": f"booking-{uuid.uuid4().hex[:8]}",
        "resource_id": booking_request.resource_id,
        "user_id": "current-user",  # Simulé - dans la réalité, ce serait l'utilisateur authentifié
        "title": booking_request.title,
        "start_time": booking_request.start_time.isoformat(),
        "end_time": booking_request.end_time.isoformat(),
        "status": "pending",  # Par défaut, les réservations sont en attente
        "attendees": booking_request.attendees,
        "created_at": datetime.now().isoformat()
    }
    
    # Ajoute la nouvelle réservation aux données mockées
    BOOKINGS_DATA["bookings"].append(new_booking)
    
    return {
        "id": new_booking["id"],
        "message": "Réservation créée avec succès",
        "status": "pending",
        "booking": new_booking
    }

@app.put("/api/exchange/bookings/{booking_id}/status")
def update_booking_status(booking_id: str, status: str = Query(..., regex="^(confirmed|cancelled)$")):
    """Met à jour le statut d'une réservation"""
    for booking in BOOKINGS_DATA["bookings"]:
        if booking["id"] == booking_id:
            booking["status"] = status
            return {
                "message": f"Statut de la réservation mis à jour: {status}",
                "booking": booking
            }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Réservation '{booking_id}' non trouvée"
    )

@app.get("/health")
def health_check():
    """Point de terminaison pour vérifier la santé du service"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "mock-services",
        "data_loaded": {
            "users": len(USERS_DATA["users"]),
            "groups": len(USERS_DATA["groups"]),
            "resources": len(RESOURCES_DATA["resources"]),
            "bookings": len(BOOKINGS_DATA["bookings"])
        }
    }

@app.on_event("startup")
def startup_event():
    """Événement de démarrage pour charger les données mockées"""
    print("🚀 Démarrage du serveur de services simulés SRR...")
    load_mock_data()

if __name__ == "__main__":
    # Démarre l'application avec uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
