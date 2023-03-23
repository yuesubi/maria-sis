import pygame

from ....constants import PLAYER_SPEED, UNIT
from ...assets import MARIA_FRAMES
from ...managers import Input, Time
from ..camera import Camera
from .entity import Entity


# XXX: Voici un example pour la classe du joueur, pour que tu puisse voir
# comment utiliser Time et Input, hériter de Entity et utiliser Camera


class Player(Entity):
    """Exemple d'une implémentation du Joueur."""

    def __init__(self) -> None:
        """Constructeur."""
        super().__init__(
            # La position est un vecteur mais en gros c'est un point, il y a
            # juste pas de classe Point dans pygame.
            position=pygame.Vector2(0, 0)
        )
        self.velocity: pygame.Vector2 = pygame.Vector2()

        # Masque pour les collisions
        self._collision_mask: pygame.mask.Mask = pygame.mask.from_surface(
            MARIA_FRAMES[0]
        )

    def fixed_update(self) -> None:
        # Ajouter la vélocité à la position en la multipliant par le temps
        # écoulé entre les itérations
        self.position += self.velocity * PLAYER_SPEED * Time.fixed_delta_time

    def update(self) -> None:
        # Mettre la vélocité au vecteur nul
        self.velocity.update(0, 0)

        # Si une flèche est appuyée modifier la vélocité
        if Input.is_key_down(pygame.K_DOWN):
            self.velocity.y += 1
        if Input.is_key_down(pygame.K_UP):
            self.velocity.y -= 1
        if Input.is_key_down(pygame.K_RIGHT):
            self.velocity.x += 1
        if Input.is_key_down(pygame.K_LEFT):
            self.velocity.x -= 1
        
        # Si la vélocité n'est pas nulle
        if self.velocity.xy != (0, 0):
            # Faire en sorte que le vecteur vélocité est une longueur de 1 (si
            # on ne fait pas ça, se déplacer en diagonale est plus rapide que se
            # déplacer sur les cotés)
            self.velocity.normalize_ip()
    
    def draw(self, camera: Camera) -> None:
        # Dessiner l'image du joueur
        camera.draw_surface(self.position, MARIA_FRAMES[0])
    
    @property
    def collision_mask(self) -> pygame.mask.Mask:
        """
        Assesseur du masque pour les collisions.
        :return: Le masque pour les collisions.
        """
        return self._collision_mask