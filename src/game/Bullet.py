import pygame

class Bullet:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x  # Tốc độ di chuyển theo hướng X
        self.speed_y = speed_y  # Tốc độ di chuyển theo hướng Y
        self.radius = 5

    def update(self):
        # Di chuyển theo hướng X và Y
        self.x += self.speed_x * 10  # 10 là tốc độ bắn
        self.y += self.speed_y * 10  # 10 là tốc độ bắn

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.radius)