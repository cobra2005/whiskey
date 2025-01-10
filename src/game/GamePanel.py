import pygame
import random
import tkinter as tk
from tkinter import messagebox
import sys
import os
import math
from PIL import Image, ImageTk
from Leaderboard import Leaderboard
from Player import Player
from Bullet import Bullet
from Enemy import Enemy
from AmmoBox import AmmoBox

class GamePanel:
    def update(self):
        # Cập nhật đạn, kẻ địch, và kiểm tra va chạm
        for bullet in self.player.bullets:
            bullet.update()

        for enemy in self.enemies:
            enemy.update(self.player)

        # Kiểm tra va chạm giữa đạn và kẻ địch
        surviving_bullets = []  # Create a new list to store bullets that survived collisions
        for bullet in self.player.bullets:
            bullet_collided = False  # Flag to track if the bullet collided
            for enemy in self.enemies[:]:
                if abs(bullet.x - enemy.x) < self.tile_size and abs(bullet.y - enemy.y) < self.tile_size:
                    self.enemies.remove(enemy)
                    self.score += 1  # Tăng điểm khi tiêu diệt kẻ địch
                    bullet_collided = True
                    break  # No need to check for more enemies if the bullet already collided

            if not bullet_collided:
                surviving_bullets.append(bullet)  # Add the bullet to the new list if it didn't collide

        self.player.bullets = surviving_bullets  # Update the player's bullets with the surviving bullets

        # Kiểm tra va chạm giữa người chơi và hộp đạn
        for ammo_box in self.ammo_boxes[:]:
            if ammo_box.is_picked_up(self.player):
                self.ammo_boxes.remove(ammo_box)
                self.player.ammo += 5  # Thêm 5 viên đạn khi nhặt được hộp đạn

        # Tạo hộp đạn mới sau mỗi khoảng thời gian
        self.ammo_box_timer += 1
        if self.ammo_box_timer >= self.ammo_box_spawn_rate:
            self.ammo_boxes.append(AmmoBox(self))
            self.ammo_box_timer = 0  # Reset timer

        # Sinh ra kẻ địch mới sau mỗi khoảng thời gian
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_rate:
            self.enemies.append(Enemy(self))  # Tạo kẻ địch mới
            self.enemy_spawn_timer = 0  # Reset timer

            # Tăng tốc độ sinh kẻ địch theo thời gian
            self.enemy_spawn_rate = max(30, self.enemy_spawn_rate - 5)  # Tăng tốc độ sinh kẻ địch (giảm thời gian giữa các lần sinh kẻ địch)
    # Tăng tốc độ sinh kẻ địch (giảm thời gian giữa các lần sinh kẻ địch)

    def draw(self):
        # Vẽ các đối tượng trên màn hình
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        # Vẽ người chơi, kẻ địch, và hộp đạn
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for ammo_box in self.ammo_boxes:
            ammo_box.draw(self.screen)

        # Hiển thị điểm số và số lượng đạn
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        ammo_text = font.render(f"Ammo: {self.player.ammo}", True, (255, 255, 255))
        self.screen.blit(ammo_text, (10, 40))

        # Cập nhật màn hình
        pygame.display.flip()

    def __init__(self, main_menu):
        pygame.init()
        self.main_menu = main_menu


        self.original_tile_size = 16
        self.scale = 3
        self.tile_size = self.original_tile_size * self.scale
        self.max_screen_col = 32
        self.max_screen_row = 18
        self.screen_width = self.tile_size * self.max_screen_col
        self.screen_height = self.tile_size * self.max_screen_row

        self.FPS = 60
        self.enemies = []  # Đặt lên đây trước khi sử dụng
        self.ammo_boxes = []  # Đặt lên đây trước khi sử dụng

        self.random = random.Random()

        self.frame_count = 0
        self.score = 0

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.main_menu = main_menu
        self.running = True

        # Initialize player
        self.player = Player(self)

        # Load background
        try:
            self.background = pygame.image.load("src\\game\\Data\\bg.png")
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except:
            print("Error loading background image")
            self.background = None

        # Load and start background sound
        pygame.mixer.init()
        try:
            self.background_sound = pygame.mixer.Sound("src\\game\\Data\\background.wav")
            self.background_sound.play(-1)  # -1 for loop
        except:
            print("Error loading background sound")

        # Initialize game over dialog (Tkinter)
        self.root = tk.Tk()
        self.root.withdraw()  # Hide Tkinter window initially


        # Tạo kẻ địch ban đầu
        self.enemies.append(Enemy(self))  # Đặt sau khi đã khởi tạo self.enemies

        # Tạo hộp đạn ban đầu
        self.ammo_boxes.append(AmmoBox(self))  # Đặt sau khi đã khởi tạo self.ammo_boxes

        # Initialize ammo box timer and spawn rate
        self.ammo_box_timer = 0
        self.ammo_box_spawn_rate = 200  # Adjust spawn rate as needed (in frames)

        # Initialize enemy spawn timer and spawn rate
        self.enemy_spawn_timer = 0
        self.enemy_spawn_rate = 100  # Adjust spawn rate as needed (in frames)  # Thời gian đếm để sinh kẻ địch mới

    def start_game(self):
        while self.running:
            self.handle_events()  # Xử lý sự kiện
            self.update()         # Cập nhật logic trò chơi
            self.draw()           # Vẽ màn hình
            self.check_collision_with_enemy()  # Kiểm tra va chạm
            self.clock.tick(self.FPS)

    def handle_events(self):
        keys = pygame.key.get_pressed()  # Lấy trạng thái của tất cả các phím

        # Gọi phương thức move từ Player để di chuyển nhân vật
        self.player.move(keys)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            # Kiểm tra sự kiện click chuột trái
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 là mã nút cho chuột trái
                    mouse_x, mouse_y = pygame.mouse.get_pos()  # Lấy vị trí chuột trên màn hình
                    self.player.shoot(mouse_x, mouse_y)  # Truyền tọa độ chuột vào phương thức shoot

            

    def check_collision_with_enemy(self):
        # Check collision between player and enemies
        for enemy in self.enemies:
            if abs(self.player.x - enemy.x) < self.tile_size and abs(self.player.y - enemy.y) < self.tile_size:
                self.game_over()

    def show_game_over_message(self):
        # Hiển thị hộp thoại Game Over
        messagebox.showinfo("Game Over", f"Game Over! Your score: {self.score}")
        sys.exit()  # Thoát chương trình hoàn toàn sau khi người dùng nhấn "OK"


    def game_over(self):
        # Hiển thị thông báo Game Over
        self.show_game_over_message()

        self.running = False  # Kết thúc vòng lặp game hiện tại
        # Ẩn cửa sổ game và quay lại menu chính
        
        self.main_menu.show()  # Hiển thị lại menu chính

    def back_to_main_menu(self):
        # Trở lại menu chính
        print("Returning to Main Menu...")
        self.running = False  # Kết thúc vòng lặp game hiện tại

if __name__ == "__main__":
    # Khởi tạo GamePanel và bắt đầu trò chơi
    game_panel = GamePanel(None)  # Không cần menu chính và cửa sổ Tkinter
    game_panel.start_game()
