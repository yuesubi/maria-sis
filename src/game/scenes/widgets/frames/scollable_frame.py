import pygame
from typing import Union

from ...event_manager import EventManager
from ..anchor import Anchor
from ..fit import Fit
from ..widget import Widget

from .frame import Frame


class ScrollableFrame(Widget):
    """
    Cadre avec une barre de défilement pour l'IHM, peut contenir des sous
    éléments.
    """

    def __init__(
            self,
            position: Vec2,
            anchor: Anchor,
            size: Vec2,
            inner_size: Vec2,
            fit: Fit = Fit.NONE,
            scrollbar_color: Union[pygame.Color, None] = None,
            scrollbar_width: int = 4,
            background_color: Union[pygame.Color, None] = None,
            border_color: Union[pygame.Color, None] = None,
            border_width: int = 1,
            children: list[Widget] = list()
        ) -> None:
        """
        Constructeur d'un cadre.
        :param position: La position du cadre.
        :param anchor: L'origine du cadre.
        :param size: La taille du cadre.
        :param inner_size: La taille du intérieur cadre.
        :param fit: L'adaptation au parent. (optionnel)
        :param scrollbar_color: La couleur de la barre de défilement, si la
            couleur est None, la barre de défilement est transparente.
            (optionnel)
        :param scrollbar_width: L'épaisseur de la barre de défilement.
        :param background_color: La couleur de fond du cadre, si la couleur
            est None, le fond est transparent. (optionnel)
        :param border_color: La couleur du bord du cadre, si la couleur est
            None, le bord est transparent. (optionnel)
        :param border_width: L'épaisseur du bord du cadre. (optionnel)
        :param children: Une liste l'éléments de l'IHM enfants. (optionnel)
        """

        # Initialisation de la classe parent
        super().__init__(
            position, anchor,
            size, fit
        )
        
        self._sub_frame = Frame(
            Vec2(0, 0), Anchor.NW,
            inner_size, Fit.NONE,
            background_color=None,
            border_color=None,  border_width=0,
            children=children,
        )
        self._sub_frame.parent = self

        self.background_color: Union[pygame.Color, None] = background_color
        self.border_color: Union[pygame.Color, None] = border_color
        self.border_width: int = border_width

        self.scrollbar_color: Union[pygame.Color, None] = scrollbar_color
        self.scrollbar_width: int = scrollbar_width
        
        # Variables contenant qui disent si les barres de défilement sont
        # sélectionnés
        self._x_scrollbar_held: bool = False
        self._y_scrollbar_held: bool = False
    
    def add_child(self, child: Widget) -> None:
        """
        Ajouter un enfant.
        :param child: L'enfant à ajouter.
        """
        self._sub_frame.add_child(child)
    
    def process_events(self, event_manager: EventManager) -> None:
        # Appeler la fonction sur tout les enfants
        self._sub_frame.process_events(event_manager)
        
        # Barres de défilement
        x_bar_rect = self.get_x_bar_rectangle()
        y_bar_rect = self.get_y_bar_rectangle()
        
        # Défiler si nécessaire
        if self._x_scrollbar_held:
            pixel_to_pos_ratio = (self._sub_frame.size.x - self.size.x) / (self.size.x - x_bar_rect.width - 2.0 * self.border_width - self.scrollbar_width)
            self._sub_frame.position.x -= event_manager.delta_mouse_pos.x * pixel_to_pos_ratio
        if self._y_scrollbar_held:
            pixel_to_pos_ratio = (self._sub_frame.size.y - self.size.y) / (self.size.y - y_bar_rect.height - 2.0 * self.border_width)
            self._sub_frame.position.y -= event_manager.delta_mouse_pos.y * pixel_to_pos_ratio
        
        # Commencer le défilement si la barre est appuyée 
        if event_manager.is_button_pressed(1):
            if x_bar_rect.collidepoint(event_manager.mouse_pos):
                self._x_scrollbar_held = True
            if y_bar_rect.collidepoint(event_manager.mouse_pos):
                self._y_scrollbar_held = True
        
        # Stopper le défilement si le bouton est relâché
        if not event_manager.is_button_down(1):
            self._x_scrollbar_held = False
            self._y_scrollbar_held = False
    
    def update(self, delta_time: float) -> None:
        self._sub_frame.update(delta_time)
        
        # Garder le sous cadre dans la zone possible
        
        # Position minimum en X
        frame_min_x = -self._sub_frame.size.x + self.size.x
        frame_min_x = min(frame_min_x, 0.0)
        
        # Correction de la position
        self._sub_frame.position.x = min(0.0, self._sub_frame.position.x)
        self._sub_frame.position.x = max(frame_min_x, self._sub_frame.position.x)
        
        # Position minimum en Y
        frame_min_y = -self._sub_frame.size.y + self.size.y
        frame_min_y = min(frame_min_y, 0.0)
        
        # Correction de la position
        self._sub_frame.position.y = min(0.0, self._sub_frame.position.y)
        self._sub_frame.position.y = max(frame_min_y, self._sub_frame.position.y)
    
    def render(self, target: pygame.Surface) -> None:
        # Le rectangle du cadre
        rectangle = pygame.Rect(
            self.global_position(Anchor.NW),
            self.size
        )

        # Dessiner le fond du cadre
        if self.background_color is not None:
            pygame.draw.rect(target, self.background_color, rectangle)
        
        # Restreindre la zone de dessin
        sub_frame_rectangle = rectangle.copy()
        sub_frame_rectangle.size = self._sub_frame.size.xy
        target.set_clip(sub_frame_rectangle)
        
        # Dessiner le sous cadre
        self._sub_frame.render(target)
        
        # Enlever la restriction de la zone de dessin
        target.set_clip(None)
        
        if self.scrollbar_color is not None:
            # Afficher la barre x à l'écran
            x_bar_rect = self.get_x_bar_rectangle()
            pygame.draw.rect(target, self.scrollbar_color, x_bar_rect)
            
            # Afficher la barre y à l'écran
            y_bar_rect = self.get_y_bar_rectangle()
            pygame.draw.rect(target, self.scrollbar_color, y_bar_rect)
        
        # Dessiner la bordure du cadre
        if self.border_color is not None:
            pygame.draw.rect(
                target, self.border_color,
                rectangle, self.border_width
            )
    
    def get_x_bar_rectangle(self) -> pygame.Rect:
        """
        Calculer le rectangle de la barre de défilement x.
        :return: Le rectangle calculé.
        """
        
        # Taille du cadre à l'intérieur de la bordure
        inner_border_width = self.size.x - self.border_width * 2.0 - self.scrollbar_width
        inner_border_width = max(0.0, inner_border_width)
        
        # Position actuelle et maximum du sous cadre
        frame_x = -self._sub_frame.position.x
        frame_x = max(0.0, frame_x)
        frame_max_x = self._sub_frame.size.x - inner_border_width
        frame_max_x = max(0.0, frame_max_x)
        
        # Position et taille de 0.0 à 1.0 de la barre de défilement
        bar_relative_width = inner_border_width / self._sub_frame.size.x
        bar_relative_width = min(1.0, bar_relative_width)
        #bar_relative_x = 1.0
        #if frame_max_x - 0.0 > 0.0:
        bar_relative_x = frame_x / (frame_max_x - 0.0)
        
        # Coin haut droit du cadre
        bottom_left_corner = self.global_position(Anchor.SW)
        
        # Position minimum et maximum de la barre
        bar_min_x = bottom_left_corner.x + self.border_width
        bar_max_x = bottom_left_corner.x + self.size.x  # - self.border_width
        
        # Taille de la barre de défilement
        bar_width = (bar_max_x - bar_min_x) * bar_relative_width
        
        # Réduction de la position maximum de la barre
        bar_max_x -= bar_width
        
        # Position de la barre
        bar_x = bar_min_x + (bar_max_x - bar_min_x) * bar_relative_x
        
        # Déterminer le rectangle de la barre
        bar_rect = pygame.Rect(
            bar_x,
            bottom_left_corner.y - self.scrollbar_width - self.border_width,
            bar_width,
            self.scrollbar_width
        )
        
        return bar_rect
    
    def get_y_bar_rectangle(self) -> pygame.Rect:
        """
        Calculer le rectangle de la barre de défilement y.
        :return: Le rectangle calculé.
        """
        
        # Taille du cadre à l'intérieur de la bordure
        inner_border_height = self.size.y - self.border_width * 2.0
        inner_border_height = max(0.0, inner_border_height)
        
        # Position actuelle et maximum du sous cadre
        frame_y = -self._sub_frame.position.y
        frame_y = max(0.0, frame_y)
        frame_max_y = self._sub_frame.size.y - inner_border_height
        frame_max_y = max(0.0, frame_max_y)
        
        # Position et taille de 0.0 à 1.0 de la barre de défilement
        bar_relative_height = inner_border_height / self._sub_frame.size.y
        bar_relative_height = min(1.0, bar_relative_height)
        # bar_relative_y = 1.0
        # if frame_max_y - 0.0 > 0.0:
        bar_relative_y = frame_y / (frame_max_y - 0.0)
        
        # Coin haut droit du cadre
        top_right_corner = self.global_position(Anchor.NE)
        
        # Position minimum et maximum de la barre
        bar_min_y = top_right_corner.y + self.border_width
        bar_max_y = top_right_corner.y + self.size.y  # - self.border_width
        
        # Taille de la barre de défilement
        bar_height = (bar_max_y - bar_min_y) * bar_relative_height
        
        # Réduction de la position maximum de la barre
        bar_max_y -= bar_height
        
        # Position de la barre
        bar_y = bar_min_y + (bar_max_y - bar_min_y) * bar_relative_y
        
        # Déterminer le rectangle de la barre
        bar_rect = pygame.Rect(
            top_right_corner.x - self.scrollbar_width - self.border_width,
            bar_y,
            self.scrollbar_width,
            bar_height
        )
        
        return bar_rect
