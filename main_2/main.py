import tkinter as tk
from tkinter import simpledialog
import random
import csv


class ChaseTheMole:
    def __init__(self, root1, width=600, height=400, mole_size=55, time_limit=31):
        self.root = root1
        self.root.title("CHASE THE MOLE")
        self.end = False
        self.width = width
        self.height = height
        self.mole_size = mole_size
        self.time_limit = time_limit
        self.score = 0

        self.canvas = tk.Canvas(root1, width=self.width, height=self.height, bg="#0fab24")
        self.canvas.pack()

        self.mole_color = "#9e4a11"
        self.mole_id = None
        self.time_remaining = self.time_limit

        self.score_label = tk.Label(root1, text=f"Score: {self.score}", font=("Roboto", 16), bg="lightgreen")
        self.score_label.pack(fill='x')

        self.timer_label = tk.Label(root1, text=f"Time: {self.time_remaining}", font=("Roboto", 16), bg="lightgreen")
        self.timer_label.pack(fill='x')

        self.root.bind("<Button-1>", self.whack_mole)

        self.start_game()

    def start_game(self):
        self.spawn_mole(time1=5000)
        self.update_timer()

    def spawn_mole(self, time1):
        if not self.end:
            if self.mole_id:
                self.canvas.delete(self.mole_id)
            x = random.randint(self.mole_size, self.width - self.mole_size)
            y = random.randint(self.mole_size, self.height - self.mole_size)
            self.mole_id = self.canvas.create_oval(x, y, x + self.mole_size, y + self.mole_size, fill=self.mole_color,
                                                   activefill="#6b310a")
            self.root.after(time1, self.spawn_mole, time1)

    def whack_mole(self, event):
        if not self.end and self.mole_id:
            mole_coords = self.canvas.coords(self.mole_id)
            x, y = event.x, event.y
            if (mole_coords[0] <= x <= mole_coords[2]
                    and mole_coords[1] <= y <= mole_coords[3]):
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                self.root.after(10, self.spawn_mole, 5000)

    def update_timer(self):
        if not self.end and self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.config(text=f"Time: {self.time_remaining}")
            self.root.after(1000, self.update_timer)
        else:
            self.end_game()

    def end_game(self):
        self.end = True
        if self.mole_id:
            self.canvas.delete(self.mole_id)
            self.score_label.destroy()
            self.timer_label.destroy()
        self.canvas.create_text(self.width // 2, self.height // 2,
                                text=f"Game Over\nScore: {self.score}",
                                font=("Roboto", 24), justify="center")
        self.root.after(3000, self.save_score)

    def save_score(self):
        name = simpledialog.askstring("Enter Your Name", "Enter your name:")
        if name:
            with open("scores.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([name, self.score])


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    game = ChaseTheMole(root)
    root.mainloop()
