import tkinter as tk
from tkinter import messagebox
from Leaderboard import Leaderboard
from GamePanel import GamePanel


class MainMenu(tk.Tk):
    player_name = None
    player_code = None

    def __init__(self):
        super().__init__()

        self.title("Main Menu")
        self.geometry("400x300")
        self.eval('tk::PlaceWindow . center')

        panel = tk.Frame(self)
        panel.pack(expand=True)

        self.play_button = tk.Button(panel, text="Chơi", command=self.play_game)
        self.leaderboard_button = tk.Button(panel, text="Bảng Xếp Hạng", command=self.show_leaderboard)

        self.play_button.pack(side=tk.LEFT, padx=5)
        self.leaderboard_button.pack(side=tk.LEFT, padx=5)

    def play_game(self):
        # Ẩn cửa sổ Main Menu khi bắt đầu trò chơi
        self.withdraw()

        # Tạo GamePanel và bắt đầu trò chơi
        game_panel = GamePanel(self)  # Truyền MainMenu vào GamePanel
        game_panel.start_game()

    def show_leaderboard(self):
        leaderboard = Leaderboard()  # Leaderboard needs to be implemented
        leaderboard.deiconify()

    @staticmethod
    def check_name(name):
        return all(c.isalpha() or c.isspace() for c in name)


def main():
    def validate_and_create():
        name = name_field.get().strip()
        code = code_field.get().strip()

        if MainMenu.check_name(name) and name and code:
            dialog.destroy()  # Destroy the dialog if name and code are valid
            MainMenu.player_name = name
            MainMenu.player_code = code

            # Tạo và hiển thị MainMenu sau khi người chơi nhập thông tin
            main_menu = MainMenu()
            main_menu.mainloop()  # Chạy lại Main Menu

            # Nếu game kết thúc và muốn quay lại MainMenu:
            main_menu.deiconify()  # Gọi phương thức show để hiển thị lại menu chính
        else:
            # Show warning if information is invalid
            messagebox.showwarning("Error", "Vui lòng nhập đúng và đủ thông tin.")
            dialog.quit()  # Ensure dialog window quits, and we can restart the process

            # After closing the dialog, restart the application to show the dialog again
            main()  # Restart the main function, opening the dialog again

    # Dialog for player input
    dialog = tk.Tk()
    dialog.title("Nhập thông tin người chơi")
    dialog.geometry("300x150")
    dialog.eval('tk::PlaceWindow . center')

    frame = tk.Frame(dialog)
    frame.pack(padx=10, pady=10)

    tk.Label(frame, text="Tên người chơi:").grid(row=0, column=0, sticky='e', pady=5)
    name_field = tk.Entry(frame)
    name_field.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="ID người chơi:").grid(row=1, column=0, sticky='e', pady=5)
    code_field = tk.Entry(frame)
    code_field.grid(row=1, column=1, pady=5)

    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="OK", command=validate_and_create).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    dialog.mainloop()


if __name__ == "__main__":
    main()
