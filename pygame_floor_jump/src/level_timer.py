"""This module implements the timer for a level.  The time used to complete will be factored into the final scoring logic"""
# Этот код определяет класс под названием LevelTimer, 
# который представляет цифровой таймер в стиле жидкокристаллического дисплея. 
# Он состоит из изображения в рамке и нескольких цифровых изображений 
# (также определенных в другом модуле).

# Метод __init__() инициализирует состояние таймера, 
# создает группу для цифр и создает шесть объектов 
# DigitSprite для представления цифр минут (M), секунд (S) и сотых долей секунды (h). 
# Каждая цифра расположена относительно рамки.

# Метод reset() сбрасывает таймер на ноль, а метод stop() останавливает таймер.

# Метод position_frame() перемещает базовый фрейм в заданное местоположение,
# а position_digits() перемещает каждый цифровой спрайт на основе положения фрейма.

# Метод set_digit_places() отделяет десятки и единицы от каждой временной пары, 
# а set_time() устанавливает правильные цифры на основе введенного времени в минутах, 
# секундах и сотых долях секунды.

# Метод update() обновляет часы, вычисляя прошедшее время в минутах, 
# секундах и сотых долях секунды, обновляя значения DigitSprites правильным временем и 
# обеспечивая правильное расположение цифр.

# Метод draw() рисует визуальное представление часов путем размытия изображения рамки и 
# рисования цифр на экране.

# В целом, этот код предоставляет базовую структуру для цифрового таймера с возможностью запуска, 
# остановки и сброса таймера, а также отображения прошедшего времени.




from src.digit_sprite import DigitSprite
from pygame.sprite import Group
import pygame

class LevelTimer():
    """The LevelTimer class represents a digital LCD style timer composed of a frame image and several DigitSprites"""

    def __init__(self, settings, screen):
        """Initialize the level timer state"""
        self.settings = settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.frame_image = self.settings.image_res.lcd_frame_image
        self.rect = self.frame_image.get_rect()
        self.digits = Group()
        self.running = True
        self.elapsed_time_ms = 0
        self.last_rect = self.rect
        
        # Create the digits MM:SS:hh
        self.digit_M1 = self.create_and_add_digit(self.digits)
        self.digit_M2 = self.create_and_add_digit(self.digits)
        self.digit_S1 = self.create_and_add_digit(self.digits)
        self.digit_S2 = self.create_and_add_digit(self.digits)
        self.digit_h1 = self.create_and_add_digit(self.digits)
        self.digit_h2 = self.create_and_add_digit(self.digits)

        # Each digit is positioned relative to the frame
        self.position_digits()

    def reset(self):
        """Resets the counter to 0"""
        self.elapsed_time_ms = 0
        self.clock = pygame.time.Clock()
        self.running = True
        
    def stop(self):
        """Stop the timer"""
        self.running = False

    def create_and_add_digit(self, digit_group):
        """Make a new digit and add it to the group"""
        digit_object = DigitSprite(self.settings, self.screen, self.settings.image_res.lcd_digit_images, 0)
        digit_group.add(digit_object)
        return digit_object

    def position_frame(self, top, left):
        """Move the base frame to a given location"""
        self.rect.top = top
        self.rect.left = left
        self.position_digits()

    def position_digit_pair(self, digit_left, digit_right, x_offset, y_offset):
        """Position a pair of digits, e.g. MM or SS relative to a given offset from the frame"""
        digit_width = digit_left.rect.width
        # Left
        digit_left.set_start_position(y_offset, x_offset, 0, 0, 0)
        x_offset += self.settings.lcd_frame_digit_padding_horz_minor + digit_width
        # Right
        digit_right.set_start_position(y_offset, x_offset, 0, 0, 0)
        x_offset += self.settings.lcd_frame_digit_padding_horz_major + digit_width

    def position_digits(self):
        """Move each digit sprite based on the frame position"""
        y_offset = self.rect.top + self.settings.lcd_frame_padding_vert
        x_offset = self.rect.left + self.settings.lcd_frame_padding_horz

        self.position_digit_pair(self.digit_M1, self.digit_M2, x_offset, y_offset)
        x_offset = self.digit_M2.rect.right + self.settings.lcd_frame_digit_padding_horz_major

        self.position_digit_pair(self.digit_S1, self.digit_S2, x_offset, y_offset)
        x_offset = self.digit_S2.rect.right + self.settings.lcd_frame_digit_padding_horz_major

        self.position_digit_pair(self.digit_h1, self.digit_h2, x_offset, y_offset)
        
    def set_digit_places(self, time, digit_left, digit_right):
        """Separate the tens and ones digit from each time pair"""
        digit = int(time / 10)
        digit_left.set_digit(digit)
        digit = int(time % 10)
        digit_right.set_digit(digit)
        
    def set_time(self, minutes, seconds, hundredths_of_seconds):
        """Set the correct digits"""
        self.set_digit_places(minutes, self.digit_M1, self.digit_M2)
        self.set_digit_places(seconds, self.digit_S1, self.digit_S2)
        self.set_digit_places(hundredths_of_seconds, self.digit_h1, self.digit_h2)

    def update(self):
        """Update the clock"""
        if self.running:
            self.elapsed_time_ms += self.clock.tick()

        # copy the time and define some "constants"
        total_ms = self.elapsed_time_ms
        ms_per_second = 1000
        ms_per_minute = ms_per_second * 60
        ms_per_hundredth_second = 10

        # MM
        minutes = int(total_ms / ms_per_minute)
        total_ms -= minutes * ms_per_minute

        # SS
        seconds = int(total_ms / ms_per_second)
        total_ms -= seconds * ms_per_second

        # hh
        hundredths_of_seconds = int(total_ms / ms_per_hundredth_second)

        # Now update the sprites
        self.set_time(minutes, seconds, hundredths_of_seconds)

        # Ensure the digits are placed correctly
        if (self.rect != self.last_rect):
            self.last_rect = self.rect
            self.position_digits()

    def draw(self):
        """Draw the visual representation of the clock"""
        self.screen.blit(self.frame_image, self.rect)
        self.digits.draw(self.screen)
