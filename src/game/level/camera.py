import pyray as pr

from ...constants import UNIT
from ...utils import Vec2


class Camera:
    """Camera pour le niveau."""
    
    def __init__(self) -> None:
        """Constructeur."""

        self.position: Vec2 = Vec2.null

        self._target_middle: Vec2 = Vec2.null
    
    def begin_render(self) -> None:
        """Commencer le rendu."""
        self._target_middle = \
            Vec2.from_xy(pr.get_screen_width, pr.get_screen_height()) / 2.0
    
    def end_render(self):
        """Terminer le rendu."""

        # Rien à faire, la méthode existe juste au cas où on en aurait besoin.
    
    ############################################################################
    # MÉTHODES DE DESSIN

    def draw_texture(self, texture: pr.Texture, center: Vec2) -> None: ...
    def draw_texture_part(self, texture: pr.Texture, center: Vec2,
            part: pr.Rectangle) -> None: ...
    def draw_circle(self, center: Vec2, radius: float, color: pr.Color) -> None: ...
    def draw_circle_lines(self, center: Vec2, radius: float, color: pr.Color
            ) -> None: ...
    def draw_rect(self, center: Vec2, dimensions: Vec2, color: pr.Color
            ) -> None: ...
    def draw_rect_lines(self, center: Vec2, dimensions: Vec2, color: pr.Color,
            thickness: float) -> None: ...
    
    def _draw_surface(self, center: Vec2, surface: pr.Texture) -> None:
        """
        Dessiner une surface.
        :param center: La position du centre du cercle.
        :param surface: La surface à dessiner.
        """
        pr.draw_texture_pro(
            surface, pr.Rectangle(0, 0, surface.width, surface.height),

        )
        self._target_surf.blit(
            surface,
            (self._target_middle + UNIT*(center - self.position) - \
                Vec2.from_xy(surface.get_size()) / 2.0).xy
        )
    
    def _draw_circle(self, color: pygame.Color, center: Vec2,
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
            (self._target_middle + UNIT*(center - self.position)).xy,
            radius,
            width
        )
    
    def _draw_rect(self, color: pygame.Color, position: Vec2,
            size: Vec2, width: int = 0) -> None:
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
                (self._target_middle + UNIT * (position - self.position) -
                    size / 2.0).xy,
                size.xy
            ),
            width
        )