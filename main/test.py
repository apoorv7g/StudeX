from tkinter import *
import pyautogui

window = Tk()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
print(screen_height,screen_width)
window.geometry(f"{screen_width}x{screen_height-125}+0+0")
window.mainloop()
