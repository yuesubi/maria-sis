import os
import pyray as pr


# Chargement des tuiles du monde
OVER_WORLD_TILE_SET = os.path.join(os.path.dirname(__file__), "..", "..",
    "..", "..", "assets", "tilesets", "OverWorld.png")

# Liste avec toutes les tuiles
OVER_WORLD_TILES: list[pr.Rectangle] = list(map(
    lambda rec_tuple: pr.Rectangle(
        rec_tuple[0], rec_tuple[1],
        rec_tuple[2], rec_tuple[3]
    ), [
        (0, 0, 16, 16),
        (16, 0, 16, 16),
        (32, 0, 16, 16),
        (48, 0, 16, 16),
        (64, 0, 16, 16),

        (96, 0, 16, 16),
        (112, 0, 16, 16),
        (96, 16, 16, 16),
        (112, 16, 16, 16),
    ]
))