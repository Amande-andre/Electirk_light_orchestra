from fastapi import APIRouter, HTTPException, UploadFile, File
import services.docker_controle as docker_controle
import requests
import os

router = APIRouter()

######## GET methods ########
@router.get("/status", tags=["Health"])
def read_root():
    return {"message": "Electrik Light Orchestrator API is live"}

@router.get("/containers", tags=["Containers"])
def list_all_containers():
    return docker_controle.list_containers()

@router.get("/containers/{container_id}/stats", tags=["Containers"])
def get_container_stats(container_id: str):
    try:
        return docker_controle.get_container_stats(container_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

######## POST methods ########
@router.post("/containers/{container_id}/start", tags=["Containers"])
def start_container(container_id: str):
    try:
        docker_controle.start_container(container_id)
        return {"status": f"Container {container_id} started."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/containers/{container_id}/stop", tags=["Containers"])
def stop_container(container_id: str):
    try:
        return docker_controle.stop_container(container_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/containers/{container_id}/restart", tags=["Containers"])
def restart_container(container_id: str):
    try:
        docker_controle.restart_container(container_id)
        return {"status": f"Container {container_id} restarted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compile", tags=["Compiler"])
async def compile_c_file(file: UploadFile = File(...)):
    """
    Envoie un fichier C au conteneur compiler pour compilation et exécution
    """
    try:
        # Trouver l'ID du conteneur compiler
        containers = docker_controle.list_containers()
        compiler_container = next((c for c in containers if c["name"] == "compiler"), None)
        
        if not compiler_container:
            raise HTTPException(status_code=404, detail="Conteneur 'compiler' non trouvé")
        
        # S'assurer que le conteneur compiler est démarré
        if compiler_container["status"] != "running":
            docker_controle.start_container(compiler_container["id"])
        
        # Envoyer le fichier au service de compilation
        compiler_url = "http://compiler:5042/compile/"
        
        # Préparation des données pour la requête
        temp_file_content = await file.read()
        files = {"file": (file.filename, temp_file_content, "text/plain")}
        
        # Envoi de la requête au conteneur compiler
        try:
            response = requests.post(compiler_url, files=files, timeout=20)
            
            if response.status_code != 200:
                return {
                    "success": False, 
                    "error": f"Erreur lors de la compilation: {response.text}",
                    "output": None
                }
            
            return response.json()
            
        except requests.RequestException as e:
            return {
                "success": False, 
                "error": f"Erreur de connexion au compilateur: {str(e)}",
                "output": None
            }
            
    except Exception as e:
        return {
            "success": False, 
            "error": str(e),
            "output": None
        }