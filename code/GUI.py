#!/usr/bin/python3

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


#Author(s): Erica Gitlin, Colton Eddy, Kyle Sargent, Emily Box

class analyzerGUI:
    def __init__(self, master):
        """ 
        Initialization of all entry fields, labels, buttons, etc that are necessary for the GUI. 
        we use self.___(name) for all because then we can access their values outside of the class and thus allow for 
        manipulation/capturing/checking

        Input(s): self, master
        Output(s): None
        Local Variable(s): c (Canvas), menu (Menu), fileMenu (Menu), option (StringVar), r1/r2 (RadioButton),
                           trayLabel/picLabel/dateLabel (Label), trayEntry/picEntry/dateEntry (Entry)
                           
        """
        #a blank canvas for our GUI
        self.c = Canvas(master, height=300, width=300)
        self.menu = Menu(master) 
        master.config(menu=self.menu) 
        self.helpmenu = Menu(self.menu) 


        def showAbout():
            messagebox.showinfo(title="About", message="This software is for the examinging of Leaf Disks, obtained from grape leaves, to determine whether or not specific leaf disks are resistant to the growth of Downy Mildew.")

        def showCopyright():
            messagebox.showinfo(title="Copyright", message = "This is the copyright")


        def on_exit():
            """When you click to exit, this function is called"""
            if messagebox.askyesnocancel("Exit", "Are you sure you want to close this application?"):
                master.destroy()

        master.protocol("WM_DELETE_WINDOW", on_exit)

        self.menu.add_cascade(label='About', menu=self.helpmenu) 
        self.helpmenu.add_command(label='About LDA', command= showAbout)
        self.helpmenu.add_command(label= 'Copyright', command = showCopyright)

        self.option = StringVar(value = "1")
        self.r1 = Radiobutton(master, text = "Create New Spreadsheet", value ="True" , var=self.option)
        self.r1.grid(row = 0, column = 0, padx = (0, 10))
        self.r2 = Radiobutton(master, text="Use Existing Spreadsheet", value="False", var=self.option)
        self.r2.grid(row = 0, column = 1)
        
        def clearTrayEntry(event):
            """
            Function to clear entry field. Upon the event passed in, we execute this function.
            Input(s): event
            Output(s): None
            
            """
            self.trayEntry.delete(0,tk.END)
        
        def clearPicEntry(event):
            self.picEntry.delete(0,tk.END)

        def clearDateEntry(event):
            self.dateEntry.delete(0,tk.END)


        self.trayLabel = Label(master, text= "Tray Number(s):" )
        self.trayLabel.grid(row = 1, column = 0, pady = (0,10))
        self.trayEntry = Entry(master)
        self.trayEntry.insert(0,"Placeholder: '1-3'")   
        self.trayEntry.grid(row = 1, column = 1, pady = (0,10))
        self.trayEntry.bind("<Button-1>", clearTrayEntry)

        self.picLabel = Label(master, text = "Picture Number(s):")
        self.picLabel.grid(row = 2, column = 0, pady = (0,10))
        self.picEntry = Entry(master)
        self.picEntry.grid(row = 2, column = 1, pady = (0,10))
        self.picEntry.insert(0,"Placeholder: '1-3'")
        self.picEntry.bind("<Button-1>", clearPicEntry)

        self.dateLabel= Label(master, text="Date:")
        self.dateLabel.grid(row = 3, column= 0, pady=(0,60))
        self.dateEntry = Entry(master)
        self.dateEntry.insert(0,"Date: 'mm-dd-yy'")
        self.dateEntry.grid(row = 3, column = 1, pady  = (0,60))
        self.dateEntry.bind("<Button-1>", clearDateEntry)