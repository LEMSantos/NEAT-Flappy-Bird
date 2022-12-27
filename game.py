from typing import Dict, List, Text, Any, Tuple

import pygame
from pygame.locals import *

from sprites.utils import is_horizontal_off_screen
from sprites.bird import Bird
from sprites.ground import Ground
from sprites.pipe import Pipe
from sprites.score import Score
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS
)


class SingletonMeta(type):
    """
    A classe Singleton para lidar com a instância única da classe Game.
    O objetivo é que a UI do jogo não seja recriada sempre que uma nova geração
    seja avaliada.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possíveis mudanças no valor dos argumentos passados para o `__init__` não
        afetarão a instância retornada.
        """

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class Game(metaclass=SingletonMeta):
    """
    Classe responsável pode criar toda a interface do jogo, manter o loop de
    execução e atualizar os sprites.

    Atributos
    ---------
        SCREEN_SHAPE : tuple
            dimensões da tela do jogo
        GAME_FRAMERATE : int
            taxa de atualização de quadros
        SCORE : int
            score que será mostrado na tela do jogo
        screen : Surface
            superficie onde o jogo será desenhado
        groups : Dict[Text, Any]
            grupos de sprites utilizadas no jogo

    Métodos
    -------
        reset(brains: List[Dict[Text, Any]]) -> None:
            Volta o jogo ao estado inicial.
        loop() -> None:
            Executa o loop do jogo.
    """

    SCREEN_SHAPE: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
    GAME_FRAMERATE: int = FPS
    SCORE: int = 0

    def __init__(self):
        """
        Método de inicialização da classe Game, iniciando a interface completa.
        A interface não será reconstruida ao longo da execução.
        """

        pygame.init()

        self.screen = pygame.display.set_mode(self.SCREEN_SHAPE)
        self.__background = pygame.transform.scale(
            pygame.image.load("assets/background-day.png"),
            self.SCREEN_SHAPE,
        )

        self.__pipe_gap_centers = []
        self.groups = self.__initialize_groups()

    def __initialize_groups(self, brains: List[Dict[Text, Any]]=[]) -> Dict[Text, Any]:
        """
        Método responsável por criar o conjunto de sprites que serão utilizadas
        ao longo da execução do jogo.

        Parâmetros
        ----------
            brains : list, optional
                conjunto de genomas que serão utilizados na instância

        Retorno
        -------
            Dicionário contendo todos os grupos de sprites utilizados no jogo
        """

        # Inicializa os grupos de sprites
        bird_group = pygame.sprite.Group()
        ground_group = pygame.sprite.Group()
        pipe_group = pygame.sprite.Group()
        score = Score(self.SCORE, SCREEN_WIDTH / 2, 50)

        # Cria os sprites dos pássaros em conjunto com as redes neurais
        for brain in brains:
            bird_group.add(Bird(brain))

        # Adiciona os sprites do solo
        ground_group.add(Ground(0))
        ground_group.add(Ground(SCREEN_WIDTH))

        # Inicia os sprites dos Pipes
        for i in range(2):
            pipes = Pipe.get_random_pipes(SCREEN_WIDTH * i + 800)

            parallel_pipes = pygame.sprite.Group()
            parallel_pipes.add(pipes[0])
            parallel_pipes.add(pipes[1])

            pipe_group.add(parallel_pipes)

            self.__pipe_gap_centers.append(
                (pipes[0].rect[1] + (pipes[1].rect[1] + pipes[1].rect[3])) // 2
            )

        return {
            "birds": bird_group,
            "ground": ground_group,
            "pipes": pipe_group,
            "score": score,
        }

    def __update_sprites(self) -> None:
        """
        Método responsável por atualizar o estado de todos os sprites do
        jogo.
        """

        next_pipe_center_pos = self.__pipe_gap_centers[0]

        # Chama o método de atualização dos grupos
        for key, group in self.groups.items():
            if key == "birds":
                group.update(next_pipe_center_pos)
            else:
                group.update()

            group.draw(self.screen)

    def __handle_events(self) -> None:
        """
        Método para lidar com os eventos emitidos ao longo do jogo
        """

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

    def __replace_pipes(self) -> None:
        """
        Método responsável por substituir um pipe quando ele sai da tela,
        colocando o novo na posição inicial.
        """

        pipe_group = self.groups["pipes"]

        # Remove o Pipe antigo do grupo de pipes
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
        self.__pipe_gap_centers.pop(0)

        # Gera novos pipes com a abertura em um ponto aleatório
        pipes = Pipe.get_random_pipes(SCREEN_WIDTH * 2)

        # Cria um novo subgrupo com os pipes gerados
        parallel_pipes = pygame.sprite.Group()
        parallel_pipes.add(pipes[0])
        parallel_pipes.add(pipes[1])

        pipe_group.add(parallel_pipes)

        # Atualiza a variável que guarda o centro do gap dos pipes
        self.__pipe_gap_centers.append(
            (pipes[0].rect[1] + (pipes[1].rect[1] + pipes[1].rect[3])) // 2
        )

    def __remove_when_collide(self) -> None:
        """
        Método responsável por lidar com as colisões dos pássaros com o
        chão e com os pipes, além de uma eventual saida da tela pela parte
        de cima do cenário.
        """

        bird_group = self.groups["birds"]
        ground_group = self.groups["ground"]
        pipe_group = self.groups["pipes"]

        # Remove os pássaros que colidiram com os pipes ou o chão
        collide = lambda group1, group2: pygame.sprite.groupcollide(
            group1, group2, True, False, pygame.sprite.collide_mask,
        )

        collide(bird_group, ground_group)
        collide(bird_group, pipe_group)

        # Remove os pássaros que sairam da tela pela parte de cima
        for bird in bird_group.sprites():
            if bird.rect[1] < 0 or bird.rect[1] > SCREEN_HEIGHT:
                bird.kill()

    def reset(self, brains: List[Dict[Text, Any]]) -> None:
        """
        Método responsável por voltar o jogo ao estado inicial.

        Parâmetros
        ----------
            brains : list
                conjunto de genomas que serão utilizados na instância
        """

        self.SCORE = 0
        self.__pipe_gap_centers = []
        self.groups = self.__initialize_groups(brains)

    def loop(self) -> None:
        """
        Método responsável por controlar o loop principal do jogo
        """

        # Define o clock do jogo
        clock = pygame.time.Clock()

        while True:
            clock.tick(self.GAME_FRAMERATE)
            self.groups["score"].update_score(self.SCORE)

            # Verifica os eventos emitidos durante o jogo
            self.__handle_events()

            self.screen.blit(self.__background, (0, 0))

            # Verifica se o pipe saiu da tela pela esquerda
            if is_horizontal_off_screen(self.groups["pipes"].sprites()[0]):
                self.SCORE += 1
                self.__replace_pipes()

            # Atualiza todos os sprites do jogo
            self.__update_sprites()

            pygame.display.update()

            # Remove os pássaros que colidiram ou sairam da tela
            self.__remove_when_collide()

            # Finaliza o loop quando não restar nenhum pássaro
            bird_group = self.groups["birds"]

            if len(bird_group.sprites()) == 0:
                break
