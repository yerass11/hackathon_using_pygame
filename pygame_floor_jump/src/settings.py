"""This module implements settings for floor jumper."""
# Этот код определяет класс Python с именем Settings, 
# в котором хранятся все настройки для игры под названием "floor jumper". 
# Класс имеет метод __init__,
# который инициализирует все настройки игры в качестве переменных экземпляра.

# Настройки включают в себя такие параметры экрана, 
# как screen_width, screen_height, caption (заголовок окна), 
# bg_color (цвет фона) и полноэкранный режим. 
# Он также включает в себя настройки шрифта, 
# настройки спрайтов для игрока и врагов, названия анимации, 
# настройки плитки, настройки карты и настройки генератора частиц.

# Пигмейская игра.модуль freetype импортирован,
# чтобы обеспечить способ создания объектов шрифта для рендеринга текста в игре.

# Каждая настройка инициализируется значением по умолчанию, 
# которое может быть изменено по требованию разработчика игры. 
# Например, параметр гравитации для спрайта игрока установлен на 1,4, 
# но это можно отрегулировать, чтобы сделать игру более или менее сложной. 
# Аналогично, настройка player_max_air_jumps позволяет игроку выполнить определенное количество прыжков в воздухе, 
# прежде чем упасть на землю, которые можно настроить, чтобы сделать игру проще или сложнее.

# В целом, этот класс предоставляет разработчику игр удобный способ 
# хранить все игровые настройки в одном месте и 
# изменять их по мере необходимости для точной настройки игры.

import pygame.freetype

class Settings():
    """A class to store all settings for floor jumper."""

    def __init__(self):
        """Initialize the game's settings."""
        
        # screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.caption = "floor jumper"
        self.bg_color = (26, 23, 22)
        self.color_key = (255, 0, 255)
        self.fullscreen = False

        # quick font
        self.font = pygame.freetype.SysFont(None, 16)
        self.font_color = (255, 255, 255)

        # Bonus font
        self.bonus_font = pygame.freetype.SysFont(None, 10)

        # Global sprite settings
        self.gravity = 1.4
        self.terminal_velocity = 12
        
        # Player sprite settings
        self.player_width = 24
        self.player_height = 32
        self.player_jump_velocity = -15
        self.player_air_jump_velocity = -8
        self.player_max_air_jumps = 1
        self.player_dx = 2
        # transparent pixels to offset for horizontal collision (image dependent)
        self.player_sprite_horz_margin = 3
        # transparent pixels to offset for vertical collision (e.g. jumps)
        self.player_sprite_top_margin = 9

        # Animation names
        self.anim_name_idle_left = 'IDLE.L'
        self.anim_name_idle_right = 'IDLE.R'
        self.anim_name_walk_left = 'WALK.L'
        self.anim_name_walk_right = 'WALK.R'
        self.anim_name_jump_up_left = 'JUMPUP.L'
        self.anim_name_jump_down_left = 'JUMPDOWN.L'
        self.anim_name_jump_up_right = 'JUMPUP.R'
        self.anim_name_jump_down_right = 'JUMPDOWN.R'
        self.anim_name_dead = 'DEAD'
        self.anim_name_exit = 'EXIT'

        # level digit sizes
        self.digit_width = 36
        self.digit_height = 48

        # Timer digits (LCD style)
        self.lcd_digit_width = 16
        self.lcd_digit_height = 24

        # Timer frame
        # Pixels from either side to the digit area
        self.lcd_frame_padding_horz = 5
        # Pixels above and below the digit area
        self.lcd_frame_padding_vert = 4
        # Horz spacing between related digits e.g. M M or S S
        self.lcd_frame_digit_padding_horz_minor = 2
        # Horz spacing between unrelated digits e.g. MM:SS or SS:mm
        self.lcd_frame_digit_padding_horz_major = 8
        
        # Blob enemy settings
        self.enemy_blob_width = 16
        self.enemy_blob_height = 16
        self.enemy_blob_dx = 1
        # Upwards velocity when killed by player from block break
        self.enemy_death_dy = -10
        # starting rate
        self.enemy_generation_base_rate = 120
        # current rate
        self.enemy_generation_rate = self.enemy_generation_base_rate
        # amount to decrease rate per level
        self.enemy_generation_level_rate = 5
        
        # Tile settings
        self.tile_width = 24
        self.tile_height = 24

        # Particle generator
        self.particle_gen_color = (255, 0, 0)
        self.particle_gen_dx_range = (-8, 8)
        self.particle_gen_dy_range = (5, 20)
        self.particle_gen_max_frames = 40
        self.particle_gen_per_frame = 5
        
        # Map settings
        self.map_width = 16
        self.map_height = 10
        self.map_playable_width = 10
        self.map_indicies = [-1]
        self.map_number_floors = 8
        self.map_number_subfloors = 1

