from enum import Enum

BORDER_SIZE = 15
MAX_ENEMIES_PER_ROW = 10
TIMER: int = 3
BLINK = 1


class EnemyChasingStatus(str, Enum):
    STOP = "stop"
    JUMPING = "jumping"
    RETURNING = "returning"


class PlayerMovement(Enum):
    LEFT = -1
    RIGHT = 1
    STOP = 0
