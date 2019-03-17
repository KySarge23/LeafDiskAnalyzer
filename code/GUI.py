#!/usr/bin/python3

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

#import calendarPicker as cp 


#Author(s): Erica Gitlin, Colton Eddy, Kyle Sargent, Emily Box


class analyzerGUI:
    def __init__(self, master):
        """ 
        Initialization of all entry fields, labels, buttons, etc that are necessary for the GUI. 
        we use self.___(name) for all because then we can access their values outside of the class and thus allow for 
        manipulation/capturing/checking

        Input(s): self, master
        Output(s): None

        """

        #a blank canvas for our GUI
        self.c = Canvas(master, height=300, width=300)
        self.menu = Menu(master) 
        master.config(menu=self.menu) 

        self.filemenu = Menu(self.menu) 
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='New') 
        self.filemenu.add_command(label='Open...') 
        self.filemenu.add_separator() 
        self.filemenu.add_command(label='Exit', command=master.quit) 
        self.helpmenu = Menu(self.menu) 
        self.menu.add_cascade(label='Help', menu=self.helpmenu) 
        self.helpmenu.add_command(label='About')

        self.option = StringVar(value = "1")
        self.r1 = Radiobutton(master, text = "New Spreadsheet", value ="True" , var=self.option)
        self.r1.grid(row = 0, column = 0, padx = (0, 10))
        self.r2 = Radiobutton(master, text="Existing Spreadsheet", value="False", var=self.option)
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
        self.trayEntry.bind("<FocusIn >", clearTrayEntry)

        self.picLabel = Label(master, text = "Picture Number(s):")
        self.picLabel.grid(row = 2, column = 0, pady = (0,10))
        self.picEntry = Entry(master)
        self.picEntry.grid(row = 2, column = 1, pady = (0,10))
        self.picEntry.insert(0,"Placeholder: '1-3'")
        self.picEntry.bind("<FocusIn>", clearPicEntry)

        self.dateLabel= Label(master, text="Date")
        self.dateLabel.grid(row = 3, column= 0, pady=(0,60))
        self.dateEntry = Entry(master)
        self.dateEntry.insert(0,"Date: 'mm-dd-yy'")
        self.dateEntry.grid(row = 3, column = 1, pady=(0,60))
        self.dateEntry.bind("<FocusIn>", clearDateEntry)

        # self.status = Label(master, text="Sending inputs...")

        # self.progress = ttk.Progressbar(master, orient ="horizontal", length = 150, mode= "indeterminate")
        # self.bytes = 0
        # self.maxbytes = 0

        # def start(self):
        #     self.progress["value"] = 0
        #     self.maxbytes = 50000
        #     self.progress["maximum"] = 50000
        #     self.read_bytes()

        # def read_bytes(self):
        #     '''simulate reading 500 bytes; update progress bar'''
        #     self.bytes += 500
        #     self.progress["value"] = self.bytes
        #     if self.bytes < self.maxbytes:
        #         # read more bytes after 100 ms
        #         self.after(100, self.read_bytes)
