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
# Fournit des données initiales pour le développement et les tests.
# Ce script permet d'initialiser la base de données avec un jeu de données représentatif
# pour faciliter le développement et les tests manuels de l'application.
###############################################################################
# [Source file design principles]
# - Création de données cohérentes et réalistes pour tous les modèles
# - Relations correctement établies entre les entités
# - Support de la réexécution sans duplication
# - Indépendance des ID pour la reproductibilité
# - Organisation claire par type d'entité
###############################################################################
# [Source file constraints]
# - Utilisation uniquement en environnement de développement/test
# - Ne doit pas être utilisé en production
# - Les données générées doivent couvrir les cas d'utilisation essentiels
# - Les UUID doivent être fixes pour garantir la reproductibilité
###############################################################################
# [Dependencies]
# - app/db/session: Session SQLAlchemy
# - app/models/*: Modèles de l'application
# - datetime: Manipulation des dates
# - uuid: Génération d'UUID fixes
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:23:40Z : Création initiale du script de données de test par CodeAssistant
# * Implémentation de la création d'utilisateurs de test
# * Implémentation de la création de types de ressource et ressources
# * Implémentation de la création de réservations et approbations
###############################################################################

import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.models.resource_type import ResourceType
from app.models.resource import Resource
from app.models.booking import Booking, BookingStatus
from app.models.booking_approval import BookingApproval, ApprovalStatus


def create_sample_data():
    """
    [Function intent]
    Génère des données d'exemple pour le développement et tests.
    
    [Design principles]
    Fournit un jeu de données minimal mais suffisant pour tester les fonctionnalités.
    
    [Implementation details]
    Insère des utilisateurs, types de ressources, ressources, réservations et approbations.
    Vérifie préalablement si des données existent déjà pour éviter les duplications.
    """
    db = SessionLocal()
    try:
        # Vérifier si des données existent déjà
        if db.query(User).count() > 0:
            print("Des données existent déjà. Annulation de la création des données d'exemple.")
            return
        
        print("Création des données d'exemple...")
        
        # Création des utilisateurs
        users = [
            User(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440000"),
                username="admin",
                email="admin@example.com",
                full_name="Admin Système",
                roles=["admin", "user"],
                department="DSI",
                organization="Mairie",
                position="Administrateur système",
                active=True,
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
            ),
            User(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440001"),
                username="user",
                email="user@example.com",
                full_name="Utilisateur Standard",
                roles=["user"],
                department="Service culturel",
                organization="Mairie",
                position="Agent administratif",
                active=True,
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
            ),
            User(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440002"),
                username="manager",
                email="manager@example.com",
                full_name="Gestionnaire de Ressources",
                roles=["resource_manager", "user"],
                department="Services Généraux",
                organization="Mairie",
                position="Responsable logistique",
                active=True,
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
            ),
            User(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440003"),
                username="inactive",
                email="inactive@example.com",
                full_name="Compte Désactivé",
                roles=["user"],
                department="Service technique",
                organization="Mairie",
                position="Agent technique",
                active=False,
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
            ),
        ]
        db.add_all(users)
        db.flush()
        print(f"✅ {len(users)} utilisateurs créés")
        
        # Création des types de ressources
        
        # Salle de réunion
        meeting_room_schema = {
            "properties": {
                "floor": {
                    "type": "integer",
                    "description": "Étage où se trouve la salle",
                    "minimum": 0
                },
                "has_projector": {
                    "type": "boolean",
                    "description": "Présence d'un projecteur"
                },
                "capacity": {
                    "type": "integer",
                    "description": "Nombre maximum de personnes",
                    "minimum": 1
                },
                "layout": {
                    "type": "string",
                    "enum": ["u_shape", "classroom", "boardroom", "theater"],
                    "description": "Configuration de la salle"
                }
            },
            "required": ["floor", "capacity", "layout"]
        }
        
        # Véhicule
        vehicle_schema = {
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["car", "van", "truck"],
                    "description": "Type de véhicule"
                },
                "seats": {
                    "type": "integer",
                    "description": "Nombre de places",
                    "minimum": 1
                },
                "fuel": {
                    "type": "string",
                    "enum": ["gas", "diesel", "electric", "hybrid"],
                    "description": "Type de carburant"
                },
                "license_plate": {
                    "type": "string",
                    "description": "Plaque d'immatriculation"
                }
            },
            "required": ["type", "seats", "license_plate"]
        }
        
        # Équipement informatique
        it_equipment_schema = {
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["laptop", "tablet", "projector", "printer"],
                    "description": "Type d'équipement"
                },
                "brand": {
                    "type": "string",
                    "description": "Marque de l'équipement"
                },
                "model": {
                    "type": "string",
                    "description": "Modèle de l'équipement"
                },
                "serial_number": {
                    "type": "string",
                    "description": "Numéro de série"
                }
            },
            "required": ["type", "brand", "serial_number"]
        }
        
        resource_types = [
            ResourceType(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440010"),
                name="Salle de réunion",
                description="Espaces pour réunions et événements",
                schema=meeting_room_schema,
                required_properties=["floor", "capacity", "layout"],
            ),
            ResourceType(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440011"),
                name="Véhicule",
                description="Véhicules de service",
                schema=vehicle_schema,
                required_properties=["type", "seats", "license_plate"],
            ),
            ResourceType(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440012"),
                name="Équipement informatique",
                description="Matériel informatique et audiovisuel",
                schema=it_equipment_schema,
                required_properties=["type", "brand", "serial_number"],
            ),
        ]
        db.add_all(resource_types)
        db.flush()
        print(f"✅ {len(resource_types)} types de ressources créés")
        
        # Création des ressources
        resources = [
            # Salles de réunion
            Resource(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440020"),
                name="Salle Neptune",
                description="Grande salle de réunion avec vue sur le parc",
                resource_type_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440010"),
                properties={
                    "floor": 2,
                    "has_projector": True,
                    "capacity": 20,
                    "layout": "boardroom"
                },
                requires_approval=False,
            ),
            Resource(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440021"),
                name="Salle Jupiter",
                description="Salle de conférence pour présentations importantes",
                resource_type_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440010"),
                properties={
                    "floor": 3,
                    "has_projector": True,
                    "capacity": 50,
                    "layout": "theater"
                },
                requires_approval=True,
            ),
            
            # Véhicules
            Resource(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440022"),
                name="Renault Clio Service",
                description="Véhicule de service compact",
                resource_type_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440011"),
                properties={
                    "type": "car",
                    "seats": 5,
                    "fuel": "gas",
                    "license_plate": "AA-123-BB"
                },
                requires_approval=True,
            ),
            
            # Équipement informatique
            Resource(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440023"),
                name="Projecteur portable",
                description="Projecteur HD portable pour présentations",
                resource_type_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440012"),
                properties={
                    "type": "projector",
                    "brand": "Epson",
                    "model": "EB-X41",
                    "serial_number": "EPSON12345"
                },
                requires_approval=False,
            ),
        ]
        db.add_all(resources)
        db.flush()
        print(f"✅ {len(resources)} ressources créées")
        
        # Association de gestionnaires aux ressources
        resources[1].managers.append(users[2])  # manager gère Jupiter
        resources[2].managers.append(users[2])  # manager gère Renault Clio
        db.flush()
        print("✅ Gestionnaires assignés aux ressources")
        
        # Création des réservations
        now = datetime.now()
        bookings = [
            # Réservation passée confirmée
            Booking(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440030"),
                resource_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440020"),  # Neptune
                user_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440001"),      # user
                start_time=now - timedelta(days=2, hours=2),
                end_time=now - timedelta(days=2),
                status=BookingStatus.COMPLETED.value,
                purpose="Réunion de service passée",
            ),
            
            # Réservation future confirmée
            Booking(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440031"),
                resource_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440020"),  # Neptune
                user_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440001"),      # user
                start_time=now + timedelta(days=1, hours=10),
                end_time=now + timedelta(days=1, hours=12),
                status=BookingStatus.CONFIRMED.value,
                purpose="Réunion d'équipe",
            ),
            
            # Réservation en attente d'approbation
            Booking(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440032"),
                resource_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440021"),  # Jupiter
                user_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440001"),      # user
                start_time=now + timedelta(days=2, hours=14),
                end_time=now + timedelta(days=2, hours=16),
                status=BookingStatus.PENDING.value,
                purpose="Présentation projet XYZ",
            ),
            
            # Réservation véhicule en attente
            Booking(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440033"),
                resource_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440022"),  # Clio
                user_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440000"),      # admin
                start_time=now + timedelta(days=3, hours=9),
                end_time=now + timedelta(days=3, hours=17),
                status=BookingStatus.PENDING.value,
                purpose="Déplacement réunion externe",
            ),
        ]
        db.add_all(bookings)
        db.flush()
        print(f"✅ {len(bookings)} réservations créées")
        
        # Création des approbations
        approvals = [
            # Approbation en attente
            BookingApproval(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440040"),
                booking_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440032"),  # Jupiter
                approver_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440002"),  # manager
                status=ApprovalStatus.PENDING.value,
                comment=None,
                decision_time=now,
            ),
            
            # Approbation en attente
            BookingApproval(
                id=uuid.UUID("550e8400-e29b-41d4-a716-446655440041"),
                booking_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440033"),  # Clio
                approver_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440002"),  # manager
                status=ApprovalStatus.PENDING.value,
                comment=None,
                decision_time=now,
            ),
        ]
        db.add_all(approvals)
        db.flush()
        print(f"✅ {len(approvals)} demandes d'approbation créées")
        
        # Commit des changements
        db.commit()
        print("✅ Toutes les données d'exemple ont été créées avec succès")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de la création des données: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()
