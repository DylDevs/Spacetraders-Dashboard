from typing import Any, Dict
from typing_extensions import Self
from spacetraders.models.waypoint_orbital import WaypointOrbital
from spacetraders.models.waypoint_type import WaypointType
from spacetraders.models.system_type import SystemType

class VisualizationSystem():
    '''Simplified system class for frontend visualization
    
    Attributes:
        symbol (str): The symbol of the system.
        name (str): The name of the system.
        type (SystemType): The type of the system.
        x (int): Relative position of the system in the sector in the x axis.
        y (int): Relative position of the system in the sector in the y axis.
        agent (Optional[str]): The symbol of the agent which has their headquarters in this system.
    '''

    def __init__(self, symbol: str, type: SystemType, x: int, y: int, agent: str = None):
        self.symbol = symbol
        self.type = type
        self.x = x
        self.y = y
        self.agent = agent

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "type": self.type,
            "x": self.x,
            "y": self.y,
            "agent": self.agent
        }

    @classmethod
    def from_dict(self, obj: Dict[str, Any]) -> Self:
        if obj is None:
            return None

        return self(
            symbol=obj.get("symbol"),
            type=obj.get("type"),
            x=obj.get("x"),
            y=obj.get("y"),
            agent=obj.get("agent")
        )
    
class VisualizationWaypoint():
    '''Simplified waypoint class for frontend visualization
    
    Attributes:
        symbol (str): The symbol of the waypoint.
        type (WaypointType): The type of the waypoint.
        x (int): Relative position of the waypoint on the system's x axis. This is not an absolute position in the universe.
        y (int): Relative position of the waypoint on the system's y axis. This is not an absolute position in the universe.
        orbitals (List[WaypointOrbital]): Waypoints that orbit this waypoint.
    '''

    def __init__(self, symbol: str, type: WaypointType, x: int, y: int, orbitals: list[WaypointOrbital]):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.orbitals = orbitals

        if not isinstance(type, WaypointType):
            self.type = WaypointType(type)
        else:
            self.type = type

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "type": self.type,
            "x": self.x,
            "y": self.y,
            "orbitals": self.orbitals
        }
    
    @classmethod
    def from_dict(self, obj: Dict[str, Any]) -> Self:
        if obj is None:
            return None

        return self(
            symbol=obj.get("symbol"),
            type=obj.get("type"),
            x=obj.get("x"),
            y=obj.get("y"),
            orbitals=obj.get("orbitals")
        )