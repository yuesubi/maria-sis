import pyray as pr
from typing import Callable, Union

from .....utils import Vec2
from ..anchor import Anchor
from ..fit import Fit
from ..frames import Frame
from ..texts import Text

from .button import Button


class TextButton(Frame):
    """Bouton avec du texte pour l'IHM."""
    
    def __init__(
            self,
            position: Vec2,
            anchor: Anchor,
            size: Vec2,
            fit: Fit,
            text: str,
            font_color: pr.Color,
            font_size: int,
            font_style: str = str(),
            background_color: Union[pr.Color, None] = None,
            border_color: Union[pr.Color, None] = None,
            border_width: int = 1,
            command: Union[Callable[[], None], None] = None
        ) -> None:
        """
        Constructeur d'un bouton.
        :param position: La position du bouton.
        :param anchor: L'origine du bouton.
        :param size: La taille du bouton.
        :param fit: L'adaptation au parent.
        :param text: Le texte de l'élément.
        :param font_color: La couleur du texte.
        :param font_size: La taille du texte.
        :param font_style: La police du texte. (optionnel)
        :param background_color: La couleur de fond du bouton, si la couleur
            est None, le fond est transparent. (optionnel)
        :param border_color: La couleur du bord du bouton, si la couleur est
            None, le bord est transparent. (optionnel)
        :param border_width: L'épaisseur du bord du bouton. (optionnel)
        :param command: Une fonction à appeler lorsque le bouton est cliqué.
            (optionnel)
        """
        
        # Initialisation de la classe parent
        super().__init__(
            position, anchor,
            size, fit,
            children=[
                Button(
                    Vec2(0, 0), Anchor.NW,
                    Vec2(1, 1), Fit.BOTH,
                    background_color,
                    border_color, border_width,
                    command
                ),
                Text(
                    Vec2(0, 0), Anchor.C,
                    text,
                    font_color, font_size, font_style
                )
            ]
        )