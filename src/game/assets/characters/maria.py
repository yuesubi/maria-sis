import os
import pygame


# Chargement de l'ensemble des tuiles de Maria
MARIA_SPRITE_SHEET_PATH = os.path.join(os.path.dirname(__file__), "..", "..",
    "..", "..", "assets", "Characters", "Mario.png")
MARIA_SPRITE_SHEET: pygame.Surface = pygame.image.load(MARIA_SPRITE_SHEET_PATH)

# Liste des frames de Maria
MARIA_FRAMES: list[pygame.Surface] = [
    MARIA_SPRITE_SHEET.subsurface(8, 0, 16, 32)
]