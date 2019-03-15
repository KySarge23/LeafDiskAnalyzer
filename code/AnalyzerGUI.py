#!/usr/bin/python3
from tkinter import *

class App(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        self.grid(column=2, row=5)
        self.create_gui()




    def create_gui(self):

        #label for tray number
        self.label = Label(self, text="tray Number(s)")
        self.label.grid(column = 1, row = 2)

        
#initializing the root window
root = Tk()
root.title("Leaf Disk Analyzer")
#the size of the window
root.geometry('600x600')

app=App(root)

#a blank canvas for our GUI
c = Canvas(root, height=600, width=600)

root.mainloop()