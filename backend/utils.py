from spacetraders.models.get_status200_response_announcements_inner import GetStatus200ResponseAnnouncementsInner as Announcement
from spacetraders.models.get_status200_response import GetStatus200Response as HeartbeatResponse
from spacetraders.models.agent import Agent as AgentResponse
from spacetraders.models.waypoint import Waypoint
from spacetraders.models.system import System
import backend.variables as Variables
import backend.classes as Classes
from backend.logger import Logger
from datetime import datetime
import backend.api as API
import orjson as json
import psutil
import os

logger = Logger()
PAGE_SIZE_LIMIT = 20

def RAMUsage(unit : str = "Mb") -> float:
    if unit == "B": return psutil.Process(os.getpid()).memory_info().rss
    elif unit == "Kb": return psutil.Process(os.getpid()).memory_info().rss / 1024
    elif unit == "Mb": return psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    elif unit == "Gb": return psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024
    
# region Formatters

def FormatHeartbeat(data : dict) -> str:
    data_class = HeartbeatResponse.from_dict(data)
    def Announcments(announcements : list[Announcement]) -> str:
        return "\n        ".join([f"[grey39]{a.title}:[/] {a.body}" for a in announcements])
    
    return f"""[bold]{data_class.status}[/]
        [grey39]Version:[/] {data_class.version}
        [grey39]Last Reset:[/] {data_class.reset_date}
        [grey39]Next Reset:[/] {datetime.fromisoformat(data_class.server_resets.next).astimezone().strftime("%Y-%m-%d %I:%M:%S %p")}
        {Announcments(data_class.announcements)}
    """

def FormatAgent(data : dict) -> str:
    data_class = AgentResponse.from_dict(data)
    return f"""Successfully logged in as [bold]{data_class.symbol}[/]!
        [grey39]Credits:[/] {data_class.credits}
        [grey39]Headquarters:[/] {data_class.headquarters}
        [grey39]Ships:[/] {data_class.ship_count}
    """

# region Token Management

def AccountToken() -> str:
    if not os.path.exists(Variables.ACCOUNT_TOKEN_FILE):
        return None
        
    with open(Variables.ACCOUNT_TOKEN_FILE, "r") as f: 
        token = f.read().strip()
        return token

def AgentToken() -> str:
    if not os.path.exists(Variables.AGENT_TOKEN_FILE):
        return None
    with open(Variables.AGENT_TOKEN_FILE, "r") as f: 
        token = f.read().strip()
        return token
    
def SaveAccountToken(token : str) -> None:
    with open(Variables.ACCOUNT_TOKEN_FILE, "w") as f:
        f.truncate(0)
        f.write(token)
    
def SaveAgentToken(token : str) -> None:
    with open(Variables.AGENT_TOKEN_FILE, "w") as f:
        f.truncate(0)
        f.write(token)

# region Systems

def UpdateSystems() -> bool:
    """
    Update the systems cache
    """

    first_page = API.Handler(API.Request(f"systems?page=1&limit={PAGE_SIZE_LIMIT}"))
    systems: list[dict] = []
    if not first_page.success:
        logger.error(f"Failed to load systems: {first_page.error}")
        return False

    systems += [system for system in first_page.data]
    meta = first_page.other_tags["meta"]
    total_pages = meta["total"] // 20 + (1 if meta["total"] % 20 > 0 else 0)
    remaining_page_requests = [
        API.Request(f"systems?page={page}&limit={PAGE_SIZE_LIMIT}") for page in range(2, total_pages + 1)
    ]

    logger.info(f"Loading [bold]{total_pages}[/bold] pages of systems...")
    with logger.Progress() as progress:
        load_task = progress.add_task(f"Loaded [bold]1[/bold] pages of systems ([bold]{len(systems)}[/bold] systems)...", total=total_pages)
        with API.ThreadedHandler(remaining_page_requests) as handler:
            while handler.running:
                response = handler.AwaitResponse()
                if response is None: break # All requests have been completed
                if not response.success: # Failed
                    logger.error(f"Failed to load systems: {response.error}")
                    return False
                
                systems += [system for system in response.data]
                progress.update(load_task, advance=1, description=f"Loaded [bold]{handler.index}[/bold] pages of systems ([bold]{len(systems)}[/bold] systems)...")

        save_task = progress.add_task(f"Saving [bold]{len(systems)}[/bold] systems...", total=len(systems))
        for i, system in enumerate(systems):
            os.makedirs(f"{Variables.SYSTEMS_CACHE_FOLDER}/{system['symbol']}", exist_ok=True)
            with open(f"{Variables.SYSTEMS_CACHE_FOLDER}/{system['symbol']}/system.json", "wb") as f:
                f.write(json.dumps(system, option=json.OPT_INDENT_2))
            progress.update(save_task, advance=1, description=f"Saved [bold]{i + 1}[/bold] systems...")

        progress.stop()
    logger.info(f"Successfully loaded [bold]{len(systems)}[/bold] systems!")
    return True

def SystemsExist() -> bool:
    if not os.path.exists(Variables.SYSTEMS_CACHE_FOLDER): return False
    if len(os.listdir(Variables.SYSTEMS_CACHE_FOLDER)) == 0: return False
    return True

def SystemExists(symbol : str) -> bool:
    return os.path.exists(f"{Variables.SYSTEMS_CACHE_FOLDER}/{symbol}")

def LoadSystems(simple : bool = True) -> list[Classes.VisualizationSystem | System]:
    systems : list[System | Classes.VisualizationSystem] = []

    logger.info(f"Loading [bold]{len(os.listdir(Variables.SYSTEMS_CACHE_FOLDER))}[/bold] systems into memory...")
    with logger.Progress() as progress:
        load_task = progress.add_task(f"Loaded [bold]0[/bold] systems into memory...", total=len(os.listdir(Variables.SYSTEMS_CACHE_FOLDER)))
        for i, system in enumerate(os.listdir(Variables.SYSTEMS_CACHE_FOLDER)):
            with open(f"{Variables.SYSTEMS_CACHE_FOLDER}/{system}/system.json", "r") as f:
                data = json.loads(f.read())
                systems.append(Classes.VisualizationSystem.from_dict(data) if simple else System.from_dict(data))
            progress.update(load_task, advance=1, description=f"Loaded [bold]{i + 1}[/bold] systems into memory...")

        progress.stop()

    logger.info(f"Successfully loaded [bold]{len(systems)}[/bold] systems into memory!")

    return systems

# region Waypoints

def UpdateWaypoints(system_symbol : str) -> bool:
    """
    Update the waypoint cache for any given system
    """

    def preprocess(obj):
        """
        Recursively convert datetime objects in a dictionary to ISO 8601 strings.
        """
        if isinstance(obj, dict):
            return {key: preprocess(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [preprocess(item) for item in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 string
        return obj
    
    first_page = API.Handler(API.Request(f"systems/{system_symbol}/waypoints?page=1&limit={PAGE_SIZE_LIMIT}"))
    waypoints : list[dict] = []
    if not first_page.success:
        logger.error(f"Failed to load waypoints: {first_page.error}")
        return False
    
    waypoints += [waypoint for waypoint in first_page.data]
    meta = first_page.other_tags["meta"]
    total_pages = meta["total"] // 20 + (1 if meta["total"] % 20 > 0 else 0)
    remaining_page_requests = [
        API.Request(f"systems/{system_symbol}/waypoints?page={page}&limit={PAGE_SIZE_LIMIT}") for page in range(2, total_pages + 1)
    ]
    
    logger.info(f"Loading [bold]{total_pages}[/bold] pages of waypoints from system [bold]{system_symbol}[/bold]...")
    with logger.Progress() as progress:
        load_task = progress.add_task(f"Loaded [bold]1[/bold] pages of waypoints ([bold]{len(waypoints)}[/bold] waypoints) from system [bold]{system_symbol}[/bold]...", total=total_pages)
        with API.ThreadedHandler(remaining_page_requests) as handler:
            while handler.running:
                response = handler.AwaitResponse()
                if response is None: break
                if not response.success:
                    logger.error(f"Failed to load waypoints: {response.error}")
                    return False
                
                waypoints += [waypoint for waypoint in response.data]
                progress.update(load_task, advance=1, description=f"Loaded [bold]{handler.index}[/bold] pages of waypoints ([bold]{len(waypoints)}[/bold] systems)...")

        # Save the waypoints to their respective systems cache
        save_task = progress.add_task(f"Saving [bold]{len(waypoints)}[/bold] waypoints from system [bold]{system_symbol}[/bold]...", total=len(waypoints))
        for i, waypoint in enumerate(waypoints):
            os.makedirs(f"{Variables.SYSTEMS_CACHE_FOLDER}/{system_symbol}/waypoints", exist_ok=True)
            with open(f"{Variables.SYSTEMS_CACHE_FOLDER}/{system_symbol}/waypoints/{waypoint['symbol']}.json", "wb") as file:
                file.write(json.dumps(preprocess(waypoint), option=json.OPT_INDENT_2))
            progress.update(save_task, advance=1, description=f"Saved [bold]{i + 1}[/bold] waypoints from system [bold]{system_symbol}[/bold]...")

        progress.stop() 
    logger.info(f"Successfully loaded [bold]{len(waypoints)}[/bold] waypoints from system [bold]{system_symbol}[/bold]!")
    return True

def WaypointsExists(system_symbol : str) -> bool:
    return os.path.exists(f"{Variables.SYSTEMS_CACHE_FOLDER}/{system_symbol}/waypoints")

def LoadWaypoints(system_symbol : str, simple : bool = True) -> list[Waypoint]:
    if not WaypointsExists(system_symbol):
        logger.warning(f"Waypoints for system [bold]{system_symbol}[/bold] were requested, but they do not exist!")
        return []

    waypoints : list[Waypoint] = []
    for file in os.listdir(f"{Variables.SYSTEMS_CACHE_FOLDER}/{system_symbol}/waypoints"):
        with open(f"{Variables.SYSTEMS_CACHE_FOLDER}/{system_symbol}/waypoints/{file}", "r") as f:
            if simple:
                waypoints.append(Classes.VisualizationWaypoint.from_dict(json.loads(f.read())))
            else:
                waypoints.append(Waypoint.from_dict(json.loads(f.read())))

    logger.info(f"Successfully loaded [bold]{len(waypoints)}[/bold] waypoints from system [bold]{system_symbol}[/bold] into memory!")
    return waypoints

# region Agents

def MapAgents(systems : list[Classes.VisualizationSystem]) -> list[Classes.VisualizationSystem]:
    """
    Update a list of systems' agent tags
    """
    
    def GetAgentSystemDict(agent : dict) -> dict:
        return {
            "symbol": agent["symbol"].upper().strip(),
            "system": agent["headquarters"].replace(f"-A1", "").upper().strip()
        }
    
    agent_systems : list[dict] = [] # [{"symbol": symbol, "system": system}, ...]
    first_page = API.Handler(API.Request(f"agents?page=1&limit={PAGE_SIZE_LIMIT}", "GET"))
    if not first_page.success:
        logger.error(f"Failed to load agents: {first_page.error}")
        return False
    
    agent_systems += [GetAgentSystemDict(agent) for agent in first_page.data]
    for agent in agent_systems:
        for system in systems:
            if agent["system"] == system.symbol.upper().strip():
                system.agent = agent["symbol"]
                break

    meta = first_page.other_tags["meta"]
    total_pages = meta["total"] // 20 + (1 if meta["total"] % 20 > 0 else 0)
    remaining_page_requests = [
        API.Request(f"agents?page={page}&limit={PAGE_SIZE_LIMIT}") for page in range(2, total_pages + 1)
    ]
    
    logger.info(f"Loading and mapping [bold]{total_pages}[/bold] pages of agents...")
    with logger.Progress() as progress:
        load_task = progress.add_task(f"Loaded and mapped [bold]1[/bold] page of agents...", total=total_pages, completed=1)

        with API.ThreadedHandler(remaining_page_requests) as handler:
            while handler.running:
                response = handler.AwaitResponse()
                if response is None: break
                if not response.success:
                    logger.error(f"Failed to load agents: {response.error}")
                    return False
            
                # Map the agents to their systems
                new_agent_systems = [GetAgentSystemDict(agent) for agent in response.data]
                for agent in new_agent_systems:
                    for system in systems:
                        if agent["system"] == system.symbol.upper().strip():
                            system.agent = agent["symbol"]
                            break
                
                agent_systems += new_agent_systems
                progress.update(load_task, advance=1, description=f"Loaded and mapped [bold]{handler.index}[/bold] pages of agents ([bold]{len(agent_systems)}[/bold] agents)...")
        progress.stop()

    # Check if all agents were found
    agents_found = 0
    agents_total = len(agent_systems)
    for system in systems:
        if system.agent:
            agents_found += 1
    
    if agents_found < agents_total:
        logger.warning(f"Only [bold]{agents_found}[/bold] out of [bold]{agents_total}[/bold] agents were found")
    else:
        logger.info(f"Successfully loaded [bold]{len(agent_systems)}[/bold] agents and mapped them to systems")
    return systems