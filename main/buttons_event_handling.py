import tkinter as tk


def add_numbers():
    # Get the values entered by the user from the entry widgets
    num1 = float(entry1.get())
    num2 = float(entry2.get())

    # Add the numbers
    result = num1 + num2

    # Update the result label with the sum
    result_label.config(text="Result: " + str(result), height=10, width=10)


# Create the main window
root = tk.Tk()
root.title("Addition Calculator")

# Create entry labels
entry_label1 = tk.Label(root, text="Enter first number:", height=10, width=25)
entry_label1.pack()

# Create entry widget for the first number
entry1 = tk.Entry(root, width=30)
entry1.pack()

# Create entry label
entry_label2 = tk.Label(root, text="Enter second number:", height=10, width=25)
entry_label2.pack()

# Create entry widget for the second number
entry2 = tk.Entry(root, width=30)
entry2.pack()

# Create a button widget for addition
add_button = tk.Button(root, text="Submit", command=add_numbers)
add_button.pack()

# Create a label widget to display the result
result_label = tk.Label(root, text="Result: ")
result_label.pack()

# Start the Tkinter event loop
root.mainloop()
