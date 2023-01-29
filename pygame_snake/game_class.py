import pygame
from variables import WINDOW_X, WINDOW_Y, SIZE, FONT_COLOR, SCREEN_COLOR
from snake_class import Snake
from apple_class import Apple
from pygame.locals import *
import time


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake 1.0")
        pygame.mixer.init()
        Game.play_background_music()
        self.surface = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
        self.surface.fill((0, 0, 0))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f'Score:{self.snake.length}', True, FONT_COLOR)
        self.surface.blit(score, (10, 10))

    @staticmethod
    def is_collision(x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
        return False

    @staticmethod
    def play_sound(sound_name):
        sound = pygame.mixer.Sound(f"{sound_name}.mp3")
        pygame.mixer.Sound.play(sound)

    @staticmethod
    def play_background_music():
        pygame.mixer.music.load("bg_music_1.mp3")
        pygame.mixer.music.play(-1)

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # with apple
        if Game.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            Game.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # with itself
        for i in range(1, self.snake.length):
            if Game.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                Game.play_sound("crash")
                raise Exception("Game over")

        # out of the field
        if self.is_out_of_the_field():
            Game.play_sound("crash")
            raise Exception("Game over")

    def is_out_of_the_field(self):
        if 0 <= self.snake.x[0] <= WINDOW_X and 0 <= self.snake.y[0] <= WINDOW_Y:
            return False
        return True

    def show_game_over(self):
        self.surface.fill(SCREEN_COLOR)
        image_game_over = pygame.image.load("anaconda.png")
        self.surface.blit(image_game_over, (WINDOW_X/2.5, WINDOW_Y/10))
        font = pygame.font.SysFont("arial", 26)
        line1 = font.render(f"Game is over! Your score is: {self.snake.length}", True, (FONT_COLOR))
        self.surface.blit(line1, (WINDOW_X/5, WINDOW_Y/2))
        line2 = font.render(f"To play again press Enter. To exit press Escape.", True, (FONT_COLOR))
        self.surface.blit(line2, (WINDOW_X / 20, WINDOW_Y / 1.5))

        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):

        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.3)
