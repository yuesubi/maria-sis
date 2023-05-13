import pyray as pr

from src.utils import Vec2

from ....constants import EPSILON
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
            position=Vec2.null,
            size=Vec2(1, 1)
        )
        self.velocity: Vec2 = Vec2.null
        self.texture: pr.Texture = pr.load_texture(MARIA_SPRITE_SHEET)
    
    def on_collision(self, resolve_vec: Vec2):
        self.position += resolve_vec

        if resolve_vec.x > EPSILON:
            self.velocity.x = 0
        if resolve_vec.y > EPSILON:
            self.velocity.y = 0

    def fixed_update(self) -> None:
        # Ajouter la vélocité à la position en la multipliant par le temps
        # écoulé entre les itérations
        self.velocity.x *= 0.9
        self.velocity += Vec2(0, 15) * Time.fixed_delta_time
        self.position += self.velocity * Time.fixed_delta_time

    def update(self) -> None:
        x_mov = 0.0
        if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
            x_mov += 4
        if pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
            x_mov -= 4
        self.velocity.x = x_mov
        
        if pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
            self.velocity.y = -10
    
    def draw(self, camera: Camera) -> None:
        # Dessiner l'image du joueur
        camera.draw_texture_part(
            self.texture,
            self.position,
            MARIA_FRAMES[0]
        )