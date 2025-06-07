import os

# Top level directory
PATH = os.path.dirname(os.path.dirname(__file__))
# Cache directory
CACHE = os.path.join(PATH, 'cache')
# Log file location
LOG_FILE = os.path.join(CACHE, 'app.log')
# Account token file location
ACCOUNT_TOKEN_FILE = os.path.join(CACHE, 'account_token.txt')
# Agent token file location
AGENT_TOKEN_FILE = os.path.join(CACHE, 'agent_token.txt')
# Webserver cache file location
WEBSERVER_CACHE_FILE = os.path.join(CACHE, 'webserver_cache.txt')
# Systems cache folder location
SYSTEMS_CACHE_FOLDER = os.path.join(CACHE, 'systems')

# Agent name (If you are not DylDev, please change this)
AGENT_NAME = "DylDev"

# Account token variable
account_token : str = ""
# Agent token variable
agent_token : str = ""

# Variable to hold systems when loaded to memory
systems : list = []
# The system that the agent is currently in
current_system : str = ""
# Dictionary of systems and their waypoints (this will not include all systems, only ones that have been cached by the frontend)
waypoints : dict = {}

# Instance of backend.api, this is to prevent circular imports in files that the API uses
API = None