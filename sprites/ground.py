import pygame
from pygame.sprite import Sprite

from sprites.utils import is_horizontal_off_screen
from config import (
    GAME_SPEED,
    SCREEN_HEIGHT,
    GROUND_WIDTH,
    GROUND_HEIGHT,
    SCREEN_WIDTH,
)


class Ground(Sprite):
    """
    Classe que representa o sprite do chão, lidando com o movimento.

    Atributos
    ---------
        image: pygame.Surface
            objeto do pygame que representa a imagem do chão
        mask: pygame.mask.Mask
            objeto do pygame que representa a máscaras de bits 2D do chão
        rect: pygame.Rect
            objeto do pygame que armazena as cordenadas retangulares do chão

    Métodos
    -------
        update() -> None:
            controlar como vai ocorrer a atualização do chão
    """

    def __init__(self, xpos: int) -> None:
        """
        Método de inicialização da classe Ground, gerenciando os sprites
        do chão.

        Parâmetros
        ----------
            xpos: int
                posição em x onde o chão deve ser colocado inicialmente
        """

        Sprite.__init__(self)

        self.image = pygame.image.load("assets/base.png")
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        # posiciona o chão corretamente na tela
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self) -> None:
        """
        Método para controlar como vai ocorrer a atualização do chão,
        incluindo deslocamento lateral e sensação de continuidade.
        """

        if is_horizontal_off_screen(self):
            self.rect[0] = SCREEN_WIDTH

        self.rect[0] -= GAME_SPEED

