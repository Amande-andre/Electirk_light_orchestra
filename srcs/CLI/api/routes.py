from fastapi import APIRouter, HTTPException
import services.docker_controle as docker_controle

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
        return  {"status": f"Container {container_id} started."}
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


######## PUT methods ########

######## DELETE methods ########