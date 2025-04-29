from fastapi import APIRouter

router = APIRouter()

@router.get("/status", tags=["Health"])
def read_root():
    return {"message": "Electrik Light Orchestrator API is live"}

@router.get("/containers", tags=["Containers"])
def list_all_containers():
    return docker_controle.list_containers()

@router.post("/containers/{container_id}/start", tags=["Containers"])
def start_container(container_id: str):
    try:
        return docker_controle.start_container(container_id)
    except Exeption as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/containers/{container_id}/stop", tags=["Containers"])
def stop_container(container_id: str):
    try:
        return docker_controle.stop_container(container_id)
    except Exeption as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/containers/{container_id}/restart", tags=["Containers"])
def restart_container(container_id: str):
    try:
        return docker_controle.restart_container(container_id)
    except Exeption as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/containers/{container_id}/stats", tags=["Containers"])
def get_container_stats(container_id: str):
    try:
        return docker_controle.get_container_stats(container_id)
    except Exeption as e:
        raise HTTPException(status_code=500, detail=str(e))