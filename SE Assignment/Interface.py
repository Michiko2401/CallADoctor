from tkinter import Tk, ttk, Canvas, Button

def resize_columns(event, tree):
    # Get the width of the window
    window_width = event.width

    # Calculate the width for each column
    column_width = window_width // 2

    # Set the width for each column
    tree.column("#0", width=column_width)
    tree.column("#1", width=column_width)

# Create the main window
window = Tk()
window.geometry("1080x664")

# Create a Canvas widget for the blue box and buttons
canvas = Canvas(window, width=81, height=664, bg="#5271FF", highlightthickness=0)
canvas.pack(side="left", fill="y")

# Create Button 2
button_2 = Button(
    window,
    text="Button 2",
    bg="#5271FF",
    fg="#FFFFFF",
    borderwidth=0,
    command=lambda: print("Button 2 clicked")
)
button_2.place(in_=canvas, x=0, y=305, width=81, height=73)

# Create Button 4
button_4 = Button(
    window,
    text="Button 4",
    bg="#5271FF",
    fg="#FFFFFF",
    borderwidth=0,
    command=lambda: print("Button 4 clicked")
)
button_4.place(in_=canvas, x=0, y=0, width=81, height=73)

# Create Button 5
button_5 = Button(
    window,
    text="Button 5",
    bg="#5271FF",
    fg="#FFFFFF",
    borderwidth=0,
    command=lambda: print("Button 5 clicked")
)
button_5.place(in_=canvas, x=0, y=167, width=81, height=73)

# Create a Treeview widget
tree = ttk.Treeview(window, show='headings', height=1)

# Add a single empty row with values
tree.insert("", "end", values=("Value 1", "Value 2"))

# Bind the resize event to adjust column widths
window.bind("<Configure>", lambda event: resize_columns(event, tree))

# Place the treeview in the window
tree.pack(fill="both", expand=True, side="left")

# Start the Tkinter event loop
window.mainloop()
