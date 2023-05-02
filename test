# Import the required library
from tkinter import *

# Create an instance of tkinter frame
win = Tk()

# Define geometry of the window
win.geometry("700x250")

def temp_text(e):
   textbox.delete(0,"end")

textbox = Entry(win, bg="white", width=50, borderwidth=2)
textbox.insert(0, "This is Temporary Text...")
textbox.pack(pady=20)

textbox.bind("<FocusIn>", temp_text)

win.mainloop()