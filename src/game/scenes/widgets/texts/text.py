import pyray as pr
from typing import Union

from .....utils import Vec2
from ..anchor import Anchor
from ..fit import Fit
from ..widget import Widget


class Text(Widget):
    """Élément de texte de l'IHM."""

    def __init__(
            self,
            position: Vec2,
            anchor: Anchor,
            text: str,
            font_color: pr.Color,
            font_size: int,
            font_style: str = str(),
            background_color: Union[pr.Color, None] = None
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

        self.font_color: pr.Color = font_color
        self.background_color: pr.Color | None = background_color

        self.text: str = str(text)

        self.font_size: int = int(font_size)
        self.font_style: str = str(font_style)

    def update(self) -> None:
        # Calculer la taille du texte
        self.size = Vec2(
            pr.measure_text(self.text, self.font_size),
            self.font_size
        )
    
    def render(self) -> None:
        # Récupérer la position du texte
        global_position = self.global_position(Anchor.NW)

        # Dessiner le fond du texte
        if self.background_color is not None:
            pr.draw_rectangle(
                global_position.x, global_position.y,
                self.size.x, self.size.y,
                self.background_color
            )

        # Afficher le texte
        pr.draw_text(
            self.text,
            int(global_position.x), int(global_position.y),
            self.font_size,
            self.font_color
        )