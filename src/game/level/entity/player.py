import pyray as pr

from ....utils import Vec2
from ...assets import MARIA_FRAMES, MARIA_SPRITE_SHEET
from ...managers import Time
from ..camera import Camera
from ..collider import RectCollider
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
            position=Vec2.null
        )
        self.velocity: Vec2 = Vec2.null
        self.texture: pr.Texture = pr.load_texture(MARIA_SPRITE_SHEET)
    
    @property
    def rect_collider(self) -> RectCollider:
        # Rectangle de collision quand Maria est petite
        return RectCollider(
            self.position + Vec2(0, 0.5),
            Vec2(1, 1)
        )

    def fixed_update(self) -> None:
        # Ajouter la vélocité à la position en la multipliant par le temps
        # écoulé entre les itérations
        self.velocity.x *= 0.9
        self.velocity += Vec2(0, 15) * Time.fixed_delta_time
        self.position += self.velocity * Time.fixed_delta_time

    def update(self) -> None:
        if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
            self.velocity.x = 4
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
            self.velocity.x = -4
        
        if pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
            self.velocity.y = -10
    
    def draw(self, camera: Camera) -> None:
        # Dessiner l'image du joueur
        camera.draw_texture_part(
            self.texture,
            self.position,
            MARIA_FRAMES[0]
        )