'''
Spacetraders API Dashboard

Spacetraders API is a game that allows you to control a fleet of ships to
explore a universe full of systems and waypoints. This is a dashboard that
allows you to manage your fleet and navigate the universe.

Programming Notes:
- Any functions which begin with an underscore (_) are local and should not be
  called directly.
- Spacetraders API is limited to a maximum of 2 requests per second. The API
  handler will automatically handle rate limiting and threading of requests.
- Use the `backend.logger.Logger` class to log messages to the console. Don't
  use the standard `print()` function or any other logging library.
- Use the `backend.varaibles` file to store global variables.
- Thouroughly comment and document your code to make it easy to understand.
- Use OOP to make your code more modular and reusable.
- Use files from the `spacetraders.models` library to access API specs and
  intellisense features.
- Don't abuse the API, it is limited to 2 requests per second, you can be
  banned if you exceed this limit too many times.

Copyright (c) 2025 DylDev (https://github.com/DylDevs)
'''

# Initialize logger
from backend.logger import Logger
logger = Logger()

# Import external libraries
import shutil
import sys

# Import Spacetraders API models
from spacetraders.models.agent import Agent

# Import internal modules
import backend.variables as Variables
import backend.server as Server
import backend.utils as Utils
import backend.api as API

# Constants
FORCE_SYSTEMS_UPDATE = False

# Get account and agent tokens from files
Variables.account_token = Utils.AccountToken()
# If this is the first register, the agent token will be "Register"
Variables.agent_token = Utils.AgentToken()

# Check if API is available
heartbeat = API.Handler(API.Request(""))
if heartbeat.success:
    logger.info(Utils.FormatHeartbeat(heartbeat.data), highlight=False)
else:
    logger.critical(f"Spacetraders API is not available! More details: {heartbeat.status_code} - {heartbeat.error}\nPress enter to exit...")
    input()
    sys.exit()

# Login or register agent
registered = False
login_request = API.Handler(API.Request("my/agent"))
if not login_request.success:
    if str(login_request.status_code) == "4113" or Variables.agent_token == "Register": # Agent not found
        logger.warning("Server wipe detected, registering new agent...")
        register_request = API.Handler(API.Request("register", "POST", {'symbol': Variables.AGENT_NAME, 'faction': 'UNITED'}))

        if not register_request.success:
            logger.critical(f"Failed to register agent: {register_request.error}\nPress enter to exit...")
            input()
            sys.exit()
        else:
            logger.info(f"Successfully registered as [bold]{register_request.data['agent']['symbol']}[/]!")
            Utils.SaveAgentToken(register_request.data['token'])
            registered = True

        login_request = API.Handler(API.Request("my/agent"))
        if not login_request.success:
            logger.critical(f"Failed to log in: {login_request.error}\nPress enter to exit...")
            input()
            sys.exit()
    else: 
        logger.critical(f"Failed to log in: {login_request.error}\nPress enter to exit...")
        input()
        sys.exit()

# Create local Agent class from login data
agent_data = Agent.from_dict(login_request.data)

# Update the current system to the headquarters
Variables.current_system = agent_data.headquarters.replace(f"-A1", "")

# Log agent data
logger.info(Utils.FormatAgent(agent_data), highlight=False)

# Systems only change when the servers are wiped, so we cache them each time the wipe happens
# If we had to register again, this means the wipe happened, so we need to get the systems again
# We also check to ensure the systems cache folder exists
if registered or FORCE_SYSTEMS_UPDATE or not Utils.SystemsExist():
    # Clear systems cache folder
    try:
        shutil.rmtree(Variables.SYSTEMS_CACHE_FOLDER)
    except FileNotFoundError:
        pass # Ignore if the folder doesn't exist
    except Exception as e:
        logger.critical(f"Failed to clear systems cache folder: {e}, press enter to exit...")
        input()
        sys.exit()

    if registered:
        logger.info("Wipe detected, updating systems cache...")
    elif FORCE_SYSTEMS_UPDATE:
        logger.warning("Forcing systems update...")
    elif not Utils.SystemsExist():
        logger.warning("Systems cache does not exist, updating...")

    # Update systems
    update_systems_status = Utils.UpdateSystems()
    if not update_systems_status:
        logger.critical("Failed to update systems cache, press enter to exit...")
        input()
        sys.exit()

    # Update waypoints for the headquarters system (This is temporary until I don't suck)
    home_agent_symbol = agent_data.headquarters.replace(f"-A1", "")
    update_waypoints_status = Utils.UpdateWaypoints(home_agent_symbol)
    if not update_waypoints_status:
        logger.critical("Failed to update waypoints cache, press enter to exit...")
        input()
        sys.exit()

# Load systems into memory and map agents to systems
Variables.systems = Utils.LoadSystems()
Variables.systems = Utils.MapAgents(Variables.systems)

# Start frontend and server
Server.Run()

# Wait for client connection to the frontend
logger.info("Waiting for client connection to continue...")
Server.AwaitClient()
logger.info("Client connected! Starting mainloop...")

# Mainloop
while True:
    pass