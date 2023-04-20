"""This module implements the exit for blob sprites on the map"""
# Этот код определяет класс под названием BlobExit, который является подклассом AnimatedSprite 
# и представляет анимированный клинок и генератор частиц в игре. 
# Класс AnimatedSprite обрабатывает изображение и анимацию спрайта, 
# в то время как BlobExit добавляет функциональность для генерации частиц
# при столкновении вражеского спрайта с лезвием.

# Метод __init__ инициализирует класс, 
# вызывая метод __init__ суперкласса, 
# устанавливая местоположение спрайта и определяя генератор частиц. 
# Метод generate_particles создает список начальных скоростей и цветов, 
# используемых генератором частиц. Методы start_gibbing и 
# stop_gibbing активируют и останавливают генератор частиц соответственно.
# Метод draw рисует генератор частиц (при необходимости) и спрайт. 
# Метод update обновляет генератор частиц и ищет новых врагов для gib, 
# в то время как метод update_current_animation никогда не обновляет анимацию, 
# поскольку существует только одна анимация.

# Метод handle_collision проверяет наличие столкновений между вражескими спрайтами и
# лезвием и запускает генератор частиц при возникновении столкновения. 
# Это не удаляет столкнувшийся спрайт из группы.




from src.particle_generator import ParticleGenerator
from src.animation import Animation
from src.animated_sprite import AnimatedSprite
import random

class BlobExit(AnimatedSprite):
    """This class encapsulates the animated blade and the gibbing 
    generator when an enemy sprite is dropped into the drain"""

    def __init__(self, settings, screen, images, tile_map):
        """Initialize the animated blade and the particle generator for the map"""
        # AnimatedSprite init
        super().__init__(settings, screen, images)

        # store the map
        self.tile_map = tile_map

        # Set the location - at the bottom, in the tile with the 'drain'
        self.rect.move_ip(0, 0)
        self.rect.move_ip(self.screen_rect.width /2 - settings.tile_width, self.tile_map.player_bounds_rect.bottom + self.settings.tile_height)
        
        # only 1 animation, could add a "bloody" one
        self.animations[self.settings.anim_name_exit] = Animation([0, 1], 1)
        self.current_animation = self.settings.anim_name_exit

        # Blob gibs
        # Leaving the callback out of this call 'self.generate_particles' will take the default behavior
        # which is randomized differently.  Add a comment to see e.g.
        # ..., settings, settings.particle_gen_color, 0, 0)#, self.generate_particles)
        self.particle_gen = ParticleGenerator(screen, settings, settings.particle_gen_color, 0, 0, self.generate_particles)
        self.particle_gen.x = self.screen_rect.centerx - self.settings.tile_width / 2
        self.particle_gen.y = self.screen_rect.bottom - self.settings.tile_width / 2

        # This is the count of frames the generator will be active upon collision with a blob
        self.particles_frames_max = self.settings.particle_gen_max_frames

        # Override default update handling in the base
        self.bound_by_the_laws_of_physics = False
        self.bound_by_map = False

    def generate_particles(self):
        """Generates a list of initial velocities and colors used by the generator as a callback, the list returned
        should hold a tuple for velocities followed by a color"""
        # This callback allows us to provide specific behavior for the generator without deriving
        # a new class (which is also a valid option)
        new_particle_data = []
        dx_a = self.settings.particle_gen_dx_range[0]
        dx_b = self.settings.particle_gen_dx_range[1]
        dy_a = self.settings.particle_gen_dy_range[0]
        dy_b = self.settings.particle_gen_dy_range[1]
        
        # Count per frame should be fairly low
        for particle_index in range(0, self.settings.particle_gen_per_frame):
            new_data = (random.randint(dx_a, dx_b), random.randint(dy_a, dy_b) * -1, self.settings.particle_gen_color)
            new_particle_data.append(new_data)

        return new_particle_data

    def start_gibbing(self):
        """Activates the timed particle generator (in response to a blob collision)"""
        self.particle_gen.start(self.particles_frames_max)

    def stop_gibbing(self):
        """Stops generation, existing particles will live out whatever short life they have left"""
        self.particle_gen.stop()

    def draw(self):
        """Draw the generator (if needed) and the sprite (always)"""
        # Do this first so the sprite is drawn over the generator
        self.particle_gen.draw()
        super().draw()

    def update(self, enemies):
        """Update - mostly look for new enemies to gib"""
        # Let the particle generator update itself
        self.particle_gen.update()
        super().update(self.tile_map, self.tile_map.enemies)
        # common animated sprite code
        self.finish_update()

    def update_current_animation(self):
        """This never updates as there is only 1 animation"""
        pass
    
    def handle_collision(self, collision_list, group):
        """In this case, we are checking against enemies colliding with the blade"""
        # Check for fresh meat to grind
        for blob in collision_list:
            if blob.rect.colliderect(self.rect):
                self.start_gibbing()
                # Don't need to remove it from the group here, we could, but a future
                # update to the blob will catch it
