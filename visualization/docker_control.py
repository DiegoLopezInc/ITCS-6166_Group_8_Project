"""
Docker Control Utilities for Dashboard
- Start/stop/restart containers
- Query container status
"""
import docker

client = docker.from_env()

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
        c.pause()
    except docker.errors.NotFound:
        pass

def resume_marketdata():
    try:
        c = client.containers.get('marketdata')
        c.unpause()
    except docker.errors.NotFound:
        pass

def reset_demo():
    # Optionally restart all bots, api, marketdata, scoring
    for name in ['api_server', 'marketdata', 'bot1', 'bot2', 'bot3', 'bot4', 'reactivebot']:
        try:
            c = client.containers.get(name)
            c.restart()
        except docker.errors.NotFound:
            pass

def get_container_status(name):
    try:
        c = client.containers.get(name)
        return c.status
    except docker.errors.NotFound:
        return 'not found'
