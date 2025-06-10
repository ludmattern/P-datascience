# Variables
POSTGRES_CONTAINER = piscineds_postgres
PGADMIN_CONTAINER = piscineds_pgadmin
DB_USER = lmattern
DB_NAME = piscineds
SCRIPTS_PATH = /scripts

# Colors for output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m

.PHONY: help up down restart status logs clean setup-db exec-postgres exec-pgadmin run-sql run-table run-item run-auto run-customers remove_duplicates

# Default target
help:
	@echo "$(BLUE)Makefile pour le projet Data Science$(NC)"
	@echo ""
	@echo "$(YELLOW)Commandes disponibles:$(NC)"
	@echo "  $(GREEN)up$(NC)           - Démarrer tous les services"
	@echo "  $(GREEN)down$(NC)         - Arrêter tous les services"
	@echo "  $(GREEN)restart$(NC)      - Redémarrer tous les services"
	@echo "  $(GREEN)status$(NC)       - Afficher le statut des conteneurs"
	@echo "  $(GREEN)logs$(NC)         - Afficher les logs"
	@echo "  $(GREEN)logs-postgres$(NC) - Afficher les logs PostgreSQL"
	@echo "  $(GREEN)logs-pgadmin$(NC)  - Afficher les logs PgAdmin"
	@echo "  $(GREEN)clean$(NC)        - Nettoyer les conteneurs et volumes"
	@echo ""
	@echo "$(YELLOW)Base de données:$(NC)"
	@echo "  $(GREEN)setup-db$(NC)     - Configurer la base de données (tables + données)"
	@echo "  $(GREEN)exec-postgres$(NC) - Se connecter à PostgreSQL"
	@echo "  $(GREEN)exec-pgadmin$(NC)  - Ouvrir PgAdmin dans le navigateur"
	@echo ""
	@echo "$(YELLOW)Scripts SQL:$(NC)"
	@echo "  $(GREEN)run-sql$(NC)      - Exécuter table.sql"
	@echo "  $(GREEN)run-item$(NC)     - Exécuter item_table.sql"
	@echo "  $(GREEN)run-auto$(NC)     - Exécuter automatic_table.sql"
	@echo "  $(GREEN)run-all-scripts$(NC) - Exécuter tous les scripts dans l'ordre"

# Services management
up:
	@echo "$(YELLOW)Démarrage des services...$(NC)"
	docker compose up -d
	@echo "$(GREEN)Services démarrés!$(NC)"
	@echo "$(BLUE)PostgreSQL:$(NC) localhost:5432"
	@echo "$(BLUE)PgAdmin:$(NC) http://localhost:8080"

down:
	@echo "$(YELLOW)Arrêt des services...$(NC)"
	docker compose down
	@echo "$(GREEN)Services arrêtés!$(NC)"

restart:
	@echo "$(YELLOW)Redémarrage des services...$(NC)"
	docker compose restart
	@echo "$(GREEN)Services redémarrés!$(NC)"

status:
	@echo "$(YELLOW)Statut des conteneurs:$(NC)"
	docker compose ps

# Logs
logs:
	docker compose logs -f

logs-postgres:
	docker compose logs -f postgres

logs-pgadmin:
	docker compose logs -f pgadmin

# Database operations
setup-db: up wait-postgres run-all-scripts
	@echo "$(GREEN)Base de données configurée avec succès!$(NC)"

wait-postgres:
	@echo "$(YELLOW)Attente du démarrage de PostgreSQL...$(NC)"
	@until docker exec $(POSTGRES_CONTAINER) pg_isready -U $(DB_USER) -d $(DB_NAME) >/dev/null 2>&1; do \
		sleep 1; \
	done
	@echo "$(GREEN)PostgreSQL est prêt!$(NC)"

exec-postgres:
	@echo "$(YELLOW)Connexion à PostgreSQL...$(NC)"
	docker exec -it $(POSTGRES_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)

exec-pgadmin:
	@echo "$(YELLOW)Ouverture de PgAdmin...$(NC)"
	@echo "$(BLUE)URL:$(NC) http://localhost:8080"
	@echo "$(BLUE)Email:$(NC) lmattern@student.42.fr"
	@echo "$(BLUE)Password:$(NC) mysecretpassword"
	@echo "$(GREEN)Le serveur PostgreSQL sera automatiquement configuré!$(NC)"
	@if command -v xdg-open >/dev/null 2>&1; then \
		xdg-open http://localhost:8080; \
	elif command -v open >/dev/null 2>&1; then \
		open http://localhost:8080; \
	else \
		echo "$(RED)Impossible d'ouvrir automatiquement le navigateur$(NC)"; \
	fi

# SQL Scripts execution
run-sql:
	@echo "$(YELLOW)Exécution de table.sql...$(NC)"
	docker exec -it $(POSTGRES_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -f $(SCRIPTS_PATH)/table.sql
	@echo "$(GREEN)table.sql exécuté!$(NC)"

run-auto:
	@echo "$(YELLOW)Exécution de automatic_table.sql...$(NC)"
	docker exec -it $(POSTGRES_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -f $(SCRIPTS_PATH)/automatic_table.sql
	@echo "$(GREEN)automatic_table.sql exécuté!$(NC)"

run-item:
	@echo "$(YELLOW)Exécution de item_table.sql...$(NC)"
	docker exec -it $(POSTGRES_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -f $(SCRIPTS_PATH)/item_table.sql
	@echo "$(GREEN)item_table.sql exécuté!$(NC)"

run-customers:
	@echo "$(YELLOW)Exécution de customers_table.sql...$(NC)"
	docker exec -it $(POSTGRES_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -f $(SCRIPTS_PATH)/customers_table.sql
	@echo "$(GREEN)customers_table.sql exécuté!$(NC)"

run-remove_duplicates:
	@echo "$(YELLOW)Suppression des doublons dans la table customers...$(NC)"
	docker exec -it $(POSTGRES_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -f $(SCRIPTS_PATH)/remove_duplicates.sql
	@echo "$(GREEN)remove_duplicates.sql exécuté!$(NC)"

run-fusion:
	@echo "$(YELLOW)Fusion des tables customers et items...$(NC)"
	docker exec -it $(POSTGRES_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -f $(SCRIPTS_PATH)/fusion.sql
	@echo "$(GREEN)fusion.sql exécuté!$(NC)"

run-all-scripts: run-sql run-auto run-item run-customers run-remove_duplicates run-fusion
	@echo "$(GREEN)Tous les scripts ont été exécutés!$(NC)"

# Development utilities
shell-postgres:
	@echo "$(YELLOW)Ouverture du shell dans le conteneur PostgreSQL...$(NC)"
	docker exec -it $(POSTGRES_CONTAINER) /bin/bash

shell-pgadmin:
	@echo "$(YELLOW)Ouverture du shell dans le conteneur PgAdmin...$(NC)"
	docker exec -it $(POSTGRES_CONTAINER) /bin/bash

# display graphs

display-help:
	@echo "$(BLUE)Graphiques disponibles:$(NC)"
	@echo "  $(GREEN)display-pie$(NC)       - Afficher le graphique en secteurs"
	@echo "  $(GREEN)display-chart$(NC)     - Afficher le graphique des graphiques"
	@echo "  $(GREEN)display-mustache$(NC)  - Afficher le graphique en moustaches"
	@echo "  $(GREEN)display-building$(NC)  - Afficher le graphique en barres"
	@echo "  $(GREEN)display-elbow$(NC)     - Afficher le graphique en courbes"
	@echo "  $(GREEN)display-clustering$(NC) - Afficher le graphique de clustering"

display-pie:
	@echo "$(YELLOW)Affichage du graphique en secteurs...$(NC)"
	python3 ./graphs/pie.py

display-chart:
	@echo "$(YELLOW)Affichage du graphique des graphique...$(NC)"
	python3 ./graphs/chart.py

display-mustache:
	@echo "$(YELLOW)Affichage du graphique en moustaches...$(NC)"
	python3 ./graphs/mustache.py

display-building:
	@echo "$(YELLOW)Affichage du graphique en barres...$(NC)"
	python3 ./graphs/Building.py

display-elbow:
	@echo "$(YELLOW)Affichage du graphique en courbes...$(NC)"
	python3 ./graphs/elbow.py

display-clustering:
	@echo "$(YELLOW)Affichage du graphique de clustering...$(NC)"
	python3 ./graphs/Clustering.py

# Cleanup
clean:
	@echo "$(YELLOW)Nettoyage des conteneurs et images...$(NC)"
	docker compose down -v --remove-orphans
	docker system prune -f
	@echo "$(GREEN)Nettoyage terminé!$(NC)"

clean-all: clean
	@echo "$(RED)Suppression complète (conteneurs, images, volumes)...$(NC)"
	docker compose down -v --rmi all --remove-orphans
	@echo "$(GREEN)Suppression complète terminée!$(NC)"

# Quick commands
start: up
stop: down
rebuild: down up