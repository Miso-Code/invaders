from enum import Enum

BORDER_SIZE = 15
MAX_ENEMIES_PER_ROW = 10


class EnemyChasingStatus(str, Enum):
    STOP = "stop"
    JUMPING = "jumping"
    RETURNING = "returning"
