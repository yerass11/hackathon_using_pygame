"""This module caches images for the Floor-jumper game"""
# Это код на Python, который определяет класс Image Resources для хранения 
# всех загруженных данных изображения для игры. Класс имеет метод инициализатора, 
# который загружает и сохраняет различные изображения, используемые в игре, 
# такие как рамки плитки, рамки спрайта для игрока и вражеского блоба, 
# изображение блока платформы, спрайт выхода, изображения цифр и ЖК-цифр, кадры таймера и текст УРОВНЯ.

# Метод load_image_to_tiles() используется для разделения изображения на плитки заданной ширины 
# и высоты, а затем добавления полученных поверхностей к списку изображений. 
# Он использует pygame из библиотеки Pygame. 
# Поверхность и pygame.Методы Surface.blit() для создания новой поверхности
# размером с плитку и копирования подраздела изображения на поверхность.

# В целом, этот код показывает, как загрузить и сохранить необходимые изображения 
# для игры с помощью Pygame, а также как разделить изображение на плитки заданного размера.



import pygame

class ImageResources():
    """Hold all of the loaded image data to be shared"""

    def __init__(self, settings):
        """Load and store the images we need"""

        self.settings = settings
        # Load the tile frames
        self.tile_images = []
        tile_images = self.tile_images
        self.load_image_to_tiles('images/tiles.bmp', self.settings.tile_width, self.settings.tile_height, tile_images)

        # Load the sprite frames
        self.player_sprite_images = []
        player_images = self.player_sprite_images
        self.load_image_to_tiles('images/sprite_player.bmp', self.settings.player_width, self.settings.player_height, player_images)

        # Load the enemy blob frames
        self.enemy_blob_images = []
        blob_images = self.enemy_blob_images
        self.load_image_to_tiles('images/sprite_blob.bmp', self.settings.enemy_blob_width, self.settings.enemy_blob_height, blob_images)

        # Load the platform block image
        self.block_image = pygame.image.load('images/block.bmp')
        self.block_image.set_colorkey(self.settings.color_key)

        # Load the exit sprite (blade)
        self.blob_exit_images = []
        exit_images = self.blob_exit_images
        self.load_image_to_tiles('images/sprite_exit.bmp', self.settings.tile_width, self.settings.tile_height, exit_images)

        # Load digits
        self.digit_images = []
        digit_images = self.digit_images
        self.load_image_to_tiles('images/digits.bmp', self.settings.digit_width, self.settings.digit_height, digit_images)

        # Load 'LCD' digits
        self.lcd_digit_images = []
        lcd_digit_images = self.lcd_digit_images
        self.load_image_to_tiles('images/timer_digits.bmp', self.settings.lcd_digit_width, self.settings.lcd_digit_height, lcd_digit_images)

        # Load timer frames - no need for a color key on this one
        self.lcd_frame_image = pygame.image.load('images/timer_frame.bmp')

        # Load 'LEVEL' text
        self.level_image = pygame.image.load('images/level_text.bmp')
        self.level_image.set_colorkey(self.settings.color_key)
        

    def load_image_to_tiles(self, file_name, tile_width, tile_height, images):
        """Load the specified image and attempt to split it into tiles
        of the specified width and height."""
        image = pygame.image.load(file_name)
        image_rect = image.get_rect()

        image_width = image_rect.width
        image_height = image_rect.height

        # Calculate the number of tiles in one row of the image (ignoring any remaining space)
        tiles_per_row = image_width // tile_width
        # Calculate the number of tiles in one col of the image (ignoring any remaining space)
        tiles_per_col = image_height // tile_height

        # The index for the row is over the number of cols in a row and vice versa
        for row_index in range(0, tiles_per_col):
            for col_index in range(0, tiles_per_row):
                # Create a new surface the size of the tile
                new_surface = pygame.Surface((tile_width, tile_height))
                # Set transparency color key (colors matching this won't get copied in blits)
                new_surface.set_colorkey(self.settings.color_key)
                # Copy just the sub-section of the image onto the surface
                new_surface.blit(image, (0, 0), (col_index * tile_width, row_index * tile_height, tile_width, tile_height))
                # Now add it to our list of surfaces, these will be index-addressed for now
                images.append(new_surface)