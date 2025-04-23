# Plan d'Infrastructure - Environnement de Développement SRR

## Objectifs Spécifiques

Ce plan détaille la mise en place de l'infrastructure Docker pour l'environnement de développement minimaliste du SRR. L'objectif est de créer un environnement isolé, reproductible et proche de la production qui permet le développement et les tests des différentes composantes du système.

## Dépendances

- Aucune dépendance avec d'autres plans (ce module est le point de départ)
- Référence aux principes définis dans [DESIGN.md](/doc/DESIGN.md), section "9. DÉPLOIEMENT ET OPÉRATIONS"

## Composants à Implémenter

### 1. Structure de Base Docker

```
srr/
├── .env                      # Variables d'environnement
├── docker-compose.yml        # Configuration des services
├── docker-compose.dev.yml    # Surcharge pour développement (volumes, ports...)
├── .dockerignore             # Fichiers à ignorer
├── Makefile                  # Commandes de gestion simplifiées
└── services/
    ├── backend/              # Service FastAPI
    │   ├── Dockerfile        # Construction du backend 
    │   └── requirements.txt  # Dépendances Python
    ├── frontend/             # Service React
    │   └── Dockerfile        # Construction du frontend
    ├── postgres/             # Service PostgreSQL
    │   ├── Dockerfile        # Customisation PostgreSQL (si nécessaire)
    │   └── init/             # Scripts d'initialisation
    ├── redis/                # Service Redis
    │   └── redis.conf        # Configuration Redis
    └── mocks/                # Services simulés (AD/LDAP, Exchange)
        ├── Dockerfile        # Construction des mocks
        └── data/             # Données de test
```

### 2. Configuration des Services Docker

#### Service Backend (FastAPI)

```yaml
# Extrait du docker-compose.yml
backend:
  build: 
    context: ./services/backend
    dockerfile: Dockerfile
  volumes:
    - ./services/backend:/app  # Pour le développement (hot-reload)
  environment:
    - DATABASE_URL=postgresql://postgres:password@db:5432/srr_dev
    - REDIS_URL=redis://redis:6379/0
    - DEBUG=True
    - MOCK_AUTH=True
    - MOCK_EXCHANGE=True
  ports:
    - "8000:8000"
  depends_on:
    - db
    - redis
    - mock-services
  command: uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Service Frontend (React)

```yaml
# Extrait du docker-compose.yml
frontend:
  build:
    context: ./services/frontend
    dockerfile: Dockerfile
  volumes:
    - ./services/frontend:/app  # Pour le développement (hot-reload)
    - /app/node_modules
  environment:
    - REACT_APP_API_URL=http://localhost:8000
    - NODE_ENV=development
  ports:
    - "3000:3000"
  depends_on:
    - backend
  command: npm start
```

#### Service Base de Données (PostgreSQL)

```yaml
# Extrait du docker-compose.yml
db:
  image: postgres:14
  volumes:
    - postgres_data:/var/lib/postgresql/data
    - ./services/postgres/init:/docker-entrypoint-initdb.d
  environment:
    - POSTGRES_PASSWORD=password
    - POSTGRES_DB=srr_dev
  ports:
    - "5432:5432"
```

#### Service Redis

```yaml
# Extrait du docker-compose.yml
redis:
  image: redis:alpine
  volumes:
    - redis_data:/data
    - ./services/redis/redis.conf:/usr/local/etc/redis/redis.conf
  command: redis-server /usr/local/etc/redis/redis.conf
  ports:
    - "6379:6379"
```

#### Service Mock (AD/LDAP et Exchange)

```yaml
# Extrait du docker-compose.yml
mock-services:
  build:
    context: ./services/mocks
    dockerfile: Dockerfile
  volumes:
    - ./services/mocks:/app
  environment:
    - MOCK_USERS_FILE=/app/data/users.json
    - MOCK_RESOURCES_FILE=/app/data/resources.json
  ports:
    - "8080:8080"
```

### 3. Dockerfile pour FastAPI Backend

```dockerfile
# services/backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. Dockerfile pour Frontend React

```dockerfile
# services/frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

### 5. Dockerfile pour Mock Services

```dockerfile
# services/mocks/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "mock_server.py"]
```

### 6. Makefile pour Gestion Simplifiée

```makefile
# Makefile

.PHONY: help build up down logs ps clean rebuild test lint

help:
	@echo "SRR Development Environment Commands:"
	@echo "make build      - Build all docker images"
	@echo "make up         - Start all services"
	@echo "make down       - Stop all services"
	@echo "make logs       - View logs for all services"
	@echo "make ps         - List running services"
	@echo "make clean      - Remove all containers and volumes"
	@echo "make rebuild    - Rebuild images and restart"
	@echo "make test       - Run tests"
	@echo "make lint       - Run linting"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

ps:
	docker-compose ps

clean:
	docker-compose down -v
	docker system prune -f

rebuild:
	docker-compose down
	docker-compose build
	docker-compose up -d

test:
	docker-compose exec backend pytest

lint:
	docker-compose exec backend flake8
	docker-compose exec frontend npm run lint
```

### 7. Variables d'Environnement

```env
# .env
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=srr_dev

# Backend
DEBUG=True
ALLOW_CORS_ORIGINS=http://localhost:3000
JWT_SECRET=temporarily_insecure_jwt_secret_for_dev_only
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

### 8. Configuration Redis

```
# services/redis/redis.conf
# Redis configuration for SRR development
port 6379
bind 0.0.0.0
protected-mode no
maxmemory 256mb
maxmemory-policy allkeys-lru
```

### 9. Réseau Docker

La configuration réseau permettra aux services de communiquer entre eux tout en exposant les ports nécessaires au développement.

- Backend : accessible depuis le host sur port 8000
- Frontend : accessible depuis le host sur port 3000
- PostgreSQL : accessible depuis le host sur port 5432
- Redis : accessible depuis le host sur port 6379
- Mock Services : accessible depuis le host sur port 8080

Les services communiquent entre eux via le réseau Docker interne utilisant les noms de service comme hostnames.

### 10. Volumes Docker

```yaml
# Extrait du docker-compose.yml pour les volumes
volumes:
  postgres_data:    # Persistance des données PostgreSQL
  redis_data:       # Persistance des données Redis
```

## Implémentation Étape par Étape

1. **Création de la structure de répertoires**
   - Mettre en place l'arborescence des dossiers décrite ci-dessus

2. **Création des fichiers Docker**
   - Créer le docker-compose.yml principal
   - Créer les Dockerfiles pour chaque service
   - Créer le .env avec les variables d'environnement

3. **Préparation des services**
   - Configurer PostgreSQL avec scripts d'initialisation
   - Configurer Redis
   - Préparer le service mock minimal

4. **Scripts utilitaires**
   - Créer le Makefile pour simplifier les commandes
   - Documenter les commandes disponibles

5. **Test de l'infrastructure**
   - Vérifier que tous les containers démarrent correctement
   - Vérifier la connectivité entre les services
   - Vérifier l'accès depuis l'hôte

## Critères de Validation

- ✅ Tous les services peuvent démarrer via `docker-compose up`
- ✅ Pas d'erreurs dans les logs des containers
- ✅ Backend peut se connecter à PostgreSQL et Redis
- ✅ Frontend peut se connecter au Backend API
- ✅ Les volumes persistent correctement les données
- ✅ Les modifications de code sont rechargées automatiquement (hot-reload)

## Considérations de Sécurité

> **Note Importante** : Cette configuration est uniquement pour le développement et contient des simplifications qui ne sont pas adaptées à un environnement de production :
> - Mots de passe par défaut
> - Ports exposés sur l'hôte
> - Mode debug activé
> - Secrets stockés dans des fichiers d'environnement

Pour une mise en production, il faudrait :
- Supprimer les mots de passe par défaut
- Utiliser un système de gestion de secrets
- Limiter l'exposition des ports
- Désactiver les modes debug
- Implémenter une authentification robuste

## Références

- [Documentation Docker Compose](https://docs.docker.com/compose/)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation PostgreSQL](https://www.postgresql.org/docs/)
- [DESIGN.md](/doc/DESIGN.md) section "9. DÉPLOIEMENT ET OPÉRATIONS"
