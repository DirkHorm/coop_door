from enum import Enum, auto

class CoopDoorState(Enum):
    OPEN = auto()
    CLOSED = auto()
    STOP = auto()
    RUNNING = auto()
    UNKNOWN = auto()
