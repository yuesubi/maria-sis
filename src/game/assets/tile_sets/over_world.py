import os
import pygame


# Chargement des tuiles du monde
OVER_WORLD_TILE_SET_PATH = os.path.join(os.path.dirname(__file__), "..", "..",
    "..", "..", "assets", "tilesets", "OverWorld.png")
OVER_WORLD_TILE_SET: pygame.Surface = \
    pygame.image.load(OVER_WORLD_TILE_SET_PATH)

# Liste avec toutes les tuiles
OVER_WORLD_TILES: list[pygame.Surface] = [
    OVER_WORLD_TILE_SET.subsurface(0, 0, 16, 16)
]