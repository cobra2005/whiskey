import tkinter as tk
from tkinter import messagebox, scrolledtext, font
import os

class Leaderboard(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Leaderboard")
        self.geometry("400x300")
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2
        self.geometry(f"400x300+{x}+{y}")

        # Create text area with scrollbar
        self.leaderboard_area = scrolledtext.ScrolledText(self)
        self.leaderboard_area.configure(font=('Monospace', 14))
        self.leaderboard_area.configure(state='disabled')
        self.leaderboard_area.pack(expand=True, fill='both')

        self.load_scores()

    def load_scores(self):
        scores = []
        try:
            if os.path.exists("leaderboard.txt"):
                with open("leaderboard.txt", "r") as reader:
                    for line in reader:
                        # Check if line contains the separator " - "
                        if " - " in line:
                            scores.append(line.strip())

                # Sort scores in descending order
                def sort_key(s):
                    try:
                        return -int(s.split(" - ")[1].split(":")[1].strip())
                    except (IndexError, ValueError):
                        return 0

                scores.sort(key=sort_key)
                self.display_leaderboard(scores)
        except IOError as e:
            print(e)  # For debugging
            messagebox.showerror("Error", "Cannot load leaderboard.")

    def display_leaderboard(self, scores):
        self.leaderboard_area.configure(state='normal')
        self.leaderboard_area.delete('1.0', tk.END)
        for score in scores:
            self.leaderboard_area.insert(tk.END, f"{score}\n")
        self.leaderboard_area.configure(state='disabled')

    def save_score(self, score, player_name, player_code):
        try:
            with open("leaderboard.txt", "a") as writer:
                writer.write(f"{player_name} (ID: {player_code}) - Score: {score}\n")
        except IOError as e:
            print(e)  # For debugging
