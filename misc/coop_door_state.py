from enum import Enum, auto

class CoopDoorState(Enum):
    OPEN = auto()
    # CLOSED is the state
    CLOSED = auto()
    # CLOSE is the command
    CLOSE = auto()
    STOP = auto()
    RUNNING = auto()
    UNKNOWN = auto()
