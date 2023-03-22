import pygame
from pygame._common import ColorValue


class Camera:
    """Camera pour le niveau."""
    
    def __init__(self) -> None:
        """Constructeur."""

        self.position: pygame.Vector2 = pygame.Vector2((0, 0))

        self._target_surf: pygame.Surface = pygame.Surface((0, 0))
        self._target_middle: pygame.Vector2 = pygame.Vector2()
    
    def begin_drawing(self, target_surf: pygame.Surface) -> None:
        """
        Commencer à dessiner.
        :param target_surf: La surface sur laquelle dessiner.
        """
        self._target_surf = target_surf
        self._target_middle = pygame.Vector2(target_surf.get_size()) / 2.0
    
    def end_drawing(self) -> None:
        """ """
    
    ############################################################################
    # MéTHODES DE DESSIN

    def draw_circle(self, color: ColorValue, center: pygame.Vector2,
            radius: float, width: float) -> None:
        
        pygame.draw.circle(
            self._target_surf, color,
            self._target_middle + center - self.position, radius,
            int(round(width))
        )