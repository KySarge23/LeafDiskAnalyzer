#!/usr/bin/python3

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

#import calendarPicker as cp 


#Author(s): Erica Gitlin, Colton Eddy, Kyle Sargent


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

        self.option = StringVar()
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

        self.status = Label(root, text="Sending inputs...")

        self.progress = ttk.Progressbar(root, orient ="horizontal", length = 200, mode= "indeterminate")
        self.bytes = 0
        self.maxbytes = 0

        def start(self):
            self.progress["value"] = 0
            self.maxbytes = 50000
            self.progress["maximum"] = 50000
            self.read_bytes()

        def read_bytes(self):
            '''simulate reading 500 bytes; update progress bar'''
            self.bytes += 500
            self.progress["value"] = self.bytes
            if self.bytes < self.maxbytes:
                # read more bytes after 100 ms
                self.after(100, self.read_bytes)
    


if __name__ == '__main__':
    #initializing the root window
    root = tk.Tk()
    #the size of the window
    root.geometry('350x300')
    root.title("LDA GUI v1.0")
    gui = analyzerGUI(root) #create new instance of the analyzerGUI with root as master.
    
    trayNumArr = []
    picNumArr = []
    
    trays = ""
    pics = ""
    date = ""

    numTrays = 0
    numPics = 0

    # following lines uncomment if want to use calendarPicker.py 
    # def date():
    #     cp.DatePicker(format_str='%s-%02d-%s')

    def validateTP(x,y):
        """
        
        Function to validate the Tray/Picture entries. We initialize countx and county for counting correct or 
        valid characters found from the inputs.
        Then we loop over each string and check if the character is valid (e.g. digit, '-' or ','). 
        If so we increment count, if not we show a warning with the invalid character 
        and clear the entry field in which the invalid character was found. 
        After character validation, we check if countx and county 
        are equal to the length of the strings passed in, meaning that each character was valid.

        Input(s): x (String), y (String)
        Output(s): boolean value based on whether or not both strings are valid.
        Local Varaible(s): countx (int), county (int)

        """
        if x == "":
            messagebox.showwarning("No Entry Warning!", "No entry found in the Tray Entry Field. Please enter data in the following format: '1-3' or '1,2,3'.")
            return False
        if y == "":
            messagebox.showwarning("No Entry Warning!", "No entry found in the Picture Entry Field. Please enter data in the following format: '1-3' or '1,2,3'.")
            return False

        countx, county = 0, 0
        for i in x:
            if i.isdigit() or i == '-' or i == ',':
                countx += 1
            else:
                messagebox.showwarning("Entry warning!", "Incorrect character of: '" + i + "' in Tray Entry Field. Please enter in the following format: '1-3' or '1,2,3'.")
                gui.trayEntry.delete(0,tk.END)                

                return False     
        for o in y:
            if o.isdigit() or o == '-' or o == ',':
                county += 1
            else: 
                messagebox.showwarning("Entry warning!", "Incorrect character of: '" + o + "' in Picture Entry Field. Please enter in the following format: '1-3' or '1,2,3'.")
                gui.picEntry.delete(0,tk.END)                
                return False

        if countx == len(x) and county == len(y):
            return True
        
    def validateDate(date):
        """
        Function to validate the date input by the user. We check if date is less than 6 because it allows for folders to be structured 
        as d-m-yy as well. Otherwise we check for digits and the '-' character if anything else is found, 
        then we warn the user about the found character and then clear the entry field for retrying.
        
        Input(s): date (String)
        Output(s): boolen if count found == len of date 
        Local Varaible(s): count (int)

        """
        if date == "":
            messagebox.showwarning("No Entry Warning!", "No entry found in Date entry. Please enter a date in the following format: 'mm-dd-yy'.")
            return False

        elif len(date) < 6 or len(date) > 8 :
            messagebox.showwarning("Date Warning!", "Date entered has too many or too little characters. Please enter a date in the following format: 'mm-dd-yy'")
            gui.dateEntry.delete(0,tk.END)
            return False
        else:
            count = 0
            for i in date:
                if i.isdigit() or i == '-':
                    count+=1
                else: 
                    messagebox.showwarning("Entry warning!", "Incorrect character of: '" + i + "' in Date Entry Field. Please enter in the following format: mm-dd-yy")
                    gui.dateEntry.delete(0,tk.END)
                    return False
            if count == len(date):
                return True
    
    def findOccurrences(s, ch):
        """
        Function to find occurances of a character in a string. only useful for when ',' is used in an entry field.

        Input(s): s (String), ch (Character)
        Output(s): a list of indicies in which ch was found in s.
        Local Variable(s): None

        """    
        return [i for i, letter in enumerate(s) if letter == ch]

    def getNumbers(input):
        """
        Function to extract the numbers from the entry fields after they've been validated. 
        This will grab the numbers found surrounding a '-' or multiple ',' in an entry field. 
        Then will place either the range of numbers or sequence of numbers in a list
        and return that to the Analyzer.

        Input(s): input (String)
        Output(s): nums[] (list of ints)
        Local Variables: idx (int), n1/n2 (int), nums[] (list of ints), comms [] (list of indicies where ',' is found)

        """

        nums, comms = [], []

        n1,n2 = 0,0

        if '-' in input:
            idx = input.index('-')
            n1 = int(input[idx-1])
            n2 = int(input[idx+1])
            if n1 > n2: 
                return messagebox.showwarning("Entry Warning!", "Left Hand Side of '-' is greater than Right Hand Side. Please fix the order and retry.")
            else:
                for i in range (n1, n2+1):
                    nums.append(i)
                return nums
        
        if ',' in input and len(input) >= 3:
            comms = findOccurrences(input, ',')
            for idx in comms:
                n1 = int(input[idx-1])
                n2 = int(input[idx+1])
                if n1 in nums:
                    nums.append(n2)
                elif n2 in nums:
                    nums.append(n1)
                else:
                    nums.append(n1)
                    nums.append(n2)
            return nums

        if len(input) == 1:
            n1 = int(input)
            nums.append(n1)
            return nums
    
    def newOrExisting():
       value = gui.option.get()
       if value == "True":
            print("Creating new Spread Sheet")
            new = True
            print(new)
            return True
       elif value == "False":
            print("Going to Existing")
            new = False
            print(new)
            return True
       else:
            print("An option must be selected")

    def upload():
        """
        Function to send data from entry fields to diskAnalyzer. We grab the entry fields' values and strip any 
        whitespace from the front/back so that it doesnt mess up with our validation methods. 
        Then we validate the entry fields and upon them returning true, 
        we disable all buttons and add a status label to let the user know we're sending the inputs. 
        
        Input(s): None
        Output(s) None
        Local Varaible(s): None

        """

        trays = gui.trayEntry.get() .rstrip().lstrip()
        pics = gui.picEntry.get().rstrip().lstrip()
        date = gui.dateEntry.get().rstrip().lstrip()

        trayNumArr = getNumbers(trays)
        picNumArr = getNumbers(pics)
        numTrays = len(trayNumArr)
        numPics = len(picNumArr)
        
        if numPics * numTrays > 8:
            return messagebox.showwarning("Input Warning!", "Current inputs from Tray/Picture entry fields will spawn too many threads. Use the following as a guide for entering data into tray/pictures entry fields: trays * pictures <= 8.")
            

        if validateTP(trays, pics) and validateDate(date) and newOrExisting():
            gui.trayEntry.config(state='disabled')      
            gui.picEntry.config(state='disabled')  
            gui.dateEntry.config(state='disabled')    
            uploadBtn.config(state='disabled')
            gui.r1.config(state='disabled')
            gui.r2.config(state='disabled')
            # calendarBtn.config(state='disabled')
            print(trays)
            print(pics)
            print(date)
            print("Tray Numbers are: " + str(trayNumArr))
            print("Picture Numbers are: " + str(picNumArr))
            gui.status.grid(row = 7, column = 1, pady=(50,0))
            gui.progress.grid(row=8, column = 1)
            gui.progress.start()

            
        return
                


    # calendarBtn = tk.Button(root, text="Pick a Date", command=date)
    # calendarBtn.grid(row = 6, column = 1)
    uploadBtn = tk.Button(root, text= "Upload", command=upload, height = 1, width = 12 )
    uploadBtn.grid(row= 5, column = 0)

    root.mainloop()


