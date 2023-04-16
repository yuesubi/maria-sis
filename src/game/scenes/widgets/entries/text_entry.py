import pygame

from ...event_manager import EventManager

from .....utils import Vec2
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
            font_color: pygame.Color,
            font_size: int,
            font_style: str = str(),
            background_color: pygame.Color | None = None,
            border_color: pygame.Color | None = None,
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
        self.text = Text(
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
                self.text
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
    
    def get_text(self) -> str:
        """
        Récupérer le texte du champ de texte.
        :return: Le texte.
        """
        return self.text._text
    
    def set_text(self, new_text) -> None:
        """
        Changer le texte du champ de texte.
        :param new_text: Le nouveau texte.
        """
        self.text.change_text(new_text)
    
    def process_events(self, event_manager: EventManager) -> None:
        super().process_events(event_manager)

        # Si un click gauche est détecté
        if event_manager.is_button_pressed(pygame.BUTTON_LEFT):
            # Calculer la position locale de la sourie
            local_mouse_pos = (event_manager.mouse_pos -
                self.global_position(Anchor.NW))

            # Donner le focus si le click est sur le champ, sinon l'enlever
            self._is_focused = (0 <= local_mouse_pos.x < self.size.x and
                0 <= local_mouse_pos.y < self.size.y)

        # Détecter les touches appuyées
        character_typed = event_manager.alpha_numeric
        if len(character_typed) > 0 and self._is_focused:
            self.text.change_text(self.text._text + character_typed)
        
        # Détecter si il faut supprimer des caractères
        if (event_manager.is_key_pressed(pygame.K_BACKSPACE) and
            len(self.text._text) > 0):

            self.text.change_text(self.text._text[:-1])
    
    def update(self, delta_time: float) -> None:
        super().update(delta_time)

        # Faire avancer le temps
        self._caret_time += delta_time
    
    def render(self, target: pygame.Surface) -> None:
        super().render(target)

        caret_rect = pygame.Rect(self.text.global_position(Anchor.NE),
            Vec2(2, self.text.size.y))
        if int(self._caret_time * 2) % 2 == 0 and self._is_focused:
            pygame.draw.rect(target, self.text.font_color, caret_rect)