"""This module implements a sprite that shows the level text"""
# Этот код определяет подкласс класса FlyInSprite, называемый LevelSprite.

# Класс FlyInSprite, по-видимому, является пользовательским классом, который, 
# вероятно, используется для анимации спрайтов, движущихся по экрану.

# Класс LevelSprite используется для создания статического графического спрайта
# для отображения текста "LEVEL" на экране.

# Метод __init__() инициализирует спрайт и принимает два параметра: настройки и экран. 
# Строка super().__init__() вызывает конструктор родительского класса FlyInSprite 
# и передает три аргумента: settings, screen и settings.image_res.level_image. 
# Атрибут level_image в settings.image_res, вероятно, содержит изображение, которое будет отображаться.

# Метод self.set_start_position() вызывается для установки начальной позиции спрайта. 
# Этот метод принимает пять аргументов, которые определяют положение x и y, 
# скорость и направление движения спрайта.
# В этом случае спрайт начинается в нижней части экрана (self.screen_rect.bottom) и 
# имеет определенную координату x (self.screen_rect.слева + self.settings.tile_width). 
# Аргумент 0 задает начальную скорость спрайта, 
# а аргументы -20 и 20 определяют дальность перемещения в направлении x.

from src.flyin_sprite import FlyInSprite

class LevelSprite(FlyInSprite):
    """Static image sprite for 'LEVEL' text"""
    
    def __init__(self, settings, screen):
        """Init the sprite"""
        super().__init__(settings, screen, settings.image_res.level_image)
        self.set_start_position(self.screen_rect.bottom, self.screen_rect.left + self.settings.tile_width, 0, -20, 20)
