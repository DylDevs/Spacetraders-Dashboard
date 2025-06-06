from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
import subprocess
import threading
import traceback
import uvicorn
import socket

import backend.variables as Variables
import backend.utils as Utils
from backend.logger import Logger
logger = Logger()

# Initialize FastAPI and add CORS
app = FastAPI(title="Spacetraders UI", 
    description="Webserver to handle connection between frontend and backend",
    version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client_connected = False
client_ip = None
@app.get("/")
async def Root(request: Request):
    '''
    Returns the webserver URL and IP

    Returns:
        `{"status": "ok"}`
    '''
    global client_connected, client_ip
    client_ip = request.client.host
    client_connected = True
    return {"status": "ok"}

@app.get("/systems")
async def Systems():
    try:
        dict_systems = []
        for system in Variables.systems:
            dict_systems.append(system.to_dict())
        return {"status": "ok", "systems": dict_systems}
    except:
        return {"status": "error", "traceback": traceback.format_exc()}
    
@app.get("/systems/current")
async def CurrentSystem():
    try:
        return {"status": "ok", "symbol": Variables.current_system}
    except:
        return {"status": "error", "traceback": traceback.format_exc()}

@app.get("/systems/{system_symbol}/waypoints")
async def Waypoints(system_symbol: str):
    try:
        if Variables.waypoints.get(system_symbol) is None:
            waypoints = Utils.LoadWaypoints(system_symbol)
            # Cache them in RAM for faster access
            Variables.waypoints[system_symbol] = waypoints
        else:
            # The waypoints have been accessed before
            waypoints = Variables.waypoints[system_symbol]
        return {"status": "ok", "waypoints": waypoints}
    except:
        return {"status": "error", "traceback": traceback.format_exc()}

def StartBackend():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")

def StartFrontend():
    # Redirect both stdout and stderr to /dev/null
    subprocess.run("cd ui && npm run dev", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def Run(frontend = True, backend = True):
    if backend: threading.Thread(target=StartBackend).start()
    if frontend: threading.Thread(target=StartFrontend).start()

def AwaitClient():
    global client_connected
    while not client_connected:
        pass
    return client_ip