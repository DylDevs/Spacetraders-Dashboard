# This database file is not currently being used, it will be used in the future
# Probably switched to PostgreSQL

import backend.variables as Variables
from backend.logger import Logger
from pathlib import Path
import os

logger = Logger()

class IndexPath(Path):
    def __init__(self, path : Path) -> None:
        super().__init__(path)
        if not self.exists():
            logger.error(f"Database index path '{path}' does not exist!")
            raise FileNotFoundError(f"Database index path '{path}' does not exist!")

INDEX_PATHS : list[Path] = [
    Path(Variables.PATH) / "cache" / "systems",
    Path(Variables.PATH) / "cache" / "systems" / {Variables.current_system} / "waypoints"
]

class Database:
    def __init__(self) -> None:
        self.paths : list[Path] = INDEX_PATHS
        self._PathsExist() # Will raise FileNotFoundError if path(s) do not exist

    def _PathsExist(self) -> bool:
        for path in self.paths:
            if not path.exists():
                logger.error(f"Database index path '{path}' does not exist!")
                raise FileNotFoundError("Database index paths do not exist!")
        return True
    
    def _TotalFiles(self) -> int:
        total = 0
        for path in self.paths:
            total += len(os.listdir(path))
        return total