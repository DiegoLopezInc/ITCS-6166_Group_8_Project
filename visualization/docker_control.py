"""
Docker Control Utilities for Dashboard
- Start/stop/restart containers
- Query container status
"""
import docker

try:
    client = docker.from_env()
except Exception as e:
    print(f"Docker SDK initialization failed: {e}")
    client = None

CONTROLLER_SERVICE = {
    'sdn_controller.py': 'ryu',
    'jasper_multicast_controller.py': 'ryu_jasper',
    'dbo_multicast_controller.py': 'ryu_dbo'
}

def switch_controller(controller_script):
    # Stop all ryu* containers, start the desired one
    for name in ['ryu', 'ryu_jasper', 'ryu_dbo']:
        try:
            c = client.containers.get(name)
            c.stop()
        except docker.errors.NotFound:
            pass
    target = CONTROLLER_SERVICE.get(controller_script)
    if target:
        try:
            c = client.containers.get(target)
            c.start()
        except docker.errors.NotFound:
            pass

def pause_marketdata():
    try:
        c = client.containers.get('marketdata')
        if c.status != 'running':
            print("[WARN] Marketdata container is not running and cannot be paused.")
            return False
        c.pause()
        return True
    except docker.errors.NotFound:
        print("[WARN] Marketdata container not found.")
        return False
    except docker.errors.APIError as e:
        print(f"[WARN] Could not pause Marketdata container: {e}")
        return False

def resume_marketdata():
    try:
        c = client.containers.get('marketdata')
        if c.status != 'paused':
            print("[WARN] Marketdata container is not paused and cannot be unpaused.")
            return False
        c.unpause()
        return True
    except docker.errors.NotFound:
        print("[WARN] Marketdata container not found.")
        return False
    except docker.errors.APIError as e:
        print(f"[WARN] Could not unpause Marketdata container: {e}")
        return False

def reset_demo():
    # Optionally restart all bots, api, marketdata, scoring
    for name in ['api_server', 'marketdata', 'bot1', 'bot2', 'bot3', 'bot4', 'reactivebot']:
        try:
            c = client.containers.get(name)
            c.restart()
        except docker.errors.NotFound:
            pass

def get_container_status(name):
    if client is None:
        return 'docker unavailable'
    try:
        c = client.containers.get(name)
        return c.status
    except docker.errors.NotFound:
        return 'not found'
    except Exception as e:
        print(f"Error getting container status: {e}")
        return 'error'
