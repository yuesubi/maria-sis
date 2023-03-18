"""Jeu Maria Sis"""

import pygame

from .managers import Input, Time


WIDTH, HEIGHT = 16, 13


class Game:
    """Jeu Maria Sis"""

    def __init__(self) -> None:
        pygame.init()
        
        self.window = pygame.display.set_mode((WIDTH * 16 * 2, HEIGHT * 16 * 2))
        pygame.display.set_caption("Maria Sis")

    def run(self) -> None:
        surf = pygame.Surface((16*16, 13*16))

        pygame.font.init()
        font = pygame.font.SysFont("", 16)

        running = True
        
        while running:
            Input.update()
            if Input.is_quitting == True:
                running = False
            
            surf.fill((0, 0, 0))

            pygame.draw.circle(surf, (255, 0, 0), (8*16, 6.5*16), 64)
            surf.blit(font.render(str(round(Time.fps)), False, (0, 255, 0)), (8, 8))
            
            self.window.blit(pygame.transform.scale(surf, self.window.get_size()), (0, 0))
            pygame.display.flip()
            
            Time.update()