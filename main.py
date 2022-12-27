import os
from typing import List, Tuple, Text

import neat

from game import Game
from config import MAX_GENERATIONS


def eval_genomes(genomes: List[Tuple[int, neat.DefaultGenome]],
                 config: neat.Config) -> None:
    """
    Função responsável por executar o jogo e calcular o fitness da
    população.

    Parâmetros
    ----------
        genomes: List[Tuple[int, neat.DefaultGenome]]
            genomas que serão testados na geração corrente
        config: neat.Config
            variável contendo a configuração do algoritimo
    """

    brains = []

    # itera sobre os genomas zerando o fitness e montando a estrutura
    # para o jogo
    for _, genome in genomes:
        genome.fitness = 0

        brains.append({
            "genome": genome,
            "net": neat.nn.FeedForwardNetwork.create(genome, config),
        })

    # Recupera a instância do jogo e executa com as redes neurais
    flappy_bird = Game()

    flappy_bird.reset(brains)
    flappy_bird.loop()


def run(config_file: Text) -> None:
    """
    Função responsável por configurar a execução do NEAT.

    Parâmetros
    ----------
        config_file: Text
            caminho do arquivo de configuração do NEAT
    """

    # Cria as configurações do NEAT
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Gera o relatório do terminal e a população inicial
    stats = neat.StatisticsReporter()
    population = neat.Population(config)

    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(5))
    population.add_reporter(neat.StdOutReporter(True))

    # Executa uma quantidade definida de gerações e recupera o vencedor
    winner = population.run(eval_genomes, MAX_GENERATIONS)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    print('\nBest genome:\n{!s}'.format(winner))

    # Executa o jogo apenas com o vencedor
    flappy_bird = Game()
    flappy_bird.reset([{
        "genome": winner,
        "net": winner_net,
    }])

    flappy_bird.loop()

    input("Game Over...")


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')

    run(config_path)
