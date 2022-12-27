from pygame.sprite import Sprite


def is_horizontal_off_screen(sprite: Sprite) -> bool:
    """
    Função responsável por verificar se o sprite saiu da tela pelo lado
    esquerdo.

    Parâmetros
    ----------
        sprite: Sprite
            sprite que será verificado
    """

    return (sprite.rect[0] + sprite.rect[2]) <= 0
