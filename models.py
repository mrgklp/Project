from threading import Timer
from pygame.math import Vector2
from pygame.transform import rotozoom
import pygame
import time
from utils import get_random_velocity, load_sound, load_sprite, wrap_position
UP= Vector2(-1, 0)
fire = Vector2(1, 0)
UP1 = Vector2(0, -1)
DOWN = Vector2(0, 1)

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Usercar(GameObject):
    
    ACCELERATION = 0.5
    BULLET_SPEED = 3
    
    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)

        super().__init__(position, pygame.transform.rotate(pygame.transform.scale(
            load_sprite("Usercar"), (55, 40)), 0), Vector2(0))
        
      
    

    def accelerate(self):
        self.velocity += UP1* self.ACCELERATION
    def yavas(self):
        self.velocity += DOWN * self.ACCELERATION
    
    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def shoot(self):
        bullet_velocity = fire * self.BULLET_SPEED
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()


class Obstacles(GameObject):
    def __init__(self, position, size=1):
          
           
        
        self.size = size
          
        
        size_to_scale = {3: 1.0, 2: 0.5, 1: 0.25}
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("Obstacle"), 0, scale)

        super().__init__(position, sprite, Vector2(-1,0))

class RegCar(GameObject):
    def __init__(self, position, size=1):
          
           
        
        self.size = size
          
        
        size_to_scale = {3: 1.0, 2: 0.5, 1: 0.25}
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("RegCar"), 0, scale)

        super().__init__(position, sprite, Vector2(-1,0))

class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity