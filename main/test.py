from tkinter import *

window = Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
print(screen_height, screen_width)
window.geometry(f"{screen_width - 10}x{screen_height - 90}+0+0")
window.resizable(False, False)  # Make window non-resizable

# Create the frame with desired background color
main_frame = Frame(window, bg="#11DFBD", height=400, width=300)

# Place the frame within the window (using pack() in this example)
main_frame.grid()

window.mainloop()
