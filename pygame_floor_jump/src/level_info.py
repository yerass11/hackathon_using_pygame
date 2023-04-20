"""This module implements the information display for the current level"""
# Этот код определяет класс под названием LevelInfo, 
# который служит контейнером для спрайтов, 
# отображающих информацию о текущем уровне на экране.

# Класс импортирует два пользовательских класса спрайтов, 
# называемых DigitSprite и LevelSprite, из двух разных модулей.

# В методе __init__() класс создает три объекта sprite: 
#     LevelSprite для отображения текста "УРОВЕНЬ" и 
#     два объекта DigitSprite для отображения номера уровня. 
#     Объекты DigitSprite используются для отображения десятков и
#     единиц цифр номера уровня соответственно.

# Начальные позиции объектов DigitSprite устанавливаются с помощью метода set_start_position(),
# который задает начальное положение, скорость и направление движения спрайтов.

# Метод update() вызывается для обновления позиций всех спрайтов в контейнере.

# Метод reset() используется для сброса позиций всех спрайтов в контейнере на их исходные позиции.

# Метод increase_level() используется для увеличения номера уровня на единицу, 
# что делается путем увеличения сначала цифры единицы, 
# а затем, при необходимости, десятичной цифры.

# Наконец, метод draw() используется для рисования всех спрайтов 
# в контейнере в их текущем положении на экране.

from src.digit_sprite import DigitSprite
from src.level_sprite import LevelSprite

class LevelInfo():
    """Container for the sprites that fly in for the current level display"""

    def __init__(self, settings, screen):
        """Init both the level text sprite and digits for the level number"""
        self.settings = settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # LEVEL text
        self.level_sprite = LevelSprite(self.settings, self.screen)
        # 10s digit
        self.digit_tens = DigitSprite(self.settings, self.screen, self.settings.image_res.digit_images, 0)
        self.digit_tens.set_start_position(self.screen_rect.top - 64, self.screen_rect.left + self.settings.tile_width, 0, 15, 22)
        # 1s digit
        self.digit_ones = DigitSprite(self.settings, self.screen, self.settings.image_res.digit_images, 1)
        self.digit_ones.set_start_position(self.screen_rect.top + self.screen_rect.height/2 - 35, self.screen_rect.right, -37, 0, 20)

    def update(self):
        """Update all owned sprites"""
        self.level_sprite.update()
        self.digit_ones.update()
        self.digit_tens.update()

    def reset(self):
        """Reset all owned sprites"""
        self.level_sprite.reset_position()
        self.digit_ones.reset_position()
        self.digit_tens.reset_position()

    def increase_level(self):
        """Raise the level by one and update the sprites as needed"""
        # We only have 2 digits, so this will wrap if the player can get to level 100
        # But that seems unlikely with the current logic and increases
        if self.digit_ones.increase():
            self.digit_tens.increase()

        self.reset()

    def draw(self):
        """Draw all owned sprites at their current positions"""
        self.level_sprite.draw()
        self.digit_ones.draw()
        self.digit_tens.draw()