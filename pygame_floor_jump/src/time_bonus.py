"""This module implements the time bonus for killing a blob"""
# Этот код определяет класс под названием "TimeBonus", 
# который представляет собой сокращение времени на убийство врага-блоба в игре. 
# Класс принимает в своем конструкторе несколько параметров, включая прямоугольник, 
# представляющий позицию противника, количество времени, 
# которое должно быть уменьшено в миллисекундах, объект "LevelTimer", 
# который отслеживает прошедшее время на игровом уровне, 
# объект Pygame font для рендеринга текста и текст, который будет отображаться на экране..

# Когда создается экземпляр класса "TimeBonus",
# он сохраняет начальное состояние сокращения времени, 
# включая количество времени и позицию противника. 
# Он также инициализирует несколько других свойств,
# таких как скорость перемещения текста, 
# задержка между каждым кадром и максимальное количество кадров, 
# прежде чем сокращение времени исчезнет.

# Класс предоставляет три метода: "alive()", "update()" и "draw()". 
# Метод "alive()" проверяет, истекло ли максимальное количество кадров, 
# указывая, что сокращение времени должно быть удалено из игры.
# Метод "update()" перемещает текст вверх и случайным образом меняет его цвет. 
# Mетод "draw()" отображает текст на экране с использованием объекта Pygame font,
# но только в том случае, если сокращение времени все еще активно и текст виден на экране.

# В целом, этот класс представляет собой временной бонус в игре,
# который сокращает время, затраченное игроком на убийство врага, 
# и обеспечивает визуальную обратную связь о временном бонусе на экране.
from src.level_timer import LevelTimer
import random
import pygame

class TimeBonus():
    """Time reduction for killing a blob"""

    def __init__(self, enemy_rect, text, milliseconds, level_timer, font):
        """save the initial state"""
        self.ms_reduction = milliseconds
        self.enemy_rect = enemy_rect
        self.dy = -4
        self.frame = 0
        self.frame_delay = 2
        self.frames_max = 80
        self.total_frames = 0
        self.font = font
        self.text = text
        self.text_rect = self.font.get_rect(self.text)
        self.text_rect.left = self.enemy_rect.left
        self.text_rect.top = self.enemy_rect.top
        self.color = (255, 0, 0)

        level_timer.elapsed_time_ms = max(0, level_timer.elapsed_time_ms - milliseconds)

    def alive(self):
        """Check if max frames has expired"""
        return self.total_frames < self.frames_max

    def update(self):
        """Move the text"""
        self.frame += 1
        self.total_frames += 1
        if self.frame > self.frame_delay:
            self.frame = 0
            self.text_rect.move_ip(0, self.dy)
            self.color = (random.choice([255, 0]), 0, random.choice([255, 0]))

    def draw(self, screen):
        """Draw the current text"""
        if self.total_frames < self.frames_max and self.text_rect.top >= 0:
            self.font.render_to(screen, (self.text_rect.left, self.text_rect.top), self.text, self.color)
        

