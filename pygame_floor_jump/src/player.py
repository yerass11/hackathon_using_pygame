"""This module implements the player object (sprite) for Floor-jumper"""
# Это код на Python, который определяет класс Player,
# наследуемый от класса AnimatedSprite. 
# Объект Player - это спрайтовый объект, представляющий главного героя игры.

# Конструктор проигрывателя инициализирует объект несколькими атрибутами, 
# такими как настройки, экран, изображения, initial_bounding_rect и tile_map. 
# Он вызывает конструктор AnimatedSprite, используя метод super().

# Класс Player имеет несколько других методов, таких как reset(),
# который сбрасывает объект Player для карты, update_current_animation(), 
# который устанавливает правильную анимацию на основе состояния игрока, и collided(), 
# который является обратным вызовом, используемым для изменения базовой 
# проверки столкновения для спрайта player.

# Метод update() обновляет позицию спрайта игрока. 
# Он проверяет, находится ли игрок в верхнем ряду, 
# устанавливает группу врагов и вызывает метод update() класса AnimatedSprite.
# Если игрок сталкивается с вражеским спрайтом, он устанавливает атрибуту dying значение True, 
# атрибуту dy значение -15, атрибуту falling значение True и атрибуту falling_frames значение 1.

# Этот код, по-видимому, является частью игры, 
# которая включает в себя перемещение спрайта игрока и уклонение от врагов.
# Класс Player содержит все необходимые методы и атрибуты для обработки движений и 
# анимации игрока. Поведение объекта Player можно изменить, изменив значения его атрибутов.


from src.animation import Animation
from src.animated_sprite import AnimatedSprite
from src.time_bonus import TimeBonus
import pygame

class Player(AnimatedSprite):
    """Player object"""

    def __init__(self, settings, screen, images, initial_bounding_rect, tile_map):
        """Initialize the player sprite"""
        # Calls AnimatedSprite, which in turn will call pygame.Sprite __init_()
        super().__init__(settings, screen, images)

        self.tile_map = tile_map

        # Override the initial position
        self.initial_bounding_rect = initial_bounding_rect
        self.rect.bottom = initial_bounding_rect.bottom
        self.rect.left = self.screen.get_rect().width / 2

        # Set the transparent margins
        self.margin_left = self.settings.player_sprite_horz_margin
        self.margin_right = self.settings.player_sprite_horz_margin
        self.margin_top = self.settings.player_sprite_top_margin

        # set the optional collision check callback
        self.collision_check = self.collided

        # These are specific to the player object
        self.air_jumps = 0
        self.max_air_jumps = settings.player_max_air_jumps
        self.idle_top = False
        self.idle_counter = 0
        self.won_level = False
        self.at_top = False

        # Add the animations for the player
        self.animations[self.settings.anim_name_idle_left] = Animation([0, 1, 2, 3, 2, 1], 5)
        self.animations[self.settings.anim_name_idle_right] = Animation([5, 6, 7, 8, 7, 6], 5)
        self.animations[self.settings.anim_name_walk_left] = Animation([0, 10, 11, 10], 2)
        self.animations[self.settings.anim_name_walk_right] = Animation([5, 12, 13, 12], 2)
        self.animations[self.settings.anim_name_jump_up_left] = Animation([15], 5)
        self.animations[self.settings.anim_name_jump_down_left] = Animation([16], 5)
        self.animations[self.settings.anim_name_jump_up_right] = Animation([17], 5)
        self.animations[self.settings.anim_name_jump_down_right] = Animation([18], 5)
        self.animations[self.settings.anim_name_dead] = Animation([4], 5)
        self.current_animation = self.settings.anim_name_idle_left
        self.facing_left = True

    def reset(self):
        """Reset the player object for the map"""
        player = self
        player.rect.bottom = self.initial_bounding_rect.bottom
        player.dx = 0.0
        player.dy = 0.0
        player.dying = False
        player.idle_counter = 0
        player.idle_top = False
        player.won_level = False
        player.at_top = False

    def update_current_animation(self):
        """Set the correct animation based on state"""
        # DEAD
        if self.idle_top:
            self.set_current_animation(self.settings.anim_name_idle_left)
        elif self.dying:
            self.set_current_animation(self.settings.anim_name_dead)
        # IDLE
        elif self.dx == 0 and self.dy == 0:
            if self.facing_left:
                self.set_current_animation(self.settings.anim_name_idle_left)
            else:
                self.set_current_animation(self.settings.anim_name_idle_right)
        # WALKING
        elif self.dy == 0:
            if self.dx < 0:
                self.set_current_animation(self.settings.anim_name_walk_left)
            else:
                self.set_current_animation(self.settings.anim_name_walk_right)
        # JUMPING
        else:
            if self.dy < 0:
                if self.facing_left:
                    self.set_current_animation(self.settings.anim_name_jump_up_left)
                else:
                    self.set_current_animation(self.settings.anim_name_jump_up_right)
            else:
                if self.facing_left:
                    self.set_current_animation(self.settings.anim_name_jump_down_left)
                else:
                    self.set_current_animation(self.settings.anim_name_jump_down_right)

    def collided(self, player, sprite):
        """This callback is used to modify the basic collision check for the player sprite"""
        if sprite.dying:
            return False
        
        player_rect = player.rect.copy()
        # shrink the player rect based on the margins
        player_rect.height -= player.settings.player_sprite_top_margin
        player_rect.width -= (player.settings.player_sprite_horz_margin * 2)
        player_rect.midbottom = player.rect.midbottom
        # Now do a standard check with the adjusted Rect
        return player_rect.colliderect(sprite.rect)

    def update(self, tile_map, enemies):
        """Updates the player sprite's position"""

        if not self.dying:
            # Check if we're on the top row
            if self.idle_top:
                self.idle_counter +=1
                if self.idle_counter > (30 * 3):
                    self.won_level = True
            else:
                # AnimatedSprite handles most of this, but save the current enemies Group for the handler
                self.enemies = enemies
                super().update(tile_map, tile_map.block_group)
                if self.dy == 0:
                    self.air_jumps = 0

                # The player needs to also check against the group of enemy sprites
                intersected_blobs = pygame.sprite.spritecollide(self, enemies, False, self.collision_check)
                if intersected_blobs:
                    self.dying = True
                    self.dy = -15
                    self.falling = True
                    self.falling_frames = 1
                    
                player_idle = ((self.current_animation == self.settings.anim_name_idle_left) or (self.current_animation == self.settings.anim_name_idle_right))
                player_walking = ((self.current_animation == self.settings.anim_name_walk_left) or (self.current_animation == self.settings.anim_name_walk_right))
                if (self.rect.bottom <= tile_map.player_bounds_rect.top + 2 * self.settings.tile_height) and (player_idle or player_walking):
                    self.idle_top = True
                    self.at_top = True
                    self.idle_counter = 0
        else:
            if self.rect.top > self.screen_rect.bottom:
                # For now, just reset the player position, but nothing else
                self.rect.bottom = tile_map.player_bounds_rect.bottom
                self.dx = 0.0
                self.dy = 0.0
                self.dying = False
            else:
                if self.dy < self.settings.terminal_velocity:
                    self.dy += self.settings.gravity
                self.rect.centery += self.dy
                self.falling_frames += 1

        self.finish_update()

    def handle_collision(self, collision_list, group):
        """Given a list of sprites that collide with the player, alter state such as position, velocity, etc"""
        # Even though this is a list, the first item should be all we need for now
        if collision_list:
            block = collision_list[0]

            # is this a side-collision?
            side_collision = self.rect.right > block.rect.right  or self.rect.left < block.rect.left

            # Falling is the default case, so check it first
            if self.dy > 0:
                self.falling = False
                self.falling_frames = 1
                self.air_jumps = 0
                self.dy = 0
                self.rect.bottom = block.rect.top
            # If the player is jumping, check for a lower hit
            elif self.dy < 0:
                if self.rect.bottom > block.rect.bottom:
                    self.dy = 0
                    self.rect.top = block.rect.bottom - self.settings.player_sprite_top_margin
                    # remove blocks struck from the bottom
                    group.remove(collision_list)

                    # remove enemies above those blocks
                    self.remove_enemies_above_blocks(collision_list)

            # Now check the left
            elif self.dx > 0:
                if side_collision:
                    self.dx = 0
                    self.rect.right = block.rect.left + self.settings.player_sprite_horz_margin
            elif self.dx < 0:
                if side_collision:
                    self.dx = 0
                    self.rect.left = block.rect.right - self.settings.player_sprite_horz_margin

    def remove_enemies_above_blocks(self, collision_list):
        # build a kill rect to check against the enemies
        kill_rect = collision_list[0].rect
        for sprite in collision_list:
            kill_rect.union_ip(sprite.rect)

        # Shift up one block
        kill_rect.move_ip(0, collision_list[0].rect.height * -1)

        # Now see if any enemies are in this block
        for enemy in self.enemies:
            if kill_rect.colliderect(enemy.rect):
                enemy.dying = True
                enemy.dy = self.settings.enemy_death_dy
                bonus = TimeBonus(enemy.rect, "-0.5 seconds", 500, self.tile_map.level_timer, self.settings.bonus_font)
                self.tile_map.bonuses.append(bonus)
