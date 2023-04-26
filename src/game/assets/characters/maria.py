import os
import pyray as pr


# Chargement de l'ensemble des tuiles de Maria
MARIA_SPRITE_SHEET = os.path.join(os.path.dirname(__file__), "..", "..",
    "..", "..", "assets", "characters", "maria.png")

# Liste des frames de Maria
MARIA_FRAMES: list[pr.Rectangle] = list(map(
    lambda rec_tuple: pr.Rectangle(
        rec_tuple[0], rec_tuple[1],
        rec_tuple[2], rec_tuple[3]
    ),
    [
        (8, 0, 16, 32)
    ]
))