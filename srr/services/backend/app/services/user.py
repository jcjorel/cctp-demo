from typing import Dict, List, Optional, Any, Union
from sqlalchemy.orm import Session

from app.core.security import verify_password, get_password_hash
from app.models.user import User
from app.utils.mock_ad import authenticate_mock_user, get_mock_user, search_mock_users
from app.core.config import settings


class UserService:
    """
    [Class intent]
    Service centralisant les opérations d'authentification et de gestion des utilisateurs.
    
    [Design principles]
    Interface unifiée indépendante du système d'authentification sous-jacent (AD, LDAP, local).
    Séparation entre l'authentification externe et les modèles d'utilisateurs internes.
    
    [Implementation details]
    Utilise le mock AD en développement avec possibilité de basculer vers un vrai service AD.
    """

    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> Optional[User]:
        """
        [Function intent]
        Authentifie un utilisateur en vérifiant ses identifiants.
        
        [Design principles]
        Point d'entrée unique pour l'authentification de tout type d'utilisateur.
        Gestion de la synchronisation entre l'annuaire externe et la base locale.
        
        [Implementation details]
        Vérifie les identifiants via Mock AD, puis crée ou met à jour l'utilisateur local.
        
        Args:
            db: Session de base de données
            username: Nom d'utilisateur
            password: Mot de passe en clair
            
        Returns:
            User | None: Utilisateur authentifié ou None si échec
        """
        # En développement, utilise le mock AD
        if settings.MOCK_AUTH:
            # Appel au service mock AD pour vérifier les identifiants
            ad_user = authenticate_mock_user(username, password)
            if not ad_user:
                return None
                
            # Vérifier si l'utilisateur existe déjà en base
            db_user = db.query(User).filter(User.username == username).first()
            
            if db_user:
                # Mise à jour des informations si l'utilisateur existe
                db_user.email = ad_user.get("email", "")
                db_user.full_name = ad_user.get("full_name", "")
                db_user.role = ad_user.get("roles", ["user"])[0]  # Rôle principal
                db_user.groups = ad_user.get("roles", ["user"])   # Tous les rôles comme groupes
                db_user.department = ad_user.get("department", "")
                db_user.is_active = ad_user.get("active", True)
                db.commit()
                db.refresh(db_user)
                return db_user
            else:
                # Création d'un nouvel utilisateur
                hashed_password = ad_user.get("hashed_password", get_password_hash(password))
                db_user = User(
                    username=username,
                    email=ad_user.get("email", ""),
                    full_name=ad_user.get("full_name", ""),
                    role=ad_user.get("roles", ["user"])[0],  # Rôle principal
                    groups=ad_user.get("roles", ["user"]),   # Tous les rôles comme groupes
                    department=ad_user.get("department", ""),
                    hashed_password=hashed_password,
                    is_active=ad_user.get("active", True)
                )
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                return db_user
        else:
            # Pour une véritable intégration AD/LDAP
            # Cette partie serait implémentée dans une version de production
            raise NotImplementedError("L'authentification réelle n'est pas encore implémentée.")

    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        """
        [Function intent]
        Récupère un utilisateur par son nom d'utilisateur.
        
        [Design principles]
        Accès direct à un utilisateur spécifique sans authentification.
        
        [Implementation details]
        Interroge la base de données locale, pas l'annuaire externe.
        
        Args:
            db: Session de base de données
            username: Nom d'utilisateur
            
        Returns:
            User | None: Utilisateur trouvé ou None
        """
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def search_users(
        db: Session, 
        query: str = "", 
        role: str = None,
        department: str = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """
        [Function intent]
        Recherche des utilisateurs selon plusieurs critères.
        
        [Design principles]
        Interface de recherche multi-critères avec pagination.
        
        [Implementation details]
        Combinaison de filtres SQLAlchemy pour affiner la recherche.
        
        Args:
            db: Session de base de données
            query: Texte à rechercher dans nom ou email
            role: Filtrer par rôle
            department: Filtrer par département
            skip: Index de départ pour la pagination
            limit: Nombre maximum de résultats
            
        Returns:
            List[User]: Liste des utilisateurs correspondants
        """
        search = db.query(User)
        
        if query:
            search = search.filter(
                (User.username.ilike(f"%{query}%")) | 
                (User.email.ilike(f"%{query}%")) |
                (User.full_name.ilike(f"%{query}%"))
            )
            
        if role:
            search = search.filter(User.role == role)
            
        if department:
            search = search.filter(User.department == department)
            
        return search.offset(skip).limit(limit).all()

    @staticmethod
    def create_user(
        db: Session, 
        username: str,
        password: str,
        email: str = "",
        full_name: str = "",
        role: str = "user",
        department: str = "",
        is_active: bool = True
    ) -> User:
        """
        [Function intent]
        Crée un nouvel utilisateur dans le système.
        
        [Design principles]
        Création d'utilisateur avec validation des données.
        
        [Implementation details]
        Validation du nom d'utilisateur unique et hachage du mot de passe.
        
        Args:
            db: Session de base de données
            username: Nom d'utilisateur unique
            password: Mot de passe en clair
            email: Adresse email (optionnelle)
            full_name: Nom complet (optionnel)
            role: Rôle de l'utilisateur (défaut: user)
            department: Département (optionnel)
            is_active: État du compte (défaut: actif)
            
        Returns:
            User: Nouvel utilisateur créé
            
        Raises:
            ValueError: Si l'utilisateur existe déjà
        """
        # Vérification d'unicité
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise ValueError(f"L'utilisateur {username} existe déjà")
            
        # Création du nouvel utilisateur
        hashed_password = get_password_hash(password)
        db_user = User(
            username=username,
            email=email,
            full_name=full_name,
            role=role,
            groups=[role, "user"],  # Ajout du rôle principal et user par défaut
            department=department,
            hashed_password=hashed_password,
            is_active=is_active
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(
        db: Session, 
        user_id: int,
        email: str = None,
        full_name: str = None,
        role: str = None,
        department: str = None,
        is_active: bool = None
    ) -> Optional[User]:
        """
        [Function intent]
        Met à jour les informations d'un utilisateur.
        
        [Design principles]
        Mise à jour partielle avec des paramètres optionnels.
        
        [Implementation details]
        Mise à jour conditionnelle selon les champs fournis.
        
        Args:
            db: Session de base de données
            user_id: ID de l'utilisateur à mettre à jour
            email: Nouvelle adresse email (optionnel)
            full_name: Nouveau nom complet (optionnel)
            role: Nouveau rôle (optionnel)
            department: Nouveau département (optionnel)
            is_active: Nouvel état du compte (optionnel)
            
        Returns:
            User | None: Utilisateur mis à jour ou None si non trouvé
        """
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
            
        # Mise à jour conditionnelle des champs
        if email is not None:
            db_user.email = email
            
        if full_name is not None:
            db_user.full_name = full_name
            
        if role is not None:
            db_user.role = role
            # Mise à jour des groupes pour inclure le nouveau rôle
            if role not in db_user.groups:
                db_user.groups.append(role)
                
        if department is not None:
            db_user.department = department
            
        if is_active is not None:
            db_user.is_active = is_active
            
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def change_password(
        db: Session, 
        user_id: int,
        current_password: str,
        new_password: str
    ) -> bool:
        """
        [Function intent]
        Change le mot de passe d'un utilisateur.
        
        [Design principles]
        Vérification de sécurité avec l'ancien mot de passe avant changement.
        
        [Implementation details]
        Vérifie l'ancien mot de passe, puis hache et enregistre le nouveau.
        
        Args:
            db: Session de base de données
            user_id: ID de l'utilisateur
            current_password: Mot de passe actuel
            new_password: Nouveau mot de passe
            
        Returns:
            bool: True si réussi, False sinon
        """
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False
            
        # Vérifier le mot de passe actuel
        if not verify_password(current_password, db_user.hashed_password):
            return False
            
        # Mettre à jour vers le nouveau mot de passe
        db_user.hashed_password = get_password_hash(new_password)
        db.commit()
        return True

    @staticmethod
    def refresh_ad_sync(db: Session) -> List[User]:
        """
        [Function intent]
        Synchronise les utilisateurs depuis l'annuaire externe (Mock AD).
        
        [Design principles]
        Mise à jour périodique pour maintenir la cohérence avec l'annuaire externe.
        
        [Implementation details]
        Parcourt les utilisateurs de l'annuaire et crée/met à jour les utilisateurs locaux.
        
        Args:
            db: Session de base de données
            
        Returns:
            List[User]: Liste des utilisateurs synchronisés
        """
        if not settings.MOCK_AUTH:
            raise NotImplementedError("Synchronisation AD non implémentée hors mode mock")
            
        # Récupérer tous les utilisateurs mock
        mock_users = search_mock_users()
        synced_users = []
        
        for ad_user in mock_users:
            username = ad_user.get("username")
            
            # Vérifier si l'utilisateur existe déjà
            db_user = db.query(User).filter(User.username == username).first()
            
            if db_user:
                # Mise à jour
                db_user.email = ad_user.get("email", "")
                db_user.full_name = ad_user.get("full_name", "")
                db_user.role = ad_user.get("roles", ["user"])[0]
                db_user.groups = ad_user.get("roles", ["user"])
                db_user.department = ad_user.get("department", "")
                db_user.is_active = ad_user.get("active", True)
                db.commit()
                db.refresh(db_user)
            else:
                # Création
                db_user = User(
                    username=username,
                    email=ad_user.get("email", ""),
                    full_name=ad_user.get("full_name", ""),
                    role=ad_user.get("roles", ["user"])[0],
                    groups=ad_user.get("roles", ["user"]),
                    department=ad_user.get("department", ""),
                    hashed_password=ad_user.get("hashed_password", ""),
                    is_active=ad_user.get("active", True)
                )
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                
            synced_users.append(db_user)
            
        return synced_users


user_service = UserService()
