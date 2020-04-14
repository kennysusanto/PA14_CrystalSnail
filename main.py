from tkinter import *

root = Tk()

text = StringVar()
label = Label(root, textvariable = text)

text.set("yo mabro")

label.pack()

root.mainloop()