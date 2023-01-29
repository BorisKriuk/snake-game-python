import pygame
from variables import SIZE, WINDOW_X, WINDOW_Y
import random


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def move(self):
        self.x = random.randint(0, WINDOW_X/SIZE-1) * SIZE
        self.y = random.randint(0, WINDOW_Y/SIZE-1) * SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()
