"""This module implements the enemy blob type for Floor-jumper"""
# Этот код определяет класс под названием "Blob", 
# который является типом вражеского спрайта в 2D-платформере. 
# Класс Blob наследуется от другого класса под названием "AnimatedSprite", 
# который отвечает за управление анимацией спрайта.

# Конструктор Blob принимает три аргумента: "настройки", "экран" и "изображения". "настройки" 
# - это набор настроек игры, "экран" - это поверхность отображения Pygame, 
# на которой будет нарисован спрайт, а "изображения" - это словарь,
# содержащий кадры анимации спрайта.

# В конструкторе класс Blob устанавливает некоторое начальное состояние для спрайта,
# включая его начальную позицию и анимацию. Метод update_current_animation определяет, 
# какая анимация должна воспроизводиться на основе текущего состояния спрайта 
# (например, ходьба, прыжки или умирание).

# Метод обновления вызывается один раз за игровой кадр и 
# обновляет положение спрайта в зависимости от его скорости и любых столкновений с игровым миром. 
# Если спрайт умирает, он падает вниз до тех пор, пока не исчезнет из нижней части экрана.
# В противном случае спрайт перемещается горизонтально до тех пор, пока не упрется в стену, 
# после чего разворачивается и начинает двигаться в противоположном направлении. 
# Если спрайт падает на плитку "exit", он запускает анимацию смерти.

# Метод handle_collision вызывается, 
# когда спрайт сталкивается с другим спрайтом или блоком в игровом мире.
# Если спрайт сталкивается более чем с одним блоком, он стоит на твердой земле,
# и его состояние падения сбрасывается. В противном случае спрайт падает, 
# и его вертикальная скорость соответствующим образом обновляется.



import pygame
from pygame.sprite import Sprite
from src.animation import Animation
from src.animated_sprite import AnimatedSprite

class Blob(AnimatedSprite):
    """Blob enemy object"""

    def __init__(self, settings, screen, images):
        """Initialize the blob"""
        super().__init__(settings, screen, images)
        
        # Override the start position
        self.dx = self.settings.enemy_blob_dx
        
        # Set the blob-specific animations
        self.animations[self.settings.anim_name_walk_left] = Animation([0, 1, 2, 1], 2)
        self.animations[self.settings.anim_name_walk_right] = Animation([3, 4, 5, 4], 2)
        self.animations[self.settings.anim_name_jump_down_left] = Animation([6], 1)
        self.animations[self.settings.anim_name_jump_down_right] = Animation([6], 1)
        self.animations[self.settings.anim_name_dead] = Animation([7], 60)
        self.current_animation = self.settings.anim_name_walk_right
        self.facing_left = False

    def update_current_animation(self):
        """Set the correct animation based on state"""
        # DYING
        if self.dying:
            self.set_current_animation(self.settings.anim_name_dead)
        # WALKING
        elif self.dy == 0:
            if self.dx < 0:
                self.set_current_animation(self.settings.anim_name_walk_left)
            else:
                self.set_current_animation(self.settings.anim_name_walk_right)
        # JUMPING
        else:
            if self.dy > 0:
                if self.facing_left:
                    self.set_current_animation(self.settings.anim_name_jump_down_left)
                else:
                    self.set_current_animation(self.settings.anim_name_jump_down_right)

    def update(self, tile_map):
        """Updates the blob sprite's position"""
        
        if not self.dying:
            last_dx = self.dx
            super().update(tile_map, tile_map.block_group)
            # Blobs only stop when they hit a wall so reverse course
            if last_dx != 0 and self.dx == 0:
                self.facing_left = not self.facing_left
                if self.facing_left:
                    self.dx = 1.0
                else:
                    self.dx = -1.0

            # Check if the blob is over the "exit" for the enemies, and if so, drop it down
            if tile_map.drainrect.colliderect(self.rect):
                self.dying = True
                self.falling = True
                self.falling_frames = 1
        else:
            if self.dy < self.settings.terminal_velocity:
                self.dy += self.settings.gravity
            
            self.rect.centery += self.dy
            self.falling_frames += 1

            if self.rect.top > self.screen_rect.bottom:
                self.kill()

        self.finish_update()

    def handle_collision(self, collision_list, group):
        """Given a list of sprites that collide with the sprite, alter state such as position, velocity, etc"""
        # If there's only 1 block, then we're over an edge, so do nothing in that case
        # and just let the sprite fall, otherwise, clamp to the top of the block
        if collision_list:
            if len(collision_list) > 1:
                self.falling = False
                self.falling_frames = 1
                self.dy = 0
                self.rect.bottom = collision_list[0].rect.top
            elif len(collision_list) == 1:
                if self.facing_left and self.rect.right > collision_list[0].rect.left:
                    self.falling = False
                    self.falling_frames = 1
                    self.dy = 0
                    self.rect.bottom = collision_list[0].rect.top
                elif not self.facing_left and self.rect.left < collision_list[0].rect.right:
                    self.falling = False
                    self.falling_frames = 1
                    self.dy = 0
                    self.rect.bottom = collision_list[0].rect.top
