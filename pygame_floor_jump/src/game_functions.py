"""This module implements standard game functions for Floor-jumperr, such as processing keypresses"""
# Этот код является частью видеоигры, запрограммированной с использованием библиотеки Pygame,
# набора модулей Python, предназначенных для написания видеоигр. 
# Он включает в себя несколько функций, определяющих поведение игры, 
# таких как проверка событий клавиатуры и мыши, генерация новых врагов, 
# обновление и рисование игровых объектов, сброс игры, а также обновление и переворачивание экрана.

# Инструкции import в начале кода импортируют различные библиотеки, 
# используемые в коде, включая библиотеку sys для системных функций, 
# библиотеку random для генерации случайных чисел, класс Blob из модуля src.blob_enemy, 
# а также pygame и pygame.библиотеки freetype для написания видеоигры.

# Функция check_events проверяет наличие событий клавиатуры и мыши и 
# соответствующим образом вызывает другие функции. Например, 
# если пользователь нажмет кнопку "ВЫЙТИ", функция завершит работу программы с помощью функции sys.exit(). 
# Если пользователь нажимает клавиши со стрелками "ВЛЕВО" или "ВПРАВО", 
# функция вызовет функцию check_keydown_events, чтобы проверить, идет ли игрок влево или вправо.

# Функция reset_game сбрасывает игру, вызывая функцию reset объекта tile_map.

# Функция check_keydown_events реагирует на события нажатия клавиши, 
# вызывая другие функции в зависимости от того, какая клавиша была нажата.
# Например, если пользователь нажмет клавишу "a", 
# функция вызовет функцию generate_new_random_blob для создания нового врага. 
# Если пользователь нажмет клавиши со стрелками "ВЛЕВО" или "ВПРАВО", 
# функция проверит, находится ли проигрыватель в режиме ожидания, 
# и соответствующим образом установит атрибут dx проигрывателя. 
# Если пользователь нажмет клавишу "F9", функция переключит полноэкранный режим.

# Функция check_keyup_events реагирует на события key up, 
# устанавливая для атрибута dx игрока значение 0, 
# если отпущены клавиши со стрелками "ВЛЕВО" или "ВПРАВО", 
# и проверяя, падает ли игрок и использовал ли он уже прыжок в воздух, 
# если отпущена клавиша "ПРОБЕЛ".

# Функция generate_new_random_blob генерирует нового врага, 
# выбирая случайный этаж и сторону, устанавливая начальную позицию противника, 
# скорость и флаги "лицом к лицу" и добавляя врага в список врагов объекта tile_map.

# Функция blit_help_text выводит на экран текст,объясняющий, что делают различные клавиши.

# Функция update_game_objects обновляет игровые объекты, такие как игрок и враги.

# Функция draw_game_objects рисует игровые объекты, такие как карта и текст справки.

# Функция update_screen обновляет и переворачивает экран, 
# чтобы показать изменения, внесенные в игровые объекты.




import sys
import random
from src.blob_enemy import Blob
import pygame
import pygame.freetype

def check_events(settings, screen, tile_map):
    """Watch for keyboard and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(settings, event, screen, tile_map)
        elif event.type == pygame.KEYUP:
        	check_keyup_events(settings, event, screen, tile_map)

def reset_game(tile_map):
    tile_map.reset()

def check_keydown_events(settings, event, screen, tile_map):
    """Respond to key down events"""
    player = tile_map.player
    if event.key == pygame.K_ESCAPE:
        sys.exit()

    if event.key == pygame.K_a:
        generate_new_random_blob(settings, screen, settings.image_res.enemy_blob_images, tile_map)
        
    if event.key == pygame.K_r:
        reset_game(tile_map)
    
    if event.key == pygame.K_LEFT:
        if not player.idle_top:
            if player.dx == 0.0:
                player.dx = -1 * settings.player_dx
                player.facing_left = True
    
    if event.key == pygame.K_RIGHT:
        if not player.idle_top:
            if player.dx == 0.0:
                player.dx = settings.player_dx
                player.facing_left = False
        
    if event.key == pygame.K_F9:
        if settings.fullscreen == True:
            settings.fullscreen = False
            pygame.display.set_mode((800, 600))
        else:
            settings.fullscreen = True
            pygame.display.set_mode((800, 600), pygame.FULLSCREEN)

def check_keyup_events(settings, event, screen, tile_map):
    player = tile_map.player
    if event.key == pygame.K_SPACE:
        if not player.idle_top:
            if player.falling == False:
                player.dy = settings.player_jump_velocity
                player.falling = True
            elif player.air_jumps < player.max_air_jumps:
                player.dy = settings.player_air_jump_velocity
                player.air_jumps += 1

    if event.key == pygame.K_LEFT:
        if not player.idle_top:
            if player.dx != 0.0:
                player.dx = 0.0
        
    if event.key == pygame.K_RIGHT:
        if not player.idle_top:
            if player.dx != 0.0:
                player.dx = 0.0

def generate_new_random_blob(settings, screen, images, tile_map):
    """Generate a new blob enemy and add it to the list"""
    # How this should work:  First pick a floor, this is the middle_row of the triad created
    # when generating the map, e.g. not the floor and not a level where blocks can appear
    floor_number = random.randint(0, settings.map_number_floors - 2)

    # Secondly pick a side, left or right (this will affect placement and initial velocity, etc)
    facing_left = random.choice([True, False])

    # Calculate initial position / velocity / facing flags
    enemy = Blob(settings, screen, images)
    enemy.rect.bottom = settings.tile_height * ( 2 + (3 * floor_number))
    enemy.rect.left = 3 * settings.tile_width + tile_map.x_offset
    enemy.dx = settings.enemy_blob_dx

    if facing_left:
        enemy.rect.left += 10 * settings.tile_width
        enemy.dx *= -1.0
        enemy.facing_left = True
        enemy.set_current_animation(settings.anim_name_walk_left)
    else:
        enemy.facing_left = False
        enemy.set_current_animation(settings.anim_name_walk_right)

    # Add it to the list
    tile_map.enemies.add(enemy)
    
def blit_help_text(settings, screen):
    """Draws the text explaining what keys do what"""
    color_white = (255, 255, 255)
    y = screen.get_rect().bottom - 48
    font = settings.font
    font.render_to(screen, (10,y), "ESC to exit", settings.font_color)
    y -= 20
    font.render_to(screen, (10,y), "F9 to toggle fullscreen", settings.font_color)
    y -= 20
    font.render_to(screen, (10,y), "'a' to add a new enemy", settings.font_color)
    y -= 20
    font.render_to(screen, (10,y), "'r' to reset", settings.font_color)
    y -= 20
    font.render_to(screen, (15,y), "...can jump once in air", settings.font_color)
    y -= 20
    font.render_to(screen, (10,y), "SPACE to jump", settings.font_color)
    y -= 20
    font.render_to(screen, (10,y), "LEFT/RIGHT arrows to walk", settings.font_color)
    
def update_game_objects(settings, tile_map):
    tile_map.update()

def draw_game_objects(settings, screen, tile_map):
    # Draw the map - pass True to render a grid overlay on the tiles
    tile_map.draw()

    # Draw help text
    blit_help_text(settings, screen)

def update_screen(settings, screen, tile_map):
    """Update images and flip screen"""
    # Redraw screen each pass
    screen.fill(settings.bg_color)

    # UPDATES...
    update_game_objects(settings, tile_map)

    # DRAWS...
    draw_game_objects(settings, screen, tile_map)

    # FLIP....
    pygame.display.flip()
