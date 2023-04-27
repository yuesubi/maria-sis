import pyray as pr
from typing import Callable, Union

from .....utils import Vec2
from ..anchor import Anchor
from ..fit import Fit
from ..widget import Widget


class Button(Widget):
    """Bouton pour l'IHM."""
    
    def __init__(
            self,
            position: Vec2,
            anchor: Anchor,
            size: Vec2,
            fit: Fit = Fit.NONE,
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
        :param fit: L'adaptation au parent. (optionnel)
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
            size, fit
        )

        self.background_color: pr.Color | None = background_color
        self.border_color: pr.Color | None = border_color
        self.border_width: int = border_width
        
        self.command: Callable[[], None] | None = command

    def update(self) -> None:
        # Vérifier si le bouton est cliqué
        if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
            # Vérifier si la sourie est sur le bouton
            global_pos = self.global_position(Anchor.C)
            mouse_pos = Vec2(pr.get_mouse_x(), pr.get_mouse_y())
            if abs(global_pos.x - mouse_pos.x) < self.size.x / 2 and \
                    abs(global_pos.y - mouse_pos.y) < self.size.y / 2:
                # Si il y a une fonction, l'appeler
                if self.command is not None:
                    self.command()
    
    def render(self) -> None:
        global_pos = self.global_position(Anchor.NW)

        # Dessiner le fond du bouton
        if self.background_color is not None:
            pr.draw_rectangle(
                global_pos.x, global_pos.y,
                self.size.x, self.size.y,
                self.background_color
            )
        
        # Dessiner la bordure du bouton
        if self.border_color is not None:
            pr.draw_rectangle(
                global_pos.x, global_pos.y,
                self.size.x, self.size.y,
                self.border_color
            )