import tkinter as tk
from tkinter import *
from tkinter import messagebox

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
        self.trayLabel.grid(row = 0, column = 0, pady = (0,10))
        self.trayEntry = Entry(master)
        self.trayEntry.insert(0,"Placeholder: '1-3'")   
        self.trayEntry.grid(row = 0, column = 1, pady = (0,10))
        self.trayEntry.bind("<FocusIn >", clearTrayEntry)

        self.picLabel = Label(master, text = "Picture Number(s):")
        self.picLabel.grid(row = 1, column = 0, pady = (0,10))
        self.picEntry = Entry(master)
        self.picEntry.grid(row = 1, column = 1, pady = (0,10))
        self.picEntry.insert(0,"Placeholder: '1-3'")
        self.picEntry.bind("<FocusIn>", clearPicEntry)

        self.dateLabel= Label(master, text="Date")
        self.dateLabel.grid(row = 4, column= 0, pady=(0,60))
        self.dateEntry = Entry(master)
        self.dateEntry.insert(0,"Date: 'mm-dd-yy'")
        self.dateEntry.grid(row = 4, column = 1, pady=(0,60))
        self.dateEntry.bind("<FocusIn>", clearDateEntry)



if __name__ == '__main__':
    #initializing the root window
    root = tk.Tk()
    #the size of the window
    root.geometry('300x300')
    root.title("LDA GUI v1.0")
    gui = analyzerGUI(root) #create new instance of the analyzerGUI with root as master.
    trays = ""
    pics = ""
    date = ""

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

        """

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
        
        Input(s): date
        Output(s): boolen if count found == len of date 

        """"

        if len(date) < 6:
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
            

    def upload():
        """
        Function to send data from entry fields to diskAnalyzer. We grab the entry fields' values and strip any whitespace from the front/back
        so that it doesnt mess up with our validation methods. Then we validate the entry fields and upon them returning true, 
        we disable all buttonsand add a status label to let the user know we're sending the inputs. 
        
        Input(s): None
        Output(s) None

        """

        trays = gui.trayEntry.get() .rstrip().lstrip()
        pics = gui.picEntry.get().rstrip().lstrip()
        date = gui.dateEntry.get().rstrip().lstrip()
        if validateTP(trays, pics) and validateDate(date):
            gui.trayEntry.config(state='disabled')      
            gui.picEntry.config(state='disabled')  
            gui.dateEntry.config(state='disabled')    
            # calendarBtn.config(state='disabled')
            uploadBtn.config(state='disabled')
            print(trays)
            print(pics)
            print(date)

            status = tk.Label(root, text="Sending inputs...", bd = 1)
            status.grid(row = 7, column = 1, pady=(70,0))
        return
                
    
    # calendarBtn = tk.Button(root, text="Pick a Date", command=date)
    # calendarBtn.grid(row = 6, column = 1)
    uploadBtn = tk.Button(root, text= "Upload", command=upload)
    uploadBtn.grid(row= 6, column = 0)

    root.mainloop()


