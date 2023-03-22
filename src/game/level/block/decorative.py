import pygame

from ...managers import Input, Time
from ..camera import Camera
from .block import Block


# XXX: Voici un example pour un block décoratif, pour que tu puisse voir comment
# hériter de DecorativeBlock et utiliser Camera


class DecorativeBlock(Block):
    """Classe d'un exemple de block décoratif."""

    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__()
        """
        Constructeur.
        :param position: La position du block
        """

        # TODO: Prendre en argument l'image du block et la stocker pour pouvoir
        # la dessiner

        # La position est un vecteur mais en gros c'est un point, il y a juste
        # pas de classe Point dans pygame.
        self.position: pygame.Vector2 = position
    
    def draw(self, camera: Camera) -> None:

        # TODO: Dessiner l'image du block à la place d'un carré

        # Dessiner le carré qui représente le block
        camera.draw_rect(
            pygame.Color(255, 50, 255),
            self.position, size=pygame.Vector2(16, 16),
            width=2
        )