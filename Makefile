# Makefile for Docker Orchestrator Project

# Variables
NAME		   := Electrik_light_orchestra
DOCKER_COMPOSE := docker compose
PYTHON 		   := python3

# Couleurs
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color


help:
	@echo ""
	@echo "${GREEN} ${NAME} - Commandes disponibles:${NC}"
	@echo ""
	@echo "  ${YELLOW}build${NC}      - Construit les images Docker"
	@echo "  ${YELLOW}up${NC}        - Lance les services en détaché"
	@echo "  ${YELLOW}down${NC}      - Arrête et supprime les containers"
	@echo "  ${YELLOW}restart${NC}   - Redémarre les services"
	@echo "  ${YELLOW}logs${NC}      - Affiche les logs des services"
	@echo "  ${YELLOW}clean${NC}     - Nettoie les ressources Docker"
	@echo "  ${YELLOW}test${NC}      - Exécute les tests de base"
	@echo "  ${YELLOW}cli${NC}       - Lance l'interface CLI"
	@echo "  ${YELLOW}monitoring${NC}- Ouvre les interfaces de monitoring"
	@echo ""

build:
	@echo "${GREEN}Building Docker images...${NC}"
	@$(DOCKER_COMPOSE) build 
	@echo "${GREEN}Build Done!${NC}"

up:
	@echo "${GREEN}Starting services in detached mode...${NC}"
	@$(DOCKER_COMPOSE) up -d

down:
	@echo "${RED}Stopping and removing containers...${NC}"
	@$(DOCKER_COMPOSE) down

restart: down up
	@echo "${YELLOW}Services restarted${NC}"

logs:
	@echo "${YELLOW}Showing logs (Ctrl+C to exit)...${NC}"
	@$(DOCKER_COMPOSE) logs -f

ps:
	@echo "${YELLOW}Listing running containers...${NC}"
	@$(DOCKER_COMPOSE) ps

clean:
	@echo "${RED}Cleaning Docker resources...${NC}"
	@docker system prune -f
	@echo "${GREEN}Done!${NC}"

# test:
# 	@echo "${YELLOW}Running basic tests...${NC}"
# 	@$(DOCKER_COMPOSE) exec orchestrator $(PYTHON) /app/main.py list
# 	@$(DOCKER_COMPOSE) exec orchestrator $(PYTHON) /app/main.py show_stats orchestrator

cli:
	@echo "${GREEN}Launching CLI interface...${NC}"
	@$(DOCKER_COMPOSE) exec orchestrator $(PYTHON) /app/main.py

monitoring:
	@echo "${GREEN}Opening monitoring interfaces...${NC}"
	@xdg-open http://localhost:3000  # Grafana
	@xdg-open http://localhost:9090  # Prometheus

fclean: down clean
	docker builder prune -af
	@echo "${RED}Stopping and removing containers, volumes, and networks...${NC}"
	@echo "${GREEN}Done!${NC}"
# Alias pour la commande par défaut
default: help

.PHONY: help build up down restart logs clean test cli