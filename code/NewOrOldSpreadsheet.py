from tkinter import *

#Author:Emily Box

#the variable "new" is the boolean value
#true = new spread sheet,false = existing

def validate():
    value = option.get()
    if value == "True":
        print("Creating new Spread Sheet")
        new = True;
        print(new);
    elif value == "False":
        print("Going to Existing")
        new = False;
        print(new);
    else:
        print("An option must be selected")

root = Tk()
root.geometry("400x400")

option = StringVar()
R1 = Radiobutton(root, text="New Spread Sheet", value="True", var=option)
R2 = Radiobutton(root, text="Existing Spread Sheet", value="False", var=option)
button = Button(root, text="OK", command=validate)

R1.pack()
R2.pack()
button.pack()

root.mainloop()
