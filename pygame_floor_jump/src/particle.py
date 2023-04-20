"""Particle object module for Floor-jumper"""
# Это код на Python, который определяет класс с именем Particle в библиотеке pygame.
# Класс Particle представляет собой отдельный объект particle, 
# который может генерироваться и управляться отдельным классом генератора или функцией.
# Класс Particle имеет несколько методов, 
# которые определяют его поведение и внешний вид на экране:

# __init__(self, screen, settings, x, y, dx, dy, width, color): 
#     метод конструктора класса Particle, который принимает несколько аргументов, 
#     включая экранный объект для рисования, настройки системы частиц,
#     начальное положение и скорость частицы, его ширина и цвет.
# update(self): Этот метод обновляет скорость и положение частицы на основе физики системы. 
#     Он обновляет координаты x и y частицы на основе ее текущей скорости, 
#     а также учитывает влияние силы тяжести и конечной скорости.
# alive(self): Этот метод проверяет, находится ли частица все еще в пределах экрана или нет. Если частица покинула экран, она считается мертвой и может быть удалена из системы.
# draw(self): Этот метод рисует частицу на экране с помощью функции 
# pygame.draw.rect(), которая принимает объект экрана, цвет частицы, 
# а также положение и размер частицы в качестве аргументов. 
# Он просто рисует заполненный прямоугольник на экране в текущем положении частицы.
# В целом, этот код определяет базовый класс Particle,
# который может использоваться для генерации частиц 
# и управления ими в системе частиц с использованием библиотеки pygame. 
# Класс частиц может быть дополнительно настроен или 
# расширен для создания более сложных эффектов частиц.



import pygame

class Particle():
    """A single particle object which is owned by the generator"""
    def __init__(self, screen, settings, x, y, dx, dy, width, color):
        """Save the initial state"""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.settings = settings
        self.width = width

    def update(self):
        """Update the particle's velocity and position"""
        self.x += self.dx
        self.dy += self.settings.gravity
        if self.dy > self.settings.terminal_velocity:
            self.dy = self.settings.terminal_velocity
        self.y += self.dy

    def alive(self):
        """Once the particle has left the screen, it's not useful, so consider it dead"""
        return self.y <= self.screen_rect.bottom

    def draw(self):
        """Draw the particle at its current location"""
        # We're not a sprite, so just draw a simple filled rect
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.width))