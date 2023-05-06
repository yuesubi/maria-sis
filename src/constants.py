import sys


CHUNK_WIDTH: int = 10
CHUNK_HEIGHT: int = 10
CHUNK_SIZE: tuple[int, int] = CHUNK_WIDTH, CHUNK_HEIGHT

UNIT: int = 16
SCALE: float = 2.0

PLAYER_SPEED: float = 5.0

EPSILON: float = sys.float_info.epsilon

SERVER_PORT = 55357
CLIENT_PORT = 55153

TIMEOUT = 1.0
PACKET_SIZE = 1024