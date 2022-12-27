from typing import List, Any

import pygame
from pygame.sprite import Sprite

from config import SCORE_TEXT_SCALE


class Digit(Sprite):
    """
    Classe que representa o sprite de um dígito.

    Atributos
    ---------
        DIGIT_WIDTH: float
            largura do dígito na tela
        DIGIT_HEIGHT: float
            altura do dígito na tela

        image: pygame.Surface
            objeto do pygame que representa a imagem do dígito
        rect: pygame.Rect
            objeto do pygame que armazena as cordenadas retangulares do dígito

    Métodos
    -------
        set_position(xpos: int, ypos: int) -> None:
            atualiza a posição do dígito na tela
    """

    DIGIT_WIDTH: float = 24 * SCORE_TEXT_SCALE
    DIGIT_HEIGHT: float = 36 * SCORE_TEXT_SCALE

    def __init__(self, value: str):
        """
        Método de inicialização da classe Digit, gerenciando os sprites de Dígitos.

        Parâmetro
        ---------
            value: str
                string representando o dígito que será carregado na tela.
        """

        Sprite.__init__(self)

        self.image = pygame.image.load(f"assets/{value}.png")
        self.image = pygame.transform.scale(
            self.image, (self.DIGIT_WIDTH, self.DIGIT_HEIGHT)
        )

        self.rect = self.image.get_rect()

    def set_position(self, xpos: int, ypos: int) -> None:
        """
        Método para atualizar a posição do dígito na tela.

        Parâmetros
        ----------
            xpos: int
                coordenada x do dígito
            ypos: int
                coordenada y do dígito
        """

        self.rect[0] = xpos
        self.rect[1] = ypos


class Score:
    """
    Classe que representa o sprite de um dígito.

    Atributos
    ---------
        DIGITS_GAP: int
            espaçamento entre os digitos na tela

    Métodos
    -------
        update_score(value: int) -> None:
            atualiza o score que aparece na tela
        update(*args: Any, **kwargs: Any) -> None:
            função adicionada para manter a concistência com os grupos
        draw(surface: pygame.Surface) -> List[pygame.Rect]
            função adicionada para manter a concistência com os grupos
    """

    DIGITS_GAP: int = 5

    def __init__(self, score_value: int, xpos: int, ypos: int) -> None:
        """
        Método de inicialização da classe Score.

        Parâmetros
        ----------
            score_value: int
                valor de inicio do score
            xpos: int
                coordenada x do centro do score na tela
            ypos: int
                coordenada y do centro do score na tela
        """

        self.__xpos = xpos
        self.__ypos = ypos

        self.update_score(score_value)

    def __set_digits_position(self, xpos: int, ypos: int) -> None:
        """
        Método resṕonsável por calcular o posicionamento do score levando
        em consideração a quantidade de dígitos e o gap entre eles.

        Parâmetros
        ----------
            xpos: int
                coordenada x do centro do score na tela
            ypos: int
                coordenada y do centro do score na tela
        """

        reference = self.__digits_group.sprites()[0]

        total_digits = len(self.__digits)
        start_position = xpos - (
            (total_digits * reference.rect[2] + (total_digits - 1) * self.DIGITS_GAP) / 2
        )

        # Define a posição de cada um dos dígtos na tela
        for i, sprite in enumerate(self.__digits_group.sprites()):
            sprite.set_position(
                start_position + i * (sprite.rect[2] + self.DIGITS_GAP),
                ypos
            )

    def update_score(self, value: int) -> None:
        """
        Método responsável por atualizar o valor do score.

        Parâmetros
        ----------
            value: int
                novo valor para o score
        """

        self.__digits = list(str(value))
        self.__digits_group = pygame.sprite.Group()

        # Instancia cada um dos dígitos que serão colocados na tela
        for value in self.__digits:
            self.__digits_group.add(
                Digit(value)
            )

        # Posiciona dígito a dígito na tela
        self.__set_digits_position(self.__xpos, self.__ypos)

    def update(self, *args: Any, **kwargs: Any) -> None:
        """
        Método para garantir que a interface do grupo seja mantida com o método
        update.
        """

        self.__digits_group.update(*args, **kwargs)

    def draw(self, surface: pygame.Surface) -> List[pygame.Rect]:
        """
        Método para garantir que a interface do grupo seja mantida com o método
        update.
        """

        return self.__digits_group.draw(surface)
