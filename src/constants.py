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

SCAN_PORT: int = 55357
HUB_PORT: int = 55321
SERVER_PORT: int = 55352
CLIENT_PORT: int = 55153

TIMEOUT: float = 1.0
PACKET_SIZE: int = 256

WAIT_MENU_REFRESH_INTERVAL: float = 0.5