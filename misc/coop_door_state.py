from enum import Enum, auto

class CoopDoorState(Enum):
    OPEN = auto()
    CLOSED = auto()
    STOPPED = auto()
    RUNNING = auto()
