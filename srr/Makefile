# Makefile pour la gestion de l'environnement de développement SRR

.PHONY: help build up down logs ps clean rebuild test lint shell

# Couleurs pour une meilleure lisibilité
GREEN := $(shell tput setaf 2)
YELLOW := $(shell tput setaf 3)
BLUE := $(shell tput setaf 4)
RESET := $(shell tput sgr0)

help:
	@echo "${BLUE}Système de Réservation de Ressources (SRR)${RESET} - Commandes disponibles :"
	@echo ""
	@echo "${GREEN}make build${RESET}      - Construit tous les conteneurs Docker"
	@echo "${GREEN}make up${RESET}         - Démarre tous les services"
	@echo "${GREEN}make down${RESET}       - Arrête tous les services"
	@echo "${GREEN}make logs${RESET}       - Affiche les logs de tous les services"
	@echo "${GREEN}make ps${RESET}         - Liste les services en cours d'exécution"
	@echo "${GREEN}make clean${RESET}      - Supprime tous les conteneurs et volumes"
	@echo "${GREEN}make rebuild${RESET}    - Reconstruit les images et redémarre"
	@echo "${GREEN}make test${RESET}       - Lance les tests"
	@echo "${GREEN}make lint${RESET}       - Lance les vérifications de code"
	@echo "${GREEN}make shell-X${RESET}    - Ouvre un shell dans le conteneur X (backend, frontend, db, redis, mock)"
	@echo ""
	@echo "${YELLOW}Exemples :${RESET}"
	@echo "  make build && make up   - Construit et lance l'environnement"
	@echo "  make shell-backend      - Ouvre un shell dans le conteneur backend"
	@echo "  make logs               - Affiche les logs en temps réel"

build:
	@echo "${BLUE}Construction des images Docker...${RESET}"
	docker-compose build

up:
	@echo "${BLUE}Démarrage des services...${RESET}"
	docker-compose up -d

down:
	@echo "${BLUE}Arrêt des services...${RESET}"
	docker-compose down

logs:
	@echo "${BLUE}Affichage des logs...${RESET}"
	docker-compose logs -f

ps:
	@echo "${BLUE}Liste des services en cours d'exécution...${RESET}"
	docker-compose ps

clean:
	@echo "${YELLOW}Suppression des conteneurs et volumes...${RESET}"
	docker-compose down -v
	docker system prune -f

rebuild:
	@echo "${BLUE}Reconstruction des images et redémarrage...${RESET}"
	docker-compose down
	docker-compose build
	docker-compose up -d

test:
	@echo "${BLUE}Lancement des tests...${RESET}"
	docker-compose exec backend pytest
	docker-compose exec frontend npm test -- --watchAll=false

lint:
	@echo "${BLUE}Vérification du code backend...${RESET}"
	docker-compose exec backend flake8
	@echo "${BLUE}Vérification du code frontend...${RESET}"
	docker-compose exec frontend npm run lint

# Shells pour accéder aux conteneurs
shell-backend:
	@echo "${BLUE}Connexion au shell du backend...${RESET}"
	docker-compose exec backend /bin/bash

shell-frontend:
	@echo "${BLUE}Connexion au shell du frontend...${RESET}"
	docker-compose exec frontend /bin/sh

shell-db:
	@echo "${BLUE}Connexion au shell de la base de données...${RESET}"
	docker-compose exec db psql -U postgres srr_dev

shell-redis:
	@echo "${BLUE}Connexion au shell Redis...${RESET}"
	docker-compose exec redis redis-cli

shell-mock:
	@echo "${BLUE}Connexion au shell des services simulés...${RESET}"
	docker-compose exec mock-services /bin/bash
