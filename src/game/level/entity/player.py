import pyray as pr

from src.utils import Vec2

from ....constants import EPSILON
from ....utils import Vec2
from ...assets import MARIA_FRAMES, MARIA_SPRITE_SHEET
from ...managers import Time
from ..camera import Camera
from .entity import Entity


# XXX: Voici un example pour la classe du joueur, pour que tu puisse voir
# comment utiliser Time et Input, hériter de Entity et utiliser Camera


class Player(Entity):
    """Exemple d'une implémentation du Joueur."""

    class Inputs:
        """Les entrés du joueur."""

        def __init__(self) -> None:
            self.pressing_left: bool = False
            self.pressing_right: bool = False
            self.pressing_jump: bool = False
            # self.pressing_down: bool = False
            # self.pressing_fire: bool = False

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

        self.can_jump: bool = False
    
    def on_collision(self, resolve_vec: Vec2):
        self.position += resolve_vec
        
        self.can_jump = resolve_vec.y < EPSILON and self.velocity.y > 0

        if abs(resolve_vec.x) > EPSILON:
            self.velocity.x = 0
        if abs(resolve_vec.y) > EPSILON:
            self.velocity.y = 0

    def fixed_update(self) -> None:
        # Ajouter la vélocité à la position en la multipliant par le temps
        # écoulé entre les itérations
        self.velocity.x *= 0.9
        self.velocity += Vec2(0, 15) * Time.fixed_delta_time
        self.position += self.velocity * Time.fixed_delta_time

        self.can_jump = False

    def update(self, inputs: Inputs) -> None:
        x_mov = 0.0
        if inputs.pressing_right:
            x_mov += 5
        if inputs.pressing_left:
            x_mov -= 5
        self.velocity.x = x_mov
        
        if inputs.pressing_jump and self.can_jump:
            self.velocity.y = -12
    
    def draw(self, camera: Camera) -> None:
        # Dessiner l'image du joueur
        camera.draw_texture_part(
            self.texture,
            self.position,
            MARIA_FRAMES[0]
        )