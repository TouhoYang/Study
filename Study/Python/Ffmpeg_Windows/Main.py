import tkinter

root = tkinter.Tk()

label = tkinter.Label(root,text="Hello")

root.title("Test")
root.geometry('500x350')
label.pack()

root.mainloop()