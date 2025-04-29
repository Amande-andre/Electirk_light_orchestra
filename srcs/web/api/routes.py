from fastapi import APIRouter
import docker
from services.metrics import prometheus_metrics

router = APIRouter()
client = docker.from_env()

@router.post("/containers/{container_id}/stats")
def get_container_stats(container_id: str):
    try:
        container = client.containers.get(container_id)
        stats = container.stats(stream=False)
        
        cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
        mem_usage = stats['memory_stats']['usage'] / 1024 / 1024
        net_in = stats['networks']['eth0']['rx_bytes']
        net_out = stats['networks']['eth0']['tx_bytes']

        return {
            "container": container.name,
            "cpu_usage": cpu_usage,
            "memory_usage_mb": mem_usage,
            "network_in": net_in,
            "network_out": net_out
        }
    except docker.errors.NotFound:
        return {"error": "Container not found"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/metrics", tags=["Metrics"])
def get_metrics():
    metrics_data = prometheus_metrics()
    return Response(content=metrics_data, media_type="text/plain")