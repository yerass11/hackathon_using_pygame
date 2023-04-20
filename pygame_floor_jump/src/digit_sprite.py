"""This module implements a sprite that represents a single digit 0-9"""
# Этот код определяет класс с именем DigitSprite, 
# который наследуется от класса Fly In Sprite. 
# Flying Sprite - это пользовательский класс, который определяет объект sprite, 
# который может перемещаться в конечную позицию в течение нескольких кадров.

# Класс Digit Sprite предназначен для отображения на экране одной цифры (0-9).
# Метод __init__ инициализирует спрайт начальной цифрой, 
# устанавливает экран и кэширует изображения для этой цифры.

# Метод set_digit проверяет, что цифра находится в диапазоне 0-9, 
# и устанавливает изображение для цифры. 
# Метод set_image устанавливает изображение для доступа к базовому классу sprite.

# Метод увеличения увеличивает цифру на единицу. 
# Если цифра равна 9, он устанавливает цифру в 0 и возвращает True как перенос, 
# указывающий на то, что в цифре есть перенос. 
# Если цифра не равна 9, она просто увеличивает ее и возвращает False в качестве переноса.

# Метод draw отвечает за отображение текущей цифры на экране. 
# Это размывает изображение цифры в прямоугольнике спрайта.




from src.flyin_sprite import FlyInSprite

class DigitSprite(FlyInSprite):
    """Digit sprite object which can also flyin to position"""

    def __init__(self, settings, screen, images, digit=0):
        """Init the sprite"""
        super().__init__(settings, screen, images[0])

        # cache these objects
        self.images = images
        self.image_index = 0
        self.set_digit(digit)
        self.screen_rect = screen.get_rect()
        self.rect = self.images[self.image_index].get_rect()


    def set_digit(self, digit):
        """Verify the range, then store the new digit to display"""
        if digit > 9 or digit < 0:
            raise ValueError('Digit should always be 0-9, this is an internal bug')
        
        self.image_index = digit
        self.set_image()

    def set_image(self):
        """Sets the current image for the base class to access"""
        self.image = self.images[self.image_index]

    def increase(self):
        """Increase the digit.  If it's reached the end, e.g. '9' then return that as carry=True
        and reset to 0"""
        carry = False
        if self.image_index < 9:
            self.image_index += 1
        else:
            self.image_index = 0
            carry = True

        self.set_image()
        return carry

    def draw(self):
        """Draw the current digit"""
        self.screen.blit(self.image, self.rect)



