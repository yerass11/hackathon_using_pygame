"""This module implements the platform block object (sprite) for Floor-jumper"""
# Этот код определяет класс Block, 
# который наследуется от класса Sprite модуля pygame.sprite.

# Класс Block имеет метод __init__, 
# который инициализирует свойства класса, 
# включая настройки, экран, изображение, rect, screen_rect и dying. 
# настройки и экран представляют собой настройки игры и поверхность дисплея соответственно. 
# image - это изображение блока, а rect - прямоугольная область блока. 
# screen_rect - это прямоугольная область поверхности дисплея, 
# а dying - логическое значение, указывающее, умирает блок или нет.

# Метод draw является обязательным методом для pygame.sprite.Класс Group, 
# который отвечает за рисование спрайта на экране. 
# Этот метод выводит изображение блока на экран в его текущем положении, 
# которое определяется свойством rect.


import pygame
from pygame.sprite import Sprite

class Block(Sprite):
    """Block object"""

    def __init__(self, settings, screen, image):
        """Initialize the block, not much to do other than save the params"""
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.dying = False

    # 'draw' is required by pygame.Sprite.Group for drawing in batches
    def draw(self):
        """Draws the block at its current position on the screen"""
        self.screen.blit(self.image, self.rect)
        