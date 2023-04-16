import pygame

from .....utils import Vec2
from ..anchor import Anchor
from ..fit import Fit
from ..widget import Widget


# Initialiser le module de texte de pygame
if not pygame.font.get_init():
    pygame.font.init()


class Text(Widget):
    """Élément de texte de l'IHM."""

    def __init__(
            self,
            position: Vec2,
            anchor: Anchor,
            text: str,
            font_color: pygame.Color,
            font_size: int,
            font_style: str = str(),
            background_color: pygame.Color | None = None
        ) -> None:
        """
        Constructeur d'un texte.
        :param position: La position du texte.
        :param anchor: L'ancre du texte.
        :param text: Le texte de l'élément.
        :param font_color: La couleur du texte.
        :param font_size: La taille du texte.
        :param font_style: La police du texte. (optionnel)
        :param background_color: La couleur de fond du texte, si la couleur
            est None, le fond est transparent. (optionnel)
        """

        # Initialisation de la classe parent
        super().__init__(
            position, anchor,
            Vec2(1, 1), Fit.NONE
        )

        self.font_color: pygame.Color = pygame.Color(font_color)
        self.background_color: pygame.Color | None = background_color

        self._text: str = str(text)

        self._font_size: int = int(font_size)
        self._font_style: int = str(font_style)

        # Création d'une police
        self._font: pygame.font.Font = pygame.font.SysFont(
            self._font_style, self._font_size
        )

        # Rendu du texte
        self._rendered_text: pygame.Surface = pygame.Surface((0, 0))
        self._pre_render_text()
    
    def change_text(self, text: str) -> None:
        """
        Changer le contenu du texte.
        :param text: Le nouveau texte.
        """
        self._text = text
        self._pre_render_text()
    
    def change_font(
            self,
            font_size: int,
            font_style: str | None = None
        ) -> None:
        """
        Changer la police d'écriture du texte.
        :param font_size: La taille de la police.
        :param font_style: Le style de la police.
        """
        self._font_size = font_size

        # Changer le style si spécifié
        if font_style is not None:
            self._font_style = font_style
        
        self._font: pygame.font.Font = pygame.font.SysFont(
            self._font_style, self._font_size
        )

        self._pre_render_text()
        

    def _pre_render_text(self) -> None:
        """Faire le rendu du texte pour quand il doit être affiché."""
        # Faire le rendu du texte
        self._rendered_text = self._font.render(
            self._text, True, self.font_color
        )

        # Calculer la taille du texte
        self.size = Vec2(
            self._rendered_text.get_width(),
            self._rendered_text.get_height()
        )
    
    def render(self, target: pygame.Surface) -> None:
        # Récupérer la position du texte
        global_position = self.global_position(Anchor.NW)

        # Dessiner le fond du texte
        if self.background_color is not None:
            rectangle = pygame.Rect(global_position, self.size)
            pygame.draw.rect(target, self.background_color, rectangle)

        # Afficher le texte
        target.blit(self._rendered_text, global_position.xy)