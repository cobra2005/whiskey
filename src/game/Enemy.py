import pygame
import random

class Enemy:
    def __init__(self, game_panel):
        self.x = random.randint(0, game_panel.screen_width)
        self.y = random.randint(0, game_panel.screen_height)
        self.speed = 1
        self.tile_size = game_panel.tile_size
        try:
            self.image = pygame.image.load("src\\entity\\Data\\enemy_down_1.png")
            self.image = pygame.transform.scale(self.image, (self.tile_size, self.tile_size))
        except:
            print("Error loading enemy image")
            self.image = None

    def update(self, player):
        # Di chuyển về phía người chơi
        if self.x < player.x:
            self.x += self.speed
        elif self.x > player.x:
            self.x -= self.speed
        if self.y < player.y:
            self.y += self.speed
        elif self.y > player.y:
            self.y -= self.speed

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.tile_size, self.tile_size))