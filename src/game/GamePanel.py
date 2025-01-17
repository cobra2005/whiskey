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
from Enemy import Enemy, StrongEnemy, FastEnemy
from AmmoBox import AmmoBox

class GamePanel:
    def update(self):
        self.elapsed_time += 1 / self.FPS  # Cập nhật thời gian trôi qua
        # Cập nhật đạn, kẻ địch, và kiểm tra va chạm
        for bullet in self.player.bullets:
            bullet.update()

        for enemy in self.enemies:
            enemy.update(self.player)

        # Kiểm tra va chạm giữa đạn và kẻ địch
        surviving_bullets = []  # Create a new list to store bullets that survived collisions
        for bullet in self.player.bullets:
            bullet_collided = False
            for enemy in self.enemies[:]:
                if abs(bullet.x - enemy.x) < self.tile_size and abs(bullet.y - enemy.y) < self.tile_size:
                    

                    enemy.take_damage(self.enemies)  

                    self.score += 1  # Tăng điểm
                    bullet_collided = True
                    break  # Không cần kiểm tra các quái khác

            if not bullet_collided:
                surviving_bullets.append(bullet)

        self.player.bullets = surviving_bullets  # Update the player's bullets with the surviving bullets

        # Kiểm tra va chạm giữa người chơi và hộp đạn
        for ammo_box in self.ammo_boxes[:]:
            if ammo_box.is_picked_up(self.player):
                self.ammo_boxes.remove(ammo_box)
                self.pick_sound.play()
                self.player.ammo += 5  # Thêm 5 viên đạn khi nhặt được hộp đạn

        # Tạo hộp đạn mới sau mỗi khoảng thời gian
        self.ammo_box_timer += 1
        if self.ammo_box_timer >= self.ammo_box_spawn_rate:
            self.ammo_boxes.append(AmmoBox(self))
            self.ammo_box_timer = 0  # Reset timer

        # Sinh ra kẻ địch mới sau mỗi khoảng thời gian
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_rate:
            if self.score >= 50:
                enemy_type = random.choice(['normal', 'fast', 'strong'])  # Chọn loại quái ngẫu nhiên
                while True:
                    if enemy_type == 'normal':
                        new_enemy = Enemy(self)
                    elif enemy_type == 'fast':
                        new_enemy = FastEnemy(self)
                    elif enemy_type == 'strong':
                        new_enemy = StrongEnemy(self)

                    # Kiểm tra khoảng cách với người chơi
                    if abs(new_enemy.x - self.player.x) >= self.tile_size * 2 and abs(new_enemy.y - self.player.y) >= self.tile_size * 2:
                        self.enemies.append(new_enemy)
                        break  # Thoát vòng lặp khi vị trí hợp lệ
            elif self.score >= 20:
                enemy_type = random.choice(['normal', 'fast'])  # Chọn loại quái ngẫu nhiên
                while True:
                    if enemy_type == 'normal':
                        new_enemy = Enemy(self)
                    elif enemy_type == 'fast':
                        new_enemy = FastEnemy(self)

                    # Kiểm tra khoảng cách với người chơi
                    if abs(new_enemy.x - self.player.x) >= self.tile_size * 2 and abs(new_enemy.y - self.player.y) >= self.tile_size * 2:
                        self.enemies.append(new_enemy)
                        break  # Thoát vòng lặp khi vị trí hợp lệ
            
            else:
                while True:
                    new_enemy = Enemy(self)

                    # Kiểm tra khoảng cách với người chơi
                    if abs(new_enemy.x - self.player.x) >= self.tile_size * 2 and abs(new_enemy.y - self.player.y) >= self.tile_size * 2:
                        self.enemies.append(new_enemy)
                        break  # Thoát vòng lặp khi vị trí hợp lệ

            self.enemy_spawn_timer = 0  # Reset timer
            self.enemy_spawn_rate = max(50, self.enemy_spawn_rate - 5)  # Giảm thời gian giữa các lần sinh


    def draw(self):
        # Vẽ các đối tượng trên màn hình
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        # Vẽ người chơi, kẻ địch, và hộp đạn
        self.player.draw(self.screen)
        for enemy in self.enemies:
            if isinstance(enemy, StrongEnemy) and self.strong_enemy_image:
                self.screen.blit(self.strong_enemy_image, (enemy.x, enemy.y))
            elif isinstance(enemy, FastEnemy) and self.fast_enemy_image:
                self.screen.blit(self.fast_enemy_image, (enemy.x, enemy.y))
            else:
                enemy.draw(self.screen)  # Vẽ quái thường

        for ammo_box in self.ammo_boxes:
            ammo_box.draw(self.screen)

        # Hiển thị điểm số và số lượng đạn
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        ammo_text = font.render(f"Ammo: {self.player.ammo}", True, (255, 255, 255))
        self.screen.blit(ammo_text, (10, 40))

        # Tính toán thời gian theo định dạng mm:ss
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        time_text = f"{minutes:02}:{seconds:02}"  # Định dạng với 2 chữ số

        # Hiển thị thời gian        
        time_font = pygame.font.SysFont('Arial', 48)
        time_surface = time_font.render(time_text, True, (255, 255, 255))
        text_width = time_surface.get_width()
        text_height = time_surface.get_height()

        # Tính vị trí để hiển thị ở giữa màn hình
        x_position = (self.screen_width - text_width) // 2
        y_position = self.screen_height // 10  # Ví dụ: đặt ở 1/10 chiều cao màn hình

        # Vẽ thời gian ra màn hình
        self.screen.blit(time_surface, (x_position, y_position))

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
        self.running = True
        self.paused = False  # Trạng thái tạm dừng
        self.elapsed_time = 0  # Thời gian đã trôi qua tính bằng giây

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

        # Load and start skill sound
        try:
            self.skill_sound = pygame.mixer.Sound("src\\game\\Data\\skill.WAV")
        except:
            print("Error loading skill sound")
            self.skill_sound = None

        # Load and start pick sound
        try:
            self.pick_sound = pygame.mixer.Sound("src\\game\\Data\\pick.wav")
        except:
            print("Error loading pick sound")
            self.pick_sound = None

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

        try:
            self.strong_enemy_image = pygame.image.load("src\\game\\Data\\strong_enemy.png")
            self.strong_enemy_image = pygame.transform.scale(self.strong_enemy_image, (self.tile_size, self.tile_size))
        except:
            print("Error loading strong enemy image")
            self.strong_enemy_image = None

        try:
            self.fast_enemy_image = pygame.image.load("src\\game\\Data\\fast_enemy.png")
            self.fast_enemy_image = pygame.transform.scale(self.fast_enemy_image, (self.tile_size, self.tile_size))
        except:
            print("Error loading fast enemy image")
            self.fast_enemy_image = None

    def start_game(self):
        while self.running:
            self.handle_events()  # Xử lý sự kiện

            if not self.paused:  # Chỉ cập nhật và vẽ nếu không tạm dừng
                self.update()         # Cập nhật logic trò chơi
                self.draw()           # Vẽ màn hình
                self.check_collision_with_enemy()  # Kiểm tra va chạm
            else:
                self.draw_pause_screen()  # Vẽ màn hình tạm dừng

            self.clock.tick(self.FPS)

    def draw_pause_screen(self):
        # Làm mờ màn hình hoặc vẽ màn hình tạm dừng
        font = pygame.font.SysFont('Arial', 48)
        pause_text = font.render("Game Paused", True, (255, 255, 255))
        self.screen.blit(pause_text, ((self.screen_width - pause_text.get_width()) // 2, self.screen_height // 2))
        pygame.display.flip()  # Cập nhật màn hình

    

    def handle_events(self):
        keys = pygame.key.get_pressed()  # Lấy trạng thái của tất cả các phím

        # Gọi phương thức move từ Player để di chuyển nhân vật (nếu không bị tạm dừng)
        if not self.paused:
            self.player.move(keys)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Nếu bấm phím Esc
                    self.paused = not self.paused  # Chuyển đổi trạng thái tạm dừng

            # Kiểm tra sự kiện click chuột trái (chỉ khi không tạm dừng)
            if not self.paused and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 là mã nút cho chuột trái
                    self.skill_sound.play()
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
        
        

    def back_to_main_menu(self):
        # Trở lại menu chính
        print("Returning to Main Menu...")
        self.running = False  # Kết thúc vòng lặp game hiện tại

if __name__ == "__main__":
    # Khởi tạo GamePanel và bắt đầu trò chơi
    game_panel = GamePanel(None)  # Không cần menu chính và cửa sổ Tkinter
    game_panel.start_game()
