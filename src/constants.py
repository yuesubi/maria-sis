import sys


CHUNK_WIDTH: int = 10
CHUNK_HEIGHT: int = 10
CHUNK_SIZE: tuple[int, int] = CHUNK_WIDTH, CHUNK_HEIGHT

UNIT: int = 16
SCALE: float = 2.0

PLAYER_SPEED: float = 5.0

EPSILON: float = sys.float_info.epsilon

#########
# RESEAU

SERVER_PORT: int = 55357
CLIENT_PORT: int = 55153

TIMEOUT: float = 1.0
PACKET_SIZE: int = 256

WAIT_MENU_REFRESH_INTERVAL: float = 0.5