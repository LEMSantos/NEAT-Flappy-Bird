from random import randint
from typing import Tuple

import pygame
from pygame.sprite import Sprite

from config import (
    GAME_SPEED,
    SCREEN_HEIGHT,
    SCREEN_HEIGHT,
    PIPE_HEIGHT,
    PIPE_WIDTH,
    PIPE_GAP,
)

class Pipe(Sprite):
    """
    Classe que representa o sprite do pipe, lidando com o movimento.

    Atributos
    ---------
        image: pygame.Surface
            objeto do pygame que representa a imagem do pipe
        mask: pygame.mask.Mask
            objeto do pygame que representa a máscaras de bits 2D do pipe
        rect: pygame.Rect
            objeto do pygame que armazena as cordenadas retangulares do pipe

    Métodos
    -------
        update() -> None:
            controla como vai ocorrer a atualização do pipe
        get_random_pipes(xpos: int) -> Tuple[Pipe, Pipe]:
            gera pipes com a abertura em um ponto aleatório
    """

    def __init__(self, inverted: bool, xpos: int, ysize: int) -> None:
        """
        Método de inicialização da classe Pipe, gerenciando os sprites de
        Pipes.

        Parâmetros
        ----------
            inverted: bool
                variável que indica se o pipe deve ser invertido
            xpos: int
                posição x inicial do pipe
            ysize: int
                altura total do pipe em pixels
        """

        Sprite.__init__(self)

        self.image = pygame.image.load("assets/pipe-green.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - ysize

        # verifica se é necessário inverter o pipe, então gira a imagem em 180
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)

    def update(self):
        """
        Método para controlar como vai ocorrer a atualização do pipe,
        incluindo deslocamento lateral e sensação de continuidade.
        """

        self.rect[0] -= GAME_SPEED

    @classmethod
    def get_random_pipes(cls, xpos: int) -> Tuple["Pipe", "Pipe"]:
        """
        Método responsável por gerar dois pipes, um normal e outro invertido
        com uma abertura em um ponto aleatório entre eles.

        Parâmetros
        ----------
            xpos: int
                parâmetro que indica a posição inicial em x dos pipes

        Retorno
        -------
            Tupla contendo duas instâncias da classe Pipe
        """

        size = randint(100, 400)

        return (
            cls(False, xpos, size),
            cls(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
        )
