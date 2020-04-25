from tkinter import *

root = Tk()

height = 800
width = 600

root.geometry(f"{height}x{width}")
root.resizable(0, 0)

frame = Frame(root)
frame.pack()

text = StringVar()
label = Label(frame, textvariable = text)

text.set("yo mabro")

label.pack()

root.mainloop()