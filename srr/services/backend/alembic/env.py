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
# Configure l'environnement d'exécution pour Alembic, l'outil de migration de base de données.
# Ce fichier définit comment les migrations sont exécutées et connecte Alembic aux modèles SQLAlchemy.
###############################################################################
# [Source file design principles]
# - Séparation des configurations spécifiques à l'environnement
# - Accès aux métadonnées de modèle pour l'autogénération des migrations
# - Support du mode en ligne (avec connexion directe) pour les migrations
# - Utilisation de la configuration centrale de l'application
# - Gestion appropriée des ressources de connexion
###############################################################################
# [Source file constraints]
# - Doit être compatible avec les différents environnements (dev, test, prod)
# - Ne pas contenir de secrets en dur (utiliser la configuration)
# - Garantir le chargement complet du modèle pour les migrations autogénérées
# - Gestion des erreurs robuste pendant les migrations
###############################################################################
# [Dependencies]
# - alembic: Outil de migration
# - app/db/base: Modèle SQLAlchemy complet avec toutes les tables
# - app/core/config: Configuration centrale avec URL de la BDD
###############################################################################
# [GenAI tool change history]
# 2025-04-23T10:21:10Z : Création initiale du fichier env.py par CodeAssistant
# * Configuration de l'environnement Alembic pour utiliser les modèles SQLAlchemy
# * Support des migrations en mode online pour PostgreSQL
# * Intégration avec la configuration centrale de l'application
###############################################################################

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# Ajout du répertoire principal au path pour l'import des modèles
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import de la configuration et des modèles
from app.core.config import settings
from app.db.base import Base

# Configuration Alembic
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# Remplacement de l'URL de la base de données par celle de la configuration
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """
    [Function intent]
    Exécute les migrations en mode 'offline'.
    
    [Design principles]
    Support des migrations sans connexion active à la base de données.
    
    [Implementation details]
    Utilisé principalement pour générer des scripts de migration SQL.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    [Function intent]
    Exécute les migrations en mode 'online' avec connexion active.
    
    [Design principles]
    Mode normal d'exécution pour appliquer les migrations directement.
    
    [Implementation details]
    Établit une connexion à la base de données et exécute les migrations.
    Utilise la détection de changement de type pour les migrations automatiques.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Détecte les changements de type
        )

        with context.begin_transaction():
            context.run_migrations()


# Exécution des migrations selon le mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
