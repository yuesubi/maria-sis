import pygame

from ..managers import Time, Scene
from .camera import Camera
from .block import Block, DecorativeBlock
from .entity import Player


class LevelScene(Scene):
    """Scène de niveau."""
    
    def __init__(self) -> None:
        super().__init__()

        self.player: Player = Player()
        self.camera: Camera = Camera()

        self.blocks: list[Block] = [
            DecorativeBlock(pygame.Vector2(0, 1))
        ]
    
    def fixed_update(self) -> None:
        self.player.fixed_update()
        self.camera.position = self.camera.position.lerp(
            self.player.position, Time.fixed_delta_time * 4)

    def update(self) -> None:
        self.player.update()
    
    def render_to(self, target_surf: pygame.Surface) -> None:
        self.camera.begin_render(target_surf)
        for block in self.blocks:
            block.draw(self.camera)
        self.player.draw(self.camera)
        self.camera.end_render()