import random

from pygame import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound


def load_sprite(name, with_alpha=True):
    path = f"assets/sprites/{name}.jpeg"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def load_sound(name):
    path = f"assets/sounds/{name}.wav"
    return Sound(path)


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_position(surface):
    return Vector2(
        random.randrange(890,900),
        random.randrange(50,400),
        
    )


def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    
    return Vector2(speed, 0)


def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, False, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)