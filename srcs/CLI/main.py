#!/usr/bin/env python3
"""
Docker CLI Orchestrator
Un outil pour gérer et surveiller les containers Docker avec une interface CLI.
Et une API pour l'intégration avec Prometheus et Grafana.
Avec une interface web FastAPI pour la visualisation des stats.
Dans un premier temps, recevoir et revoyer du text.
"""

import docker
import logging
import argparse
import sys
import time
import requests
from rich.console import Console
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import Response, HTMLResponse
from api.routes import router
from http.server import HTTPServer, SimpleHTTPRequestHandler
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import start_http_server
from pathlib import Path
from fastapi.staticfiles import StaticFiles



app = FastAPI(title="Electrik Light Orchestrator")

# app.mount(
#     "/static",
#     StaticFiles(directory="srcs/CLI/web", html=True),
#     name="static"
# )

# Registering FastAPI routes
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    html_path = Path(__file__).parent / "web" / "index.html"
    return html_path.read_text(encoding="utf-8")
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
def serve_html():
    return FileResponse("srcs/CLI/web/index.html")
    

@router.post("/submit", response_class=HTMLResponse)
async def submit_text(user_text: str = "Enter text here"):
    # Ici tu peux logguer, stocker ou traiter le texte
    print(f"Texte reçu : {user_text}")
    return f"<h2>Merci pour votre texte !</h2><p>{user_text}</p>"
    
# Rich console for styled output
console = Console()

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Docker client
try:
    client = docker.from_env()
except Exception as e:
    logging.error(f"Erreur lors de l'initialisation du client Docker: {e}")
    sys.exit(1)


def show_container_stats(container_name):
    """
    Affiche les statistiques temps réel d'un container spécifique.
    """
    try:
        container = client.containers.get(container_name)
        stats = container.stats(stream=False)

        cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
        mem_usage = stats['memory_stats']['usage'] / 1024 / 1024
        network_in = stats['networks']['eth0']['rx_bytes']
        network_out = stats['networks']['eth0']['tx_bytes']

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
    Liste tous les containers Docker avec leurs statuts.
    """
    try:
        containers = client.containers.list(all=True)

        for container in containers:
            info = f"{container.id[:12]} [bold purple]{container.name}[/bold purple] ({container.status})"
            
            if show_stats:
                try:
                    stats = container.stats(stream=False)
                    cpu = stats['cpu_stats']['cpu_usage']['total_usage']
                    mem = stats['memory_stats'].get('usage', 0) / 1024 / 1024
                    info += f" | CPU: {cpu} | RAM: {mem:.2f} MB"
                except Exception:
                    info += " | [red]Stats indisponibles[/red]"

            console.print(info)
    except Exception as e:
        logging.error(f"Erreur lors du listing des containers: {e}")


def control_container(container_id, action):
    """
    Exécute une action sur un container Docker.
    """
    try:
        container = client.containers.get(container_id)
        getattr(container, action)()
        console.print(f"[green]Container {container.name} {action} avec succès ![/green]")
    except docker.errors.NotFound:
        console.print(f"[red]Erreur: Container {container_id} introuvable ![/red]")
    except Exception as e:
        logging.error(f"Erreur lors de l'action {action}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Orchestrateur Docker CLI - Gestion avancée des containers",
        epilog="Exemples:\n"
               "  ./orchestrator.py list --stats\n"
               "  ./orchestrator.py restart mon_container"
    )

    subparsers = parser.add_subparsers(dest="command", title="commandes")

    # Commande 'list'
    list_parser = subparsers.add_parser("list", help="Lister les containers")
    list_parser.add_argument(
        "--stats",
        action="store_true",
        help="Afficher les statistiques CPU/RAM"
    )

    # Commandes start/stop/restart
    for action in ["start", "stop", "restart"]:
        action_parser = subparsers.add_parser(action, help=f"{action} un container")
        action_parser.add_argument("container_id", help="ID ou nom du container")

    # Commande 'show_stats'
    stats_parser = subparsers.add_parser("show_stats", help="Afficher les stats d’un container")
    stats_parser.add_argument("container_id", help="ID ou nom du container")

    args = parser.parse_args()

    if args.command == "list":
        list_containers(show_stats=args.stats)
    elif args.command in ["start", "stop", "restart"]:
        control_container(args.container_id, args.command)
    elif args.command == "show_stats":
        show_container_stats(args.container_id)
    else:
        parser.print_help()