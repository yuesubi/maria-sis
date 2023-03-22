import pygame


class Camera:
    """Camera pour le niveau."""
    
    def __init__(self) -> None:
        """Constructeur."""

        self.position: pygame.Vector2 = pygame.Vector2((0, 0))

        self._target_surf: pygame.Surface = pygame.Surface((0, 0))
        self._target_middle: pygame.Vector2 = pygame.Vector2()
    
    def begin_render(self, target_surf: pygame.Surface) -> None:
        """
        Commencer le rendu.
        :param target_surf: La surface sur laquelle faire le rendu.
        """
        self._target_surf = target_surf
        self._target_middle = pygame.Vector2(target_surf.get_size()) / 2.0
    
    def end_render(self):
        """Terminer le rendu."""

        # Rien à faire, la méthode existe juste au cas où on en aurait besoin.
    
    ############################################################################
    # MÉTHODES DE DESSIN

    def draw_circle(self, color: pygame.Color, center: pygame.Vector2,
            radius: float, width: int = 0) -> None:
        """
        Dessiner un cercle.
        :param color: La couleur du cercle.
        :param center: La position du centre du cercle.
        :param radius: Le rayon du cercle.
        :param width: (optionnel) L'épaisseur du cercle, si elle est de 0 tout
            le cercle est plein.
        """
        
        pygame.draw.circle(
            self._target_surf, color,
            self._target_middle + center - self.position, radius,
            width
        )
    
    def draw_rect(self, color: pygame.Color, position: pygame.Vector2,
            size: pygame.Vector2, width: int = 0) -> None:
        """
        Dessiner un rectangle.
        :param color: La couleur du rectangle.
        :param position: La position du centre du rectangle.
        :param size: Les dimensions du rectangle.
        :param width: (optionnel) L'épaisseur du rectangle, si elle est de 0
            tout le rectangle est plein.
        """
        
        pygame.draw.rect(
            self._target_surf, color,
            pygame.Rect(
                self._target_middle + position - self.position - size/2.0,
                size
            ),
            width
        )