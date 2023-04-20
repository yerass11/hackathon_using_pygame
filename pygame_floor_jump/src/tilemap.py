# """This module implements a 2D tilemap for Floor-jumper"""
# Этот код определяет класс Tilemap, 
# который представляет коллекцию плиточных спрайтов, 
# составляющих карту. Класс Tilemap имеет следующие методы:

# __init__: Инициализирует объект Tilemap и все принадлежащие ему объекты.
# сброс: Возвращает игру в исходное состояние.
# generate_basic_map: Создает базовую плиточную карту.
# generate_platforms: Добавляет платформы блоков.
# move_map: Перемещает карту на заданную величину.
# blitme: Выводит tilemap на экран.
# check_block_collisions: проверяет наличие столкновений между игроком и платформами блоков.
# check_drain_collisions: проверяет наличие столкновений между игроком и сливом.
# обновление: Обновляет состояние tilemap.
# spawn_enemies: Порождает врагов на карте.
# spawn_bonus: Создает временной бонус на карте.
# spawn_blob_exit: выводит большой двоичный объект на карту.
# remove_enemy: Удаляет данного врага с карты.
# remove_bonus: Удаляет данный временной бонус с карты.
# remove_blob_exit: Удаляет выход большого двоичного объекта с карты.
# get_player_position: Возвращает положение игрока на карте.
# get_block_group: Возвращает группу блоков.
# get_enemies: Возвращает группу врагов.
# get_bonuses: Возвращает временные бонусы.
# get_blob_exit: Возвращает выход из большого двоичного объекта.

from src.player import Player
from src.block import Block
from src.blob_exit import BlobExit
from src.level_info import LevelInfo
from src.level_timer import LevelTimer
from src.time_bonus import TimeBonus
import src.game_functions as gf
import random
from pygame.sprite import Group
import pygame

class Tilemap():
    """Represents a collection of tile (sprites) that represent a map"""

    def __init__(self, settings, screen, map_indicies, images, block_image, exit_images, player_images, blob_images):
        """Initialize the map and all of its owned objects"""
        self.settings = settings
        self.screen = screen
        self.images = images
        self.indicies = map_indicies
        self.screen_rect = screen.get_rect()
        self.player_bounds_rect = pygame.Rect((0,0), (0,0))
        self.block_image = block_image
        self.block_group = Group()
        self.x_offset = 0
        self.drainrect = pygame.Rect((0,0), (0,0))
        self.blob_exit = None
        self.exit_images = exit_images
        self.player = None
        self.player_images = player_images
        self.blob_images = blob_images
        self.enemies = Group()
        self.new_enemy_counter = 0
        self.level_info = LevelInfo(self.settings, self.screen)
        self.level_timer = LevelTimer(self.settings, self.screen)
        self.bonuses = []
        
    def reset(self):
        """Resets the game to the starting state"""
        self.player.reset()
        self.enemies.empty()
        gf.generate_new_random_blob(self.settings, self.screen, self.settings.image_res.enemy_blob_images, self)
        self.generate_platforms()
        self.blob_exit.stop_gibbing()
        self.level_info = LevelInfo(self.settings, self.screen)
        self.settings.enemy_generation_rate = self.settings.enemy_generation_base_rate
        self.level_timer.reset()

    def generate_basic_map(self, number_of_floors, number_of_subfloor_rows=0):
        """Builds a basic tiled map - this depends on the index ordering of the tiles image"""
        # Every 'floor' that is not the bottom or below contains 3 tile rows of the same pattern
        # So just make number_of_floors - 1 entries for those, then generate the bottom 'floor'
        # which just has a different 3rd row of indices.  If tiles below that are needed for
        # looks then they all use the same pattern
        empty_row = [-1, 6, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, 8, -1]
        pipe_row = [-1, 6, 15, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 16, 8, -1]
        bottom_row = [-1, 6, 9,  1,  1,  1,  1,  5, 1,  1,  1,  1,  1, 10, 8, -1]
        sub_row = [-1, 6, 7,  7,  7,  7,  8,  -1,  6,  7,  7,  7,  7, 7, 8, -1]
        drain_col = 7

        row_index = 0
        new_indices = []
        while row_index < (number_of_floors - 1):
            new_indices.extend(empty_row)
            new_indices.extend(pipe_row)
            new_indices.extend(empty_row)
            row_index += 1

        # bottom floor - no enemy generator
        new_indices.extend(empty_row)
        new_indices.extend(empty_row)
        new_indices.extend(bottom_row)

        # optional sub-bottom floor row
        row_index = 0
        while row_index < number_of_subfloor_rows:
            new_indices.extend(sub_row)
            row_index += 1

        # Out with the old, in with the new
        self.indicies.clear()
        self.indicies.extend(new_indices)

        # Add the block platforms
        self.generate_platforms()

        # Calculate the rect that bounds outer movment of the player (and enemies in most cases)
        self.x_offset = (self.screen_rect.width - (self.settings.map_width * self.settings.tile_width)) // 2
        x_offset2 = self.x_offset + self.settings.tile_width * ((self.settings.map_width - self.settings.map_playable_width)/2)
        self.player_bounds_rect.top = 0
        self.player_bounds_rect.left = x_offset2
        self.player_bounds_rect.width = self.settings.map_playable_width * self.settings.tile_width
        self.player_bounds_rect.height = self.screen_rect.height - ((number_of_subfloor_rows + 1) * self.settings.tile_height)

        # Drain collision rect
        self.drainrect.width = self.settings.tile_width
        self.drainrect.height = self.settings.tile_height
        self.drainrect.top = self.player_bounds_rect.bottom
        self.drainrect.left = self.settings.tile_width * drain_col + self.x_offset
        self.drainrect.inflate_ip(self.settings.tile_width * -0.99, self.settings.tile_height * -0.75)
        self.drainrect.move_ip(0, self.settings.tile_height * -0.5)

        # Create the 'exit'
        self.blob_exit = BlobExit(self.settings, self.screen, self.exit_images, self)

        # Create the player
        self.player = Player(self.settings, self.screen, self.player_images, self.player_bounds_rect, self)

        # Position the timer
        self.level_timer.position_frame(self.screen_rect.centery, self.player_bounds_rect.right + self.settings.tile_width * 2)

    def generate_block(self, x, y):
        """Create a new Block object at the given x,y and return it"""
        new_block = Block(self.settings, self.screen, self.block_image)
        new_block.rect.top = y
        new_block.rect.left = x
        return new_block

    def generate_blocks(self, bounding_rect, group, bottom_left=False, bottom_right=False):
        """Generates one of 4 possible block combinations"""
        # Always add the top 2 quadrants
        image_rect = self.block_image.get_rect()
        block_top_left = self.generate_block(bounding_rect.left, bounding_rect.top)
        block_top_right = self.generate_block(bounding_rect.left + image_rect.width, bounding_rect.top)
        group.add(block_top_left)
        group.add(block_top_right)

        # The bottom 2 are optional and random
        # Note these offsets work because the blocks are 1/4 the size of the tile by design
        if bottom_left:
            block_bottom_left = self.generate_block(bounding_rect.left, bounding_rect.top + image_rect.height)
            group.add(block_bottom_left)

        if bottom_right:
            block_bottom_right = self.generate_block(bounding_rect.left + image_rect.width, bounding_rect.top + image_rect.height)
            group.add(block_bottom_right)

    def generate_platforms(self):
        """Make groups of sprites that contain the blocks for the player to stand on"""

        # Every block is contained within the self.player_bounds_rect

        # Find each "row" of tiles that can contain blocks and add some
        # Eligible rows are every 3rd row starting from the 2nd to top, except the very bottom floor
        row_rect = pygame.Rect((self.player_bounds_rect.left, self.player_bounds_rect.top + (self.settings.tile_height * 2)), 
            (self.player_bounds_rect.width, self.settings.tile_width)) 
        
        
        self.block_group.empty()
        for row in range(0, (self.settings.map_number_floors-1)):
            new_group = Group()

            # Each column in the eligble row has 4 valid placements for a block
            # Note - there are more permutations, these are just the ones allowed
            # OO OO OO OO
            # XX OX OX OO
            for col in range(0, self.settings.map_playable_width):
                bounding_rect = pygame.Rect(0, 0, 0,0)
                bounding_rect.top = row_rect.top
                bounding_rect.left = row_rect.left + col * self.settings.tile_width
                self.generate_blocks(bounding_rect, new_group, random.choice([True, False]), random.choice([True, False]))
            
            # Each row is its own group.  This could limit collision checks later
            self.block_group.add(new_group.sprites())
            # Shif the bounding rect down one floor
            row_rect = row_rect.move(0, self.settings.tile_height * 3)

    def update(self):
        """Update all owned objects (blocks, player, enemies, etc)"""
        if self.player.at_top:
            self.level_timer.stop()

        # Check for a reset flag set on the player object
        if self.player.won_level:
            self.player.reset()
            self.enemies.empty()
            gf.generate_new_random_blob(self.settings, self.screen, self.settings.image_res.enemy_blob_images, self)
            self.generate_platforms()
            self.blob_exit.stop_gibbing()
            self.level_info.increase_level()
            self.settings.enemy_generation_rate -= self.settings.enemy_generation_level_rate
            self.level_timer.reset()

        # Update the player
        self.player.update(self, self.enemies)

        # Check if it's time to add a new enemy to the map
        self.new_enemy_counter += 1
        if self.new_enemy_counter >= self.settings.enemy_generation_rate:
            self.new_enemy_counter = 0
            gf.generate_new_random_blob(self.settings, self.screen, self.settings.image_res.enemy_blob_images, self)

        # Update enemies that exist
        for enemy in self.enemies:
            enemy.update(self)

        # Update the 'exit' sprite
        self.blob_exit.update(self.enemies)

        # Update the level info
        self.level_info.update()

        # Update the level timer
        self.level_timer.update()

        # bonuses
        for bonus in self.bonuses:
            bonus.update()
            if not bonus.alive():
                self.bonuses.remove(bonus)

    def draw_tiles(self, draw_grid_overlay=False):
        """Draws just the tile portion of the map"""
        # Make the bottom of the map align with the bottom of the screen
        number_of_rows = len(self.indicies) / self.settings.map_width
        map_height = number_of_rows * self.settings.tile_height
        y_offset = self.screen_rect.height - map_height
        rect = pygame.Rect((self.x_offset, y_offset), (self.settings.tile_width, self.settings.tile_height))
        tiles_draw_per_row = 0

        # Loop through each row and render it, simple for now, map fits on the screen
        for index in self.indicies:
            if index >= 0:
                self.screen.blit(self.images[index], rect)
                if draw_grid_overlay:
                    color_red = (255, 0, 0)
                    pygame.draw.rect(self.screen, color_red, rect, 1)
            tiles_draw_per_row += 1
            rect.left += self.settings.tile_width

            # Every row worth of tiles, drop down one level and reset the x coord
            if tiles_draw_per_row == self.settings.map_width:
                rect.top += self.settings.tile_height
                rect.left = self.x_offset
                tiles_draw_per_row = 0

        # Draw the blocks
        # This works because each block has 'image' member defined
        self.block_group.draw(self.screen)
    
    def draw(self, draw_grid_overlay=False):
        """Draws the tilemap."""
        # Draw the enemies - can't use the Gorup method because of our animation logic
        for enemy in self.enemies:
            enemy.draw()

        self.draw_tiles(draw_grid_overlay)

        # Draw the player
        self.player.draw()

        # Draw the exit
        self.blob_exit.draw()

        # Draw the level info
        self.level_info.draw()

        # Draw the level timer
        self.level_timer.draw()

        # Draw bonuses
        for bonus in self.bonuses:
            bonus.draw(self.screen)