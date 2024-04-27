import tkinter as tk
from PIL import ImageTk, Image
import random

class WhackAMoleGame:
    def __init__(self, root, width=600, height=400, mole_size=50, time_limit=30):
        self.root = root
        self.root.title("Whack-a-Mole")

        self.width = width
        self.height = height
        self.mole_size = mole_size
        self.time_limit = time_limit
        self.score = 0
        self.mole_speed = 2000  # Default speed in milliseconds

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        self.mole_image = ImageTk.PhotoImage(Image.open("img.png").resize((self.mole_size, self.mole_size)))
        self.mole_id = None
        self.time_remaining = self.time_limit

        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack()

        self.timer_label = tk.Label(root, text=f"Time: {self.time_remaining}", font=("Arial", 16))
        self.timer_label.pack()

        self.speed_label = tk.Label(root, text="Speed:")
        self.speed_label.pack()

        self.speed_scrollbar = tk.Scale(root, from_=100, to=2000, orient=tk.HORIZONTAL, command=self.change_speed)
        self.speed_scrollbar.pack()

        self.root.bind("<Button-1>", self.whack_mole)

        self.start_game()

    def start_game(self):
        self.update_timer()
        self.spawn_mole()

    def spawn_mole(self):
        if self.mole_id:
            self.canvas.delete(self.mole_id)
        x = random.randint(self.mole_size, self.width - self.mole_size)
        y = random.randint(self.mole_size, self.height - self.mole_size)
        self.mole_id = self.canvas.create_image(x, y, image=self.mole_image, anchor=tk.NW)
        self.root.after(self.mole_speed, self.spawn_mole)

    def whack_mole(self, event):
        if self.mole_id:
            mole_coords = self.canvas.coords(self.mole_id)
            x, y = event.x, event.y
            if mole_coords[0] <= x <= mole_coords[0] + self.mole_size and mole_coords[1] <= y <= mole_coords[1] + self.mole_size:
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                self.canvas.delete(self.mole_id)
                self.spawn_mole()

    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.config(text=f"Time: {self.time_remaining}")
            self.root.after(1000, self.update_timer)
        else:
            self.end_game()

    def end_game(self):
        self.canvas.delete("all")
        self.canvas.create_text(self.width // 2, self.height // 2, text=f"Game Over\nScore: {self.score}", font=("Arial", 24), justify="center")

    def change_speed(self, speed):
        self.mole_speed = int(speed)

if __name__ == "__main__":
    root = tk.Tk()
    game = WhackAMoleGame(root)
    root.mainloop()
