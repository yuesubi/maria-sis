import pyray as pr
from typing import Union

from .....utils import Vec2
from ....managers import Time
from ..anchor import Anchor
from ..buttons import Button
from ..fit import Fit
from ..frames import Frame
from ..texts import Text
from ..widget import Widget


class TextEntry(Frame):
    """Champ de texte pour l'IHM."""
    
    def __init__(
            self,
            position: Vec2,
            anchor: Anchor,
            size: Vec2,
            fit: Fit,
            font_color: pr.Color,
            font_size: int,
            font_style: str = str(),
            background_color: Union[pr.Color, None] = None,
            border_color: Union[pr.Color, None] = None,
            border_width: int = 1,
        ) -> None:
        """
        Constructeur d'un champ.
        :param position: La position du champ.
        :param anchor: L'origine du champ.
        :param size: La taille du champ.
        :param fit: L'adaptation au parent.
        :param font_color: La couleur du texte.
        :param font_size: La taille du texte.
        :param font_style: La police du texte. (optionnel)
        :param background_color: La couleur de fond du champ, si la couleur
            est None, le fond est transparent. (optionnel)
        :param border_color: La couleur du bord du champ, si la couleur est
            None, le bord est transparent. (optionnel)
        :param border_width: L'épaisseur du bord du champ. (optionnel)
        """

        # Texte qui contient ce qui à été écrit
        self._text = Text(
            Vec2(0, 0), Anchor.C,
            str(),
            font_color, font_size, font_style
        )
        
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
                    command=self.focus
                ),
                self._text
            ]
        )

        # Variable qui contrôle si l'utilisateur est en train d'utiliser le
        # champ
        self._is_focused: bool = False

        # Variables pour le curseur qui clignote
        self._caret_time: float = 0.0
    
    def focus(self) -> None:
        """Faire en sorte que l'on puisse tapper du texte."""
        self._is_focused = True
    
    @property
    def text(self) -> str:
        """
        Récupérer le texte du champ de texte.
        :return: Le texte.
        """
        return self._text.text
    
    @text.setter
    def text(self, new_text) -> None:
        """
        Changer le texte du champ de texte.
        :param new_text: Le nouveau texte.
        """
        self._text.text = new_text
    
    def update(self) -> None:
        super().update()

        # Si un click gauche est détecté
        if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
            # Calculer la position locale de la sourie
            local_mouse_pos = Vec2(pr.get_mouse_x(), pr.get_mouse_y()) - \
                self.global_position(Anchor.NW)

            # Donner le focus si le click est sur le champ, sinon l'enlever
            self._is_focused = (0 <= local_mouse_pos.x < self.size.x and
                0 <= local_mouse_pos.y < self.size.y)

        # Détecter les touches appuyées
        character_typed = chr(pr.get_char_pressed())
        if character_typed and self._is_focused:
            self._text.text += character_typed
        
        # Détecter si il faut supprimer des caractères
        if pr.is_key_pressed(pr.KeyboardKey.KEY_BACKSPACE) and \
                len(self._text.text) > 0:
            self._text.text = self._text.text[:-1]

        # Faire avancer le temps
        self._caret_time += Time.delta_time
    
    def render(self) -> None:
        super().render()

        global_pos = self._text.global_position(Anchor.NE)
        if int(self._caret_time * 2) % 2 == 0 and self._is_focused:
            pr.draw_rectangle(
                global_pos.x, global_pos.y,
                2, self._text.size.y,
                self._text.font_color
            )