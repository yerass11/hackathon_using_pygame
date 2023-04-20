# Этот код представляет собой скрипт на Python для игры под названием "Floor jumper". 
# Он импортирует несколько модулей, которые содержат игровую логику, настройки и ресурсы, 
# в том числе "game_functions.py ", "image_resources.py ", "settings.py ", и "tilemap.py ". 
# Он также импортирует модули "random" и "pygame" для различных функциональных возможностей.

# Основной точкой входа в игру является функция "run_game()", 
# которая инициализирует Pygame, загружает настройки игры и ресурсы изображения, 
# создает 2D-карту с использованием загруженных ресурсов и сбрасывает состояние игры.
# Затем он входит в игровой цикл, 
# который обрабатывает системные события и обновляет состояние игры, 
# включая вывод карты плиток на экран. Цикл управляется объектом Pygame clock, 
# который обеспечивает запуск игры с фиксированной частотой 30 кадров в секунду.

# В целом, код представляет собой простой, но полноценный игровой скрипт,
# который инициализирует, запускает и управляет базовой игрой на основе Pygame.

import src.game_functions as gf
from src.image_resources import ImageResources
from src.settings import Settings
from src.tilemap import Tilemap
import random
import pygame

def run_game():
    """Main entry point for Floor-jumper"""

    # Startup pygame object
    pygame.init()

    random.seed()

    # Load our settings object and image resources, disk I/O that can be done in advance
    settings = Settings()
    image_res = ImageResources(settings)
    # Add to the cache so it's accessible where needed
    settings.image_res = image_res

    # Create the main screen to render to based on settings
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption(settings.caption)
    
    # Create a 2D tilemap - this takes a list of indices and an image list to produce a tiled surface
    tile_map = Tilemap(settings, screen, settings.map_indicies, image_res.tile_images, 
        image_res.block_image, image_res.blob_exit_images, image_res.player_sprite_images, image_res.enemy_blob_images)

    # Overwrite default indices with generated map 
    tile_map.generate_basic_map(settings.map_number_floors , settings.map_number_subfloors)

    # Reset the game
    gf.reset_game(tile_map)

    # Use pygame's simple loop management for a fixed 30 FPS
    clock = pygame.time.Clock()
    while True:
        # Should make sure each frame spends at least 1/30 seconds in this loop
        # downside is wasted sleep on fast hardware and slow hardware will lag
        # but slow hardware will always lag and implementing a time-delta based
        # loop for this simple game is IMHO overkill.
        clock.tick(30)

        # Process system events (key-presses, joystick, etc)
        gf.check_events(settings, screen, tile_map)

        # Update the game (this will update all sub-object and render them to the screen)
        gf.update_screen(settings, screen, tile_map)
    
# Invokes the function above when the script is run
run_game()

