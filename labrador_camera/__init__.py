import logging
from rich.logging import RichHandler
logging.basicConfig(level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])

from .labrador_camera import *
from .tomate_camera_sd import *
