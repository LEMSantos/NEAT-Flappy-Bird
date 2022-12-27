from typing import Dict, Text, Any
from itertools import cycle

import pygame
from pygame.sprite import Sprite

from config import (
    GRAVITY_CONSTANT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class Bird(Sprite):
    """
    Classe que representa o sprite de um pássaro, lidando com animações e movimento.

    Atributos
    ---------
        image_assets: List[pygame.Surface]
            lista de imagens do pássaro que serão usadas para animação
        image: pygame.Surface
            objeto do pygame que representa a imagem atual do pássaro
        mask: pygame.mask.Mask
            objeto do pygame que representa a máscaras de bits 2D do pássaro
        rect: pygame.Rect
            objeto do pygame que armazena as cordenadas retangulares do pássaro
        animation_loop: Iterator[pygame.Surface]
            iterador com a sequência de imagens para a animação
        velocity: float
            número que indica a velocidade atual do pássaro

    Métodos
    -------
        fly() -> None:
            gera o efeito de voo do pássaro
        update(pipe_center_pos: int) -> None:
            atualiza o estado atual do pássaro em relação a movimento e animação
    """

    image_assets = [
        pygame.image.load("assets/bluebird-midflap.png"),
        pygame.image.load("assets/bluebird-downflap.png"),
        pygame.image.load("assets/bluebird-upflap.png"),
    ]

    def __init__(self, brain: Dict[Text, Any]) -> None:
        """
        Método de inicialização da classe Bird, gerenciando os sprites
        de pássaros.

        Parâmetros
        ----------
            brain: Dict[Text, Any]
                dicionário que contém o genoma e a rede neural gerada
        """

        Sprite.__init__(self)

        self.__brain = brain

        self.image = self.image_assets[-1].convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.__reset_bird_position()

        self.animation_loop = cycle(self.image_assets)
        self.velocity = 0

    def __get_fall_velocity(self) -> float:
        """
        Método utilitário para calcular a velocidade de queda do pássaro ao
        longo da tragetória.

        a -> Velocidade de aceleração
        u -> Velocidade inicial de queda
        """

        a = GRAVITY_CONSTANT
        u = self.velocity

        self.velocity = a + u

        return self.velocity

    def __reset_bird_position(self) -> None:
        """
        Método para colocar o pássaro de volta para a posição inicial
        do jogo.
        """

        x = SCREEN_WIDTH / 3
        y = SCREEN_HEIGHT / 2

        self.rect[0], self.rect[1] = x, y

    def fly(self) -> None:
        """
        Método responsável por gerar o efeito de voo do pássaro
        """

        self.velocity = -15

    def update(self, pipe_center_pos: int) -> None:
        """
        Método para controlar como vai ocorrer a atualização do pássaro,
        incluindo queda, voo e animação de imagens.

        Parâmetros
        ----------
            pipe_center_pos: int
                posição do centro da abertura dos pipes mais próximos. Essa
                veriável é utilizada como uma das entradas para a rede neural.
        """

        # Atualiza a imagem corrente da animação e a movimentação
        self.image = next(self.animation_loop)
        self.rect[1] += self.__get_fall_velocity()

        # Atualiza o fitness do pássaro
        self.__brain["genome"].fitness += 0.1

        bird_center = (self.rect[1] + self.rect[3]) // 2

        # Gera a saída da rede neural
        _input = (bird_center, pipe_center_pos)
        output = self.__brain["net"].activate(_input)

        # Voa se a saida for maior que o threshold
        if output[0] > 0.5:
            self.fly()
