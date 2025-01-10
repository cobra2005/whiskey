import pygame
import math
from Bullet import Bullet

class Player:
    def __init__(self, game_panel):
        self.game_panel = game_panel  # Lưu trữ game_panel vào thuộc tính self.game_panel
        self.x = self.game_panel.screen_width // 2
        self.y = self.game_panel.screen_height // 2
        self.speed = 5
        self.ammo = 10
        self.bullets = []
        self.tile_size = self.game_panel.tile_size
        
        try:
            self.image = pygame.image.load("src\\entity\\Data1\\boy_down_1.png")
            self.image = pygame.transform.scale(self.image, (self.tile_size, self.tile_size))
        except:
            print("Error loading player image")
            self.image = None

    def move(self, keys):
        if keys[pygame.K_UP] and self.y > 0:  # Di chuyển lên, kiểm tra không vượt quá biên trên
            self.image = pygame.image.load("src\\entity\\Data1\\boy_up_1.png")
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < self.game_panel.screen_height - self.tile_size:  # Di chuyển xuống, kiểm tra không vượt quá biên dưới
            self.image = pygame.image.load("src\\entity\\Data1\\boy_down_1.png")
            self.y += self.speed
        if keys[pygame.K_LEFT] and self.x > 0:  # Di chuyển trái, kiểm tra không vượt quá biên trái
            self.image = pygame.image.load("src\\entity\\Data1\\boy_left_1.png")
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < self.game_panel.screen_width - self.tile_size:  # Di chuyển phải, kiểm tra không vượt quá biên phải
            self.image = pygame.image.load("src\\entity\\Data1\\boy_right_1.png")
            self.x += self.speed

        # Các phím khác nếu cần
        if keys[pygame.K_w] and self.y > 0:
            self.image = pygame.image.load("src\\entity\\Data1\\boy_up_1.png")
            self.y -= self.speed
        if keys[pygame.K_s] and self.y < self.game_panel.screen_height - self.tile_size:
            self.image = pygame.image.load("src\\entity\\Data1\\boy_down_1.png")
            self.y += self.speed
        if keys[pygame.K_a] and self.x > 0:
            self.image = pygame.image.load("src\\entity\\Data1\\boy_left_1.png")
            self.x -= self.speed
        if keys[pygame.K_d] and self.x < self.game_panel.screen_width - self.tile_size:
            self.image = pygame.image.load("src\\entity\\Data1\\boy_right_1.png")
            self.x += self.speed


    def shoot(self, mouse_x, mouse_y):
        if self.ammo > 0:  # Only shoot if there's ammo
            # Calculate direction of bullet based on mouse click
            direction_x = mouse_x - self.x
            direction_y = mouse_y - self.y
            length = math.sqrt(direction_x**2 + direction_y**2)  # Get the distance to normalize
            direction_x /= length  # Normalize the vector
            direction_y /= length  # Normalize the vector

            # Create a new bullet
            bullet = Bullet(self.x + self.tile_size // 2, self.y + self.tile_size // 2, direction_x, direction_y)
            self.bullets.append(bullet)
            self.ammo -= 1  # Reduce ammo when shooting

    def draw(self, screen):
        if self.image:
            # Draw the player image if available
            screen.blit(self.image, (self.x, self.y))
        else:
            # If no image is available, draw a default rectangle for the player
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.tile_size, self.tile_size))

        # Draw the bullets
        for bullet in self.bullets:
            bullet.draw(screen)