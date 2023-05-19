import sys

from .utils import Vec2


WIDTH_IN_BLOCKS: int = 16
HEIGHT_IN_BLOCKS: int = 13

CHUNK_WIDTH: int = 10
CHUNK_HEIGHT: int = 10
CHUNK_SIZE: tuple[int, int] = CHUNK_WIDTH, CHUNK_HEIGHT

UNIT: int = 16
SCALE: float = 2.0

CAMERA_OFFSET: Vec2 = Vec2(0, 0)

PLAYER_SPEED: float = 5.0

EPSILON: float = sys.float_info.epsilon

#########
# RESEAU

SCAN_PORT: int = 55351
HUB_PORT: int = 55322
GAME_SERVER_PORT: int = 52353
GAME_CLIENT_PORT: int = 51154

TIMEOUT: float = 1.0
PACKET_SIZE: int = 256

WAIT_MENU_REFRESH_INTERVAL: float = 0.5