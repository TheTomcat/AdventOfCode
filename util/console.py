import logging 
from rich.console import Console
from rich.logging import RichHandler

console = Console(color_system='truecolor')

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")