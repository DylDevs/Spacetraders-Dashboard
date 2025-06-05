from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.highlighter import NullHighlighter, RegexHighlighter
from backend.variables import LOG_FILE
import backend.variables as Variables
from rich.logging import RichHandler
from rich.console import Console
import logging
import inspect
import re
import os

# Logger is the first file to be imported from the main file, so we check the cache folder here
if not os.path.exists(Variables.CACHE):
    os.mkdir(Variables.CACHE)
    
class level_names:
    '''Shortened level names for logging'''
    debug = 'DBG'
    info = 'INF'
    warning = 'WRN'
    error = 'ERR'
    critical = 'CRT'

    def level(self, level_name):
        '''Returns the shortened level name for the given level name'''
        return getattr(self, level_name.lower())

class FileFormatter(logging.Formatter):
    '''Logging formatter class for file output'''
    def __init__(self):
        super().__init__(datefmt="%m-%d-%y %H:%M:%S")

    def format(self, record):
        timestamp = self.formatTime(record, self.datefmt) # Timestamp
        level_name = f"[{level_names().level(record.levelname)}]" # Three character level name
        message = re.sub(r'\[.*?\]', '', record.getMessage()) # Remove rich markup

        # Get filename and line number
        filename = os.path.basename(getattr(record, 'custom_filename', record.filename))
        lineno = getattr(record, 'custom_lineno', record.lineno)

        return f"{timestamp} {level_name} ({filename}:{lineno}) {message}" # Return formatted message

class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.console = Console()
        self.progress = None

        if not self.logger.handlers:
            logging.basicConfig(
                level=logging.INFO, format="%(message)s", datefmt="[%X]", 
                handlers=[RichHandler(markup=True, show_path=False, console=self.console)]
            )

            if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
            file_handler = logging.FileHandler(LOG_FILE)
            file_handler.setFormatter(FileFormatter())
            self.logger.addHandler(file_handler)

            self.info('Logger initialized')

    def _log(self, level, message, highlight=True, markdown=True):
        # Get the frame of the caller
        frame = inspect.currentframe()
        try:
            # Go back 2 frames: 1 for this method, 1 for the wrapper method
            caller_frame = frame.f_back.f_back
            caller_info = inspect.getframeinfo(caller_frame)
            
            extra = {
                "highlighter": RegexHighlighter() if highlight else NullHighlighter(),
                "markdown": markdown,
                "custom_filename": caller_info.filename,
                "custom_lineno": caller_info.lineno
            }
            
            getattr(self.logger, level)(message, extra=extra)
        finally:
            del frame
    
    def debug(self, message, highlight=True, markdown=True):        
        self._log("debug", message, highlight, markdown)

    def info(self, message, highlight=True, markdown=True):
        self._log("info", message, highlight, markdown)

    def warning(self, message, highlight=True, markdown=True):
        self._log("warning", message, highlight, markdown)

    def error(self, message, highlight=True, markdown=True):
        self._log("error", message, highlight, markdown)

    def critical(self, message, highlight=True, markdown=True):
        self._log("critical", message, highlight, markdown)

    def Progress(self):
        return Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(),
            console=self.console  # Share console to avoid conflict
        )