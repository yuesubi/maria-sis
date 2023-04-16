import pygame
from typing import Union

from ...event_manager import EventManager
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
            background_color: Union[pygame.Color, None] = None,
            border_color: Union[pygame.Color, None] = None,
            border_width: int = 1,
            command: Union[callable, None] = None
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

        self.background_color: Union[pygame.Color, None] = background_color
        self.border_color: Union[pygame.Color, None] = border_color
        self.border_width: int = border_width
        
        self.command: Union[callable, None] = command
        self._rectangle: pygame.Rect = pygame.Rect(0, 0, 1, 1)

    def process_events(self, event_manager: EventManager) -> None:
        # Vérifier si le bouton est cliqué
        if event_manager.is_button_released(1):
            # Vérifier si la sourie est sur le bouton
            if self._rectangle.collidepoint(event_manager.mouse_pos):
                # Si il y a une fonction, l'appeler
                if self.command is not None:
                    self.command()
        
    def update(self, delta_time: float) -> None:
        # Mettre à jour le rectangle du bouton
        self._rectangle = pygame.Rect(
            self.global_position(Anchor.NW),
            self.size
        )
    
    def render(self, target: pygame.Surface) -> None:
        # Dessiner le fond du bouton
        if self.background_color is not None:
            pygame.draw.rect(target, self.background_color, self._rectangle)
        
        # Dessiner la bordure du bouton
        if self.border_color is not None:
            pygame.draw.rect(
                target, self.border_color,
                self._rectangle, self.border_width
            )
