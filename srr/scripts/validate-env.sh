#!/bin/bash
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
# Script de validation de l'environnement de développement SRR.
# Ce script exécute automatiquement des vérifications de base sur tous les composants
# de l'environnement pour s'assurer qu'ils sont correctement configurés et fonctionnels.
###############################################################################
# [Source file design principles]
# - Vérifications isolées pour chaque service avec codes de retour propres
# - Retour visuel clair avec indicateurs de succès/échec
# - Indépendance vis-à-vis des autres scripts
# - Organisation modulaire pour faciliter l'extension
###############################################################################
# [Source file constraints]
# - Doit être exécuté depuis la racine du projet SRR
# - Dépend de Docker et docker-compose installés
# - Nécessite un environnement Unix/Linux/macOS
###############################################################################
# [Dependencies]
# - docker-compose.yml
# - .env
# - services/backend/app/api/v1/endpoints/health.py
###############################################################################
# [GenAI tool change history]
# 2025-04-23T12:47:00Z : Création initiale du script de validation par CodeAssistant
# * Implémentation des vérifications pour tous les services
# * Ajout d'indicateurs visuels pour les résultats des tests
# * Configuration des codes de retour pour intégration CI/CD
###############################################################################

set -e

# Couleurs pour la sortie
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Variables
BACKEND_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:3000"
POSTGRES_CONTAINER="srr-postgres"
REDIS_CONTAINER="srr-redis"
BACKEND_CONTAINER="srr-backend"
FRONTEND_CONTAINER="srr-frontend"
MOCKS_CONTAINER="srr-mocks"

# Fonction pour afficher les messages
print_message() {
    echo -e "$1"
}

# Fonction pour les messages de succès
success() {
    print_message "${GREEN}✅ $1${NC}"
}

# Fonction pour les messages d'erreur
error() {
    print_message "${RED}❌ $1${NC}"
}

# Fonction pour les messages d'avertissement
warning() {
    print_message "${YELLOW}⚠️  $1${NC}"
}

# Fonction pour vérifier si un conteneur est en cours d'exécution
check_container() {
    local container=$1
    if docker ps --format '{{.Names}}' | grep -q "$container"; then
        success "Le conteneur $container est en cours d'exécution"
        return 0
    else
        error "Le conteneur $container n'est pas en cours d'exécution"
        return 1
    fi
}

print_message "\n🔍 VALIDATION DE L'ENVIRONNEMENT SRR\n"
print_message "================================================"

# Vérification de Docker
print_message "\n📋 [1/7] Vérification de Docker"
if docker info &>/dev/null; then
    success "Docker est installé et fonctionne correctement"
    docker --version
else
    error "Docker n'est pas installé ou ne fonctionne pas correctement"
    exit 1
fi

# Vérification de Docker Compose
print_message "\n📋 [2/7] Vérification de Docker Compose"
if docker-compose --version &>/dev/null; then
    success "Docker Compose est installé et fonctionne correctement"
    docker-compose --version
else
    error "Docker Compose n'est pas installé ou ne fonctionne pas correctement"
    exit 1
fi

# Vérification des conteneurs
print_message "\n📋 [3/7] Vérification des conteneurs Docker"
check_postgres=$(check_container $POSTGRES_CONTAINER; echo $?)
check_redis=$(check_container $REDIS_CONTAINER; echo $?)
check_backend=$(check_container $BACKEND_CONTAINER; echo $?)
check_frontend=$(check_container $FRONTEND_CONTAINER; echo $?)
check_mocks=$(check_container $MOCKS_CONTAINER; echo $?)

if [[ $check_postgres -eq 0 && $check_redis -eq 0 && $check_backend -eq 0 && $check_frontend -eq 0 && $check_mocks -eq 0 ]]; then
    success "Tous les conteneurs sont en cours d'exécution"
else
    warning "Certains conteneurs ne sont pas en cours d'exécution. Tentative de démarrage..."
    docker-compose up -d
    sleep 10
fi

# Vérification de la base de données PostgreSQL
print_message "\n📋 [4/7] Vérification de PostgreSQL"
if docker exec $POSTGRES_CONTAINER pg_isready -U postgres &>/dev/null; then
    success "PostgreSQL est prêt à accepter des connexions"
    
    # Vérification des tables de base de données
    tables=$(docker exec $POSTGRES_CONTAINER psql -U postgres -d srr -c '\dt' -t | wc -l)
    if [[ $tables -gt 0 ]]; then
        success "Base de données initialisée avec $tables tables"
    else
        warning "Aucune table trouvée dans la base de données"
    fi
else
    error "PostgreSQL n'est pas prêt à accepter des connexions"
fi

# Vérification de Redis
print_message "\n📋 [5/7] Vérification de Redis"
if docker exec $REDIS_CONTAINER redis-cli ping | grep -q "PONG"; then
    success "Redis fonctionne correctement"
else
    error "Redis ne répond pas correctement"
fi

# Vérification du backend
print_message "\n📋 [6/7] Vérification du Backend API"
if curl -s $BACKEND_URL/api/v1/health | grep -q "status"; then
    success "Le backend API répond correctement"
    
    # Vérification de la documentation de l'API
    if curl -s $BACKEND_URL/docs | grep -q "Swagger UI"; then
        success "Documentation Swagger UI accessible"
    else
        warning "Documentation Swagger UI non accessible"
    fi
    
    # Vérification des migrations Alembic
    migration_status=$(docker exec $BACKEND_CONTAINER alembic current 2>/dev/null || echo "Erreur")
    if [[ "$migration_status" != "Erreur" ]]; then
        success "Migrations Alembic correctement appliquées"
        echo "  Version actuelle: $migration_status"
    else
        warning "Impossible de vérifier les migrations Alembic"
    fi
else
    error "Le backend API ne répond pas correctement"
fi

# Vérification du frontend
print_message "\n📋 [7/7] Vérification du Frontend"
if curl -s -o /dev/null -w "%{http_code}" $FRONTEND_URL | grep -q "200"; then
    success "Le frontend est accessible"
else
    error "Le frontend n'est pas accessible"
fi

# Vérification des logs pour détecter les erreurs
print_message "\n📋 Analyse des logs des conteneurs"
for container in $POSTGRES_CONTAINER $REDIS_CONTAINER $BACKEND_CONTAINER $FRONTEND_CONTAINER $MOCKS_CONTAINER; do
    log_errors=$(docker logs $container 2>&1 | grep -i "error" | wc -l)
    if [[ $log_errors -gt 0 ]]; then
        warning "Détection de $log_errors erreurs dans les logs de $container"
    else
        success "Aucune erreur détectée dans les logs de $container"
    fi
done

# Synthèse
print_message "\n================================================"
print_message "📝 SYNTHÈSE DE LA VALIDATION"

if [[ $check_postgres -eq 0 && $check_redis -eq 0 && $check_backend -eq 0 && $check_frontend -eq 0 && $check_mocks -eq 0 ]]; then
    if curl -s $BACKEND_URL/api/v1/health | grep -q "status" && curl -s -o /dev/null -w "%{http_code}" $FRONTEND_URL | grep -q "200"; then
        success "✨ L'environnement SRR est correctement configuré et fonctionnel"
        print_message "\nURLs d'accès:"
        print_message "  - Frontend: $FRONTEND_URL"
        print_message "  - Backend API: $BACKEND_URL/api/v1"
        print_message "  - Swagger UI: $BACKEND_URL/docs"
        exit 0
    else
        warning "⚠️  L'environnement SRR est partiellement fonctionnel"
        print_message "Certains services sont en cours d'exécution mais ne répondent pas correctement"
        exit 2
    fi
else
    error "❌ L'environnement SRR n'est pas correctement configuré"
    print_message "Certains services ne sont pas en cours d'exécution"
    exit 1
fi
