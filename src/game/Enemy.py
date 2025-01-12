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


class FastEnemy(Enemy):
    def __init__(self, game):
        super().__init__(game)
        self.speed = 2  # Tăng tốc độ di chuyển
        try:
            self.image = pygame.image.load("src\\entity\\Data1\\enemy1_down_1.png")
            self.image = pygame.transform.scale(self.image, (self.tile_size, self.tile_size))
        except:
            print("Error loading enemy image")
            self.image = None

    def update(self, player):
        # Logic di chuyển nhanh hơn
        if self.x < player.x:
            self.x += self.speed
        elif self.x > player.x:
            self.x -= self.speed
        if self.y < player.y:
            self.y += self.speed
        elif self.y > player.y:
            self.y -= self.speed

class StrongEnemy(Enemy):
    def __init__(self, game):
        super().__init__(game)
        self.health = 3  # Quái vật cần bị bắn 3 lần để tiêu diệt
        self.color = (255, 0, 0)  # Màu đỏ để dễ phân biệt
        try:
            self.image = pygame.image.load("src\\entity\\Data1\\enemy4_down_1.png")
            self.image = pygame.transform.scale(self.image, (self.tile_size, self.tile_size))
        except:
            print("Error loading enemy image")
            self.image = None

    def update(self, player):
        # Logic di chuyển tương tự quái thường
        super().update(player)

    def take_damage(self, enemies):
        self.health -= 1
        if self.health <= 0:
            enemies.remove(self)
