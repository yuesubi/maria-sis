import pyray as pr

from ...constants import UNIT, SCALE
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
            Vec2(pr.get_screen_width(), pr.get_screen_height()) / 2.0
    
    def end_render(self):
        """Terminer le rendu."""

        # Rien à faire, la méthode existe juste au cas où on en aurait besoin.
    
    ############################################################################
    # MÉTHODES DE DESSIN

    def draw_texture(self, texture: pr.Texture, center: Vec2) -> None:
        """
        Dessiner une texture.
        :param texture: La texture à dessiner.
        :param center: La position à laquelle dessiner la texture.
        """
        pos = self._target_middle + SCALE*UNIT*(center - self.position) - \
                Vec2(texture.width, texture.height) / 2.0
        pr.draw_texture_pro(
            texture, pr.Rectangle(0, 0, texture.width, texture.height),
            pr.Rectangle(
                pos.x, pos.y,
                int(texture.width*SCALE), int(texture.height*SCALE)
            ),
            pr.Vector2(texture.width/2, texture.height/2), 0.0, pr.WHITE
        )

    def draw_texture_part(self, texture: pr.Texture, center: Vec2,
            part: pr.Rectangle) -> None:
        """
        Dessiner une partie d'une texture.
        :param texture: La texture à dessiner.
        :param center: La position à laquelle dessiner la texture.
        :param part: La partie à dessiner.
        """
        pos = self._target_middle + SCALE*UNIT*(center - self.position) - \
                Vec2(part.width, part.height) / 2.0
        pr.draw_texture_pro(
            texture, part,
            pr.Rectangle(
                pos.x, pos.y,
                int(part.width*SCALE), int(part.height*SCALE)
            ),
            pr.Vector2(part.width/2, part.height/2), 0.0, pr.WHITE
        )

    def draw_circle(self, center: Vec2, radius: float, color: pr.Color) -> None:
        """
        Dessiner un cercle.
        :param center: La position du centre du cercle.
        :param radius: Le rayon du cercle.
        :param color: La couleur du cercle.
        """
        pos = self._target_middle + SCALE*UNIT*(center - self.position)
        pr.draw_circle(pos.x, pos.y, radius*UNIT*SCALE, color)

    def draw_circle_lines(self, center: Vec2, radius: float, color: pr.Color
            ) -> None:
        """
        Dessiner le contour d'un cercle.
        :param center: La position du centre du cercle.
        :param radius: Le rayon du cercle.
        :param color: La couleur du cercle.
        """
        pos = self._target_middle + SCALE*UNIT*(center - self.position)
        pr.draw_circle_lines(pos.x, pos.y, radius*UNIT*SCALE, color)
    
    def draw_rect(self, center: Vec2, dimensions: Vec2, color: pr.Color
            ) -> None:
        """
        Dessiner un rectangle.
        :param center: La position du centre du rectangle.
        :param dimensions: Les dimensions du rectangle.
        :param color: La couleur du rectangle.
        """
        pos = self._target_middle + UNIT * (center - self.position) - \
            dimensions / 2.0
        pr.draw_rectangle(
            pos.x, pos.y,
            dimensions.x*SCALE*UNIT, dimensions.y*SCALE*UNIT,
            color
        )

    def draw_rect_lines(self, center: Vec2, dimensions: Vec2, color: pr.Color,
            thickness: float = 0.0) -> None:
        """
        Dessiner un rectangle.
        :param center: La position du centre du rectangle.
        :param dimensions: Les dimensions du rectangle.
        :param color: La couleur du rectangle.
        :param thickness: (optionnel) L'épaisseur du rectangle, si elle est de 0
            tout le rectangle est plein.
        """
        pos = self._target_middle + UNIT * (center - self.position) - \
            dimensions / 2.0
        pr.draw_rectangle_lines_ex(
            pr.Rectangle(
                pos.x, pos.y,
                dimensions.x*SCALE*UNIT, dimensions.y*SCALE*UNIT,
            ),
            thickness, color
        )