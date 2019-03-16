#!/usr/bin/python3
from tkinter import *
from tkinter import messagebox

#Author(s): Erica Gitlin, Colton Eddy

class App(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        self.grid(column=4, row=6)
        self.create_gui()




    def create_gui(self):

        #label for tray number
        self.label = Label(self, text="tray Number(s)")
        self.label.grid(column = 1, row = 2)

        #labels for date

        dayLabel = Label(self, text="Day")
        dayLabel.grid(column = 1, row = 4)

        monthLabel = Label(self, text="Month")
        monthLabel.grid(column = 2, row = 4)

        yearLabel = Label(self, text="Year")
        yearLabel.grid(column = 3, row = 4)

        #entry for date

        dayEntry = Entry(self, bd = 5)
        dayEntry.grid(column = 1, row = 5)

        monthEntry = Entry(self, bd = 5)
        monthEntry.grid(column = 2, row = 5)

        yearEntry = Entry(self, bd = 5)
        yearEntry.grid(column = 3, row = 5)

        #submit function for form
        def submit():
            if (dayEntry.get().isdigit() == False):
                messagebox.showerror("Input Error", "Please only use numbers for inputting the day.")
            elif (monthEntry.get().isdigit() == False):
                messagebox.showerror("Input Error", "Please only use numbers for inputting the month.")
            elif (yearEntry.get().isdigit() == False):
                messagebox.showerror("Input Error", "Please only use numbers for inputting the year.")
            else:
                print(dayEntry.get() + "/" + monthEntry.get() + "/" + yearEntry.get())

        #submit button for form
        submitButton = Button(self, text = "Submit", width=10, command=submit)
        submitButton.grid(column = 4, row = 6)

    


        




        

        
#initializing the root window
root = Tk()
root.title("Leaf Disk Analyzer")
#the size of the window
root.geometry('600x600')


app=App(root)

#a blank canvas for our GUI
c = Canvas(root, height=600, width=600)






<<<<<<< HEAD
root.mainloop()
=======
root.mainloop()
>>>>>>> 25a2d01a72ca68b7148c41fb87601394533a4816
