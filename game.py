from threading import Timer
import pygame
import time
import utils
from models import Obstacles, RegCar, Usercar
from utils import get_random_position, get_random_velocity, load_sprite, print_text
import models

class RoadGame:
    MIN_OBSTACLE_DISTANCE = 250
    MIN_REG_DISTANCE = 250
    def __init__(self):
        self._init_pygame()
        
        
        self.screen = pygame.display.set_mode((900, 500))
        self.background = pygame.transform.scale(load_sprite("Road", False),(900,500))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""
        self.regular = []
        self.obstacles = []
        self.bullets = []
        self.usercar = Usercar((400, 550), self.bullets.append)
        
        
       
        for _ in range(10):
            start = time.time()
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.usercar.position)
                    > self.MIN_REG_DISTANCE
                ):
                    break
            self.regular.append(RegCar(position))
                       
                
        
        
        for _ in range(10):
            start = time.time()
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.usercar.position)
                    > self.MIN_OBSTACLE_DISTANCE
                ):
                    break
            self.obstacles.append(Obstacles(position))
                
    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("BUsted!")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.usercar
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.usercar.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.usercar:
            
            if is_key_pressed[pygame.K_UP]:
                self.usercar.accelerate()
            if is_key_pressed[pygame.K_DOWN]:
                self.usercar.yavas()
            
    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.usercar:
            for obstacle in self.obstacles:
                if obstacle.collides_with(self.usercar):
                    self.usercar = None
                    self.message = "You lost!"
                    break

        for bullet in self.bullets[:]:
            for obstacle in self.obstacles[:]:
                if obstacle.collides_with(bullet):
                    self.obstacles.remove(obstacle)
                    self.bullets.remove(bullet)
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        #if not self.obstacles and self.usercar:
        #    self.message = "You won!"

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.obstacles, *self.bullets]

        if self.usercar:
            game_objects.append(self.usercar)

        return game_objects