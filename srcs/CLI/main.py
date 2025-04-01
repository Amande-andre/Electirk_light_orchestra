#!/usr/bin/env python3
"""
Docker CLI Orchestrator
Un outil pour gérer et surveiller les containers Docker avec une interface CLI.
"""

import docker
import logging
from   flask import Flask, jsonify, request
from   flask_cors import CORS
import argparse
import sys
import time
from rich.console import Console  # Pour l'affichage coloré

# Initialisation de l'interface Rich pour les sorties colorées
console = Console()
console.print("[bold magenta]Docker CLI orchestrator[/bold magenta]")

# Configuration du système de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Client Docker initialisé avec les paramètres par défaut
client = docker.from_env()

# Flask app pour l'API REST
app = Flask(__name__)
CORS(app)  # Autorise les requêtes CORS

@app.route("/")
def home():
    """ Vérification de la connexion à l'API """
    return jsonify({"message": "Docker CLI orchestrata API is running!"})

def show_container_stats(container_name):
    """
    Affiche les statistiques temps réel d'un container spécifique.
    
    Args:
        container_name (str): Nom ou ID du container
    """
    try:
        container = client.containers.get(container_name)
        stats = container.stats(stream=False)  # Récupère les stats une seule fois
        
        # Extraction des métriques clés
        cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
        mem_usage = stats['memory_stats']['usage'] / 1024 / 1024  # Conversion en Mo
        network_in = stats['networks']['eth0']['rx_bytes']  # Réception
        network_out = stats['networks']['eth0']['tx_bytes']  # Transmission
        
        # Affichage formaté avec Rich
        console.print(f"""
    [bold]{container.name}[/bold] :
    [bold]- CPU:[/bold] {cpu_usage}
    [bold]- RAM:[/bold] {mem_usage:.2f} MB
    [bold]- Network:[/bold] {network_in}B in / {network_out}B out
        """)
    except docker.errors.NotFound:
        console.print("[red]Erreur: Container non trouvé[/red]")
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des stats: {e}")

def list_containers(show_stats=False):
    """
    Liste tous les containers Docker avec leurs statuts de base.
    
    Args:
        show_stats (bool): Si True, affiche les stats CPU/RAM
    """
    try:
        containers = client.containers.list(all=True)  # Inclut les containers arrêtés
        
        for container in containers:
            # Ligne de base avec ID, nom et statut
            info = f"{container.id[:12]} [bold purple]{container.name}[/bold purple] ({container.status})"
            
            if show_stats:
                try:
                    stats = container.stats(stream=False)
                    cpu = stats['cpu_stats']['cpu_usage']['total_usage']
                    mem = stats['memory_stats'].get('usage', 'N/A')
                    info += f" | CPU: {cpu} | RAM: {mem} bytes"
                except Exception as e:
                    info += " | [red]Stats indisponibles[/red]"
            
            console.print(info)
    except Exception as e:
        logging.error(f"Erreur lors du listing des containers: {e}")

def control_container(container_id, action):
    """
    Exécute une action de contrôle sur un container (start/stop/restart).
    
    Args:
        container_id (str): ID ou nom du container
        action (str): Action à exécuter (start/stop/restart)
    """
    try:
        container = client.containers.get(container_id)
        getattr(container, action)()  # Appel dynamique de la méthode
        
        # Message de confirmation coloré
        console.print(f"[green]Container {container.name} {action}é avec succès ![/green]")
    except docker.errors.NotFound:
        console.print(f"[red]Erreur: Container {container_id} introuvable ![/red]")
    except Exception as e:
        logging.error(f"Erreur lors de l'action {action}: {e}")

if __name__ == "__main__":
    # Configuration des arguments CLI avec argparse
    # while True:
    parser = argparse.ArgumentParser(
        description="Orchestrateur Docker CLI - Gestion avancée des containers",
        epilog="Exemples:\n"
            "  \n./orchestrator.py list --stats\n"
            "   (\nou si à la racine )\n"
            "  ./srcs/CLI/main.py restart mon_container"
    )
    
    subparsers = parser.add_subparsers(dest="command", title="commandes")

    # Commande 'list'
    list_parser = subparsers.add_parser("list", help="Lister les containers")
    list_parser.add_argument(
        "--stats", 
        action="store_true", 
        help="Afficher les statistiques CPU/RAM"
    )

    # Commandes de contrôle
    for action in ["start", "stop", "restart"]:
        action_parser = subparsers.add_parser(
            action, 
            help=f"{action} un container"
        )
        action_parser.add_argument(
            "container_id", 
            help="ID ou nom du container"
        )
    
    # Commande 'show_stats' (ajoutée séparément pour plus de clarté)
    stats_parser = subparsers.add_parser(
        "show_stats", 
        help="Afficher les stats détaillées d'un container"
    )
    stats_parser.add_argument(
        "container_id",  # CORRECTION: Ajout de l'argument manquant
        help="ID ou nom du container"
    )

    args = parser.parse_args()

    # Gestion des commandes
    if args.command == "list":
        list_containers(show_stats=args.stats)
    elif args.command in ["start", "stop", "restart"]:
        control_container(args.container_id, args.command)
    elif args.command == "show_stats":
        show_container_stats(args.container_id)  # CORRECTION: Passage de l'argument
    else:
        parser.print_help()
    time.sleep(1)