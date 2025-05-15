import docker

client = docker.from_env()

def list_containers():
    containers = client.containers.list(all=True)
    return [
        {
            "id": container.id,
            "name": container.name,
            "status": container.status,
            "image": container.image.tags[0] if container.image.tags else "N/A",
        }
        for container in containers
    ]

def start_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.start()
        return {"status": f"Container {container.name} started."}
    except docker.errors.NotFound:
        return {"error": "Container not found."}
    except Exception as e:
        return {"error": str(e)}

def stop_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return {"status": f"Container {container.name} stopped."}
    except docker.errors.NotFound:
        return {"error": "Container not found."}
    except Exception as e:
        return {"error": str(e)}

def restart_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.restart()
        return {"status": f"Container {container.name} restarted."}
    except docker.errors.NotFound:
        return {"error": "Container not found."}
    except Exception as e:
        return {"error": str(e)}

def get_container_stats(container_id):
    try:
        container = client.containers.get(container_id)
        stats = container.stats(stream=False)
        cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
        mem_usage = stats['memory_stats']['usage']
        network_in = stats['networks']['eth0']['rx_bytes']
        network_out = stats['networks']['eth0']['tx_bytes']
        
        return {
            "cpu_usage": cpu_usage,
            "mem_usage": mem_usage,
            "network_in": network_in,
            "network_out": network_out
        }
    except docker.errors.NotFound:
        return {"error": "Container not found."}
    except Exception as e:
        return {"error": str(e)}
        