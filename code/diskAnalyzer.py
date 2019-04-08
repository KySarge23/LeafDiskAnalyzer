#!/usr/bin/env python3

#Imports for functionalities
import math
import cv2 as cv
import numpy as np
import matplotlib.image as mpimg
import tkinter as tk
import os
import threading as thr
import time
import imghdr
import sys
import glob
import openpyxl, openpyxl.styles

#GUI Imports
import GUI
import calendarPicker as cp

#Specific functionality imports
from pathlib import Path as pth
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from matplotlib import pyplot as plt

#Author(s): Kyle Sargent, Erica Gitlin, Connor Jansen, Colton Eddy, Alex Wilson, Emily Box
#Version: 1


thrLock = thr.Lock()

def writeToExcel(value, workbookName, sheet, date):

    """
    This function will handle any writing to the spreadsheet document that is required.
    It uses openpyxl to load in a workbook and write the data obtained from the analysis to spreadsheets in selected workbooks.

    Input(s): value, workbookName, sheet, data
    Output(s): Data written to sheet in workbook
    Local Variable(s):  wb (excel workbook that is opened), ws (worksheet from opened workbook), startCol/startRow (int), 
    
    """

    wb = openpyxl.load_workbook(workbookName)
    ws = wb[sheet]
    startCol, startRow = 1, 1
    dateCol, dateRow = 0, 0

    if date not in ws.values:
        if ws.cell(startRow,startCol).value == None:
            dateCell = ws.cell(row = startRow, column = startCol, value = date)
            dateCell.alignment = openpyxl.styles.Alignment(horizontal = 'center', vertical = 'center')
            dateCol = startCol
            dateRow = startRow
            ws.merge_cells(dateCell.coordinate + ':' + ws.cell(dateRow, dateCol + 3).coordinate)
            wb.save(workbookName)

        else:
            for i in range(startCol, 25, 10):
                if ws.cell(row = startRow, column = i).value != None:
                    continue
                else: 
                    dateCell = ws.cell(row = startRow, column = i, value = date)
                    dateCell.alignment = openpyxl.styles.Alignment(horizontal = 'center', vertical = 'center')
                    dateCol = i
                    dateRow = startRow
                    ws.merge_cells(dateCell.coordinate + ':' + ws.cell(dateRow, dateCol + 3).coordinate)
                    wb.save(workbookName)
                    break

        ratioRow = dateRow + 1
        ratioCol = dateCol + 1

        for i in range(ratioRow, 27): #limit to 25 runs for now
            for j in range(ratioCol,27): #limit to 25 runs for now
                if ws.cell(ratioRow , ratioCol).value != None:
                    continue
                else:
                    ratioCell = ws.cell(ratioRow , ratioCol, value = str(value) + "%")
                    ratioCell.number_format = "0.00%"
                    wb.save(workbookName)
                    return
    wb.save(workbookName)
    return




def calculateMildew(path):

    """Area finding function, Will utilize HoughCircle method to detect circles
       within the photo or hard coded method to detect circles . Then will use that circle to find the area within it which
       is what will be used later in the edge detection"""

    img = cv.imread(path,0) #read in as Grayscale
    img = cv.resize(img,(423,280)) #resize image, for easier reading and faster execution.
    img = cv.medianBlur(img,5) #add blur to reduce noise on photo.
    cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR) #convert back to BGR scale for the drawn circle to show up as whatever color specified.
    """The following lines can be used to have an algorithm detect circles for us.
       or can use the hard-coded version that is commented out below"""

    #params are as follows: (image, method = cv.HOUGH_GRADIENT is the only one that works
    #thus far, dp, minDist, parap1 = gradient value,
    #param2 = accumulator threshold value for method input, minRadius, maxRadius)
    #for more details on HoughCircles, visit: http://www.bmva.org/bmvc/1989/avc-89-029.pdf or https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/

    """This is how the Hough Transformation works for circles:

        1. First, we create the accumulator(a two dimensional array) space, which is made up of a cell for each pixel.
           Initially each cell is set to 0.
        2. For each edge point (i, j) in the image, increment all cells which according to the equation of a circle (i-a)^{2}+(j-b)^{2}=r^{2}
           could be the center of a circle. 
           These cells are represented by th    e letter a in the equation.
        3. For each possible value of  a fou    nd in the previous step, find all possible values of b which satisfy the equation.
        4. Search for local maxima in the ac    cumulator space. These cells represent circles that were detected by the algorithm.

        If we do not know the radius of the circle we are trying to locate beforehand,
        we can use a three-dimensional accumulator space to search for circles with an arbitrary radius.
        Naturally, this is more computationally expensive.
        This method can also detect circles that are partially outside of the accumulator space, as long as enough of the circle's area is still present within it. """


    #circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,200,
                                        #param1=50,param2=30,minRadius=0,maxRadius=0)

    #circles = np.uint8(np.around(circles))

    #for circ in circles[0,:]:
        #draw the detected outer circle
        #params are as follows: (image, center coords, radius, bgr values, thickness)
     #   cv.circle(cimg,(circ[0],circ[1]),circ[2],(0,255,0),2) #this is the only circle drawn
      #  rad = circ[2] #grab the radius


    """The following lines can be used to hard-code in the circle
       or can use above to use an algorithm to detect the circle"""

    h,w = img.shape[:2]
    print("height is: " + str(h))
    print("width is: " + str(w))


    center = (int(w / 2), int(h / 2))
    rad = 200
    cv.circle(cimg, center, rad, (0,0,255), 2)


    area = math.pi * rad ** 2 #calculate the area of the circle detected in pixels
    # print("Area of circle drawn is: " + str(int(area))+"px\n")

    # cimg = cimg[0:h, 30:w-30]
    # cv.imshow(x ,cimg)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    # cv.imwrite("crop.png" , cimg)

    print("Edge Detection Starting")

    #second param: (1= color, 0= grayscale, -1 = unchanged)
    #however OCV uses BGR coloring and Matplot uses RGB coloring, so
    #when reading in with OCV, need to change to RGB if showing with matplot
    #if we want pictures to show up in RGB correctly colored.
    #notice when matplot pops up, color is distorted.
    #Reading of the same photo, in color for displaying and grayscale for edgeDetection.
    #imgC = cv.imread(x,1)


    #cv.imshow('Original', img)

    #Converting img to RGB:
    #imgC = cv.cvtColor(imgC, cv.COLOR_BGR2RGB)

    #use canny algorithm for edge detection
    #see https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
    #for more details.
    edges = cv.Canny(img,120,200)
    #Save image into photos folder for now. so can be used in analyzeDisks method
    print("Edge Detection Complete")

    #we now set a threshold using cv.threshhold. This will help to detect possible
    #contours that are greater than the value (127,255,0), a color which was detected
    #on the leaf that is dark green. This is the baseline color. Essentially this is
    #the normal color of the image.
    ret, edges = cv.threshold(edges,130,255,cv.ADAPTIVE_THRESH_MEAN_C)
    mask = np.zeros(edges.shape,np.uint8)
    #we must now find the contours. We apply the findContours using our threshold value.
    #we want the contours as a list not as a tree. The next parameter is extremely important
    #this is the method of approximating the contours. The Chain Approximation finds contours
    #that are relatively the same intensity and throws out redundant points
    contours, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    #we create a local variable called total_area. We then loop through all contours and add the area to the
    #running total. We return the int value in pixels.

    mildewRatio = 0
    for cont in contours:
        contArea = cv.contourArea(cont)
        mildewRatio += contArea

    return mildewRatio / area * 100


def threadHandler(date, trayNum, picNum, spreadsheet):
    """
    This Function accepts the three user inputs from the main function/GUI as arguments.
    It then builds a valid filepath based on the arguments. Once a valid path is created,
    this function sends that path to the findCircleArea and cannyEdgeDetection functions. 
    This function validates the file extension of the file selected to make sure that the selection is a valid image format.
    Supported file extensions: .png, .jpeg, .jpg, .tiff, .tif

    Input(s): date (String) , tray (int), picNum (int)
    Output(s): None
    Local Variable(s): path (String), dirName (String) , fName (String), circArea (int), mildewRatio (int), mildewRatio (int)

    """
    print(thr.current_thread())


    date = glob.glob("../photos/"+ date + "*", recursive=True)[0]
    tray = 'tray '+ str(trayNum)
    dirName = date + "/" + tray + "/"
    fName = str(picNum) + "-160x271_" + str(picNum)


    path = os.path.abspath(dirName + fName)

    if os.path.exists(path + ".png"): #validate the path
            path = path + ".png"
            mildewRatio = calculateMildew(path)
            thrLock.acquire()
            writeToExcel(mildewRatio, spreadsheet, tray, date[10:])
            thrLock.release()
            return print("Mildew to leaf ratio is: " + str(mildewRatio) + "%")

    elif os.path.exists(path + ".jpeg"): #validate the path
            path = path + ".jpeg"
            mildewRatio = calculateMildew(path)
            thrLock.acquire()
            writeToExcel(mildewRatio, spreadsheet, tray, date[10:])
            thrLock.release()
            return print("Mildew to leaf ratio is: " + str(mildewRatio) + "%")

    elif os.path.exists(path + ".jpg"): #validate the path
            path = path + ".jpg"
            mildewRatio = calculateMildew(path)
            thrLock.acquire()
            writeToExcel(mildewRatio, spreadsheet, tray, date[10:])
            thrLock.release()
            return print("Mildew to leaf ratio is: " + str(mildewRatio) + "%")
   
    elif os.path.exists(path + ".tiff"): #validate the path
            path = path + ".tiff"
            mildewRatio = calculateMildew(path)
            thrLock.acquire()
            writeToExcel(mildewRatio, spreadsheet, tray, date[10:])
            thrLock.release()
            return print("Mildew to leaf ratio is: " + str(mildewRatio) + "%")

    elif os.path.exists(path + ".tif"): #validate the path
            path = path + ".tif"
            mildewRatio = calculateMildew(path)
            thrLock.acquire()
            writeToExcel(mildewRatio, spreadsheet, tray, date[10:])
            thrLock.release()
            return print("Mildew to leaf ratio is: " + str(mildewRatio) + "%")
            
    else: #let user know the software has detected an invalid path
            print("Invalid path detected, No file or directory resides in: \n" + path)


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
        
def date():
    cp.DatePicker(format_str='%01d-%02d-%s')

def main():
    
    root = tk.Tk()
    #the size of the window
    root.geometry('350x300')
    root.title("LDA GUI v1.0")
    gui = GUI.analyzerGUI(root) #create new instance of the analyzerGUI with root as master.

    trays, pics, threads = [], [], []
    workbook = ""

    # following lines uncomment if want to use calendarPicker.py 

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
        as dd-mm-yy as well. Otherwise we check for digits and the '-' character if anything else is found, 
        then we warn the user about the found character and then clear the entry field for retrying.
        
        Input(s): date (String)
        Output(s): boolean if count found == len of date 
        Local Variable(s): count (int) , dashes (list of indicies), numCount (int)

        """

        if date == "":
            messagebox.showwarning("No Entry Warning!", "No entry found in Date entry. Please enter a date in the following format: 'mm-dd-yy'.")
            return False

        elif len(date) < 6 or len(date) > 8 :
            messagebox.showwarning("Date Warning!", "Date entered has too many or too little characters. Please enter a date in the following format: 'mm-dd-yy'.")
            gui.dateEntry.delete(0,tk.END)
            return False
        else:
            dashes = findOccurrences(date, '-')
            numCount = 0
            s1 = date[0:dashes[1]]
            s2 = date[dashes[1]:]
            s1 = s1.split('-')
            s2 = s2.split('-')

            for str in s1 and s2:
                if len(str) > 2:
                    messagebox.showwarning("Incorrect Date Warning!", "An incorrect date of: "+ date +" has been found. Please enter a date in the following format: 'mm-dd-yy'.")
                    gui.dateEntry.delete(0, tk.END)
                    return False

            count = 0
            for i in date:
                if i.isdigit() or i == '-':
                    count+=1
                else:
                    messagebox.showwarning("Incorrect Character Warning!", "Incorrect character of: " + i +" has been found. Only use the following characters: '-'.")
                    return False

            if count == len(date):
                return True

    def newOrExisting(trays):
        """
        Function for determining whether a new spreadsheet or an existing spreadsheet will be used to hold data from the analyzing process.
        We get the option selected from the radio buttons on the GUI and return True if one was selected, otherwise we show a 
        messagebox warning letting the user know neither button was picked, and return false

        Input(s): trays (list of trays gained from user input)
        Output(s): True or False Boolean
        Local Variable(s): value (String), new (Boolean)

        """
        value = gui.option.get()
        if value == "True":
                print("Creating new Spread Sheet")
                wb = openpyxl.Workbook()
                rm = wb['Sheet']
                wb.remove(rm)

                for tray in trays:
                    ws = wb.create_sheet("tray " + str(tray))
                
                file = asksaveasfilename(initialdir = ".",title = "Save As",filetypes = (("xlsx","*.xlsx"),("All Files","*.*"))) + ".xlsx" #creates new workbook (currently creates a single placeholder book in the current directory               
                wb.save(file)
                return file

        elif value == "False":
                print("Going to Existing")
                file = askopenfilename(initialdir = ".", title = "Open File", filetypes = (("xlsx","*.xlsx"),("All Files","*.*"))) #lets user browse for what spreadsheet they want to open
                wb = openpyxl.load_workbook(file)
                wsheets = wb.sheetnames
                for tray in trays:
                    if "tray " + str(tray) not in wsheets:
                        ws = wb.create_sheet("tray " + str(tray))

                wb.save(file)
                return file

    def sendToAnalyzer():
        """
        Function to send data from entry fields to diskAnalyzer. We grab the entry fields' values and strip any 
        whitespace from the front/back so that it doesnt mess up with our validation methods. 
        Then we validate the entry fields and upon them returning true, 
        we disable all buttons and then run the analyzer methods with the validated data gained from the GUI.
        
        Input(s): None
        Output(s) None
        Local Varaible(s): None

        """

        trayStr = gui.trayEntry.get().rstrip().lstrip()
        picStr = gui.picEntry.get().rstrip().lstrip()
        dateStr = gui.dateEntry.get().rstrip().lstrip()

        if validateTP(trayStr, picStr) and validateDate(dateStr):
            trays = getNumbers(trayStr)
            pics = getNumbers(picStr)
            workbook = newOrExisting(trays)

            if workbook == ".xlsx": #saving the workbook filename is cancelled, file will become ".xlsx" and still create a spreadsheet and run the analyzing. This will prevent that.
                os.remove(workbook) 
                return messagebox.showwarning("No Save/Existing Spreadsheet Name Warning!", "No name has been selected for the spreadsheet you wish to use. Please retry.")

            numTrays = len(trays)
            numPics = len(pics)

            if numPics * numTrays > 8:
                return messagebox.showwarning("Input Warning!", "Current inputs from Tray/Picture entry fields will spawn too many threads. Use the following as a guide for entering data into tray/pictures entry fields: trays * pictures <= 8.")
            
        
            for i in range(len(trays)):
                for j in range(len(pics)): 
                    t = thr.Thread(target = threadHandler, args = [dateStr, trays[i], pics[j], workbook])
                    threads.append(t)
                    t.start()
            
            for  t in threads:
                t.join()
 
        return
                
    uploadBtn = tk.Button(root, text= "Analyze", command=sendToAnalyzer, height = 1, width = 10)
    uploadBtn.grid(row= 5, column = 0)    
    calendarBtn = tk.Button(root, text="Pick a Date", command=date)
    calendarBtn.grid(row = 3, column = 1, pady = (0,60))

    root.mainloop()




main()
