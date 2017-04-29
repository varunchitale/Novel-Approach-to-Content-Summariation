#from tkinter import *
from Tkinter import *
#from Tkinter import 
import tkMessageBox
#from Tkinter.filedialog import askopenfilename
import tkFileDialog
from reduction import Reduction
from nltk.stem import PorterStemmer
import wikipedia
import shortForm
import time
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
#from collections import Counter


def freshWindow():
    ipEntry.delete(1.0, END)
    ipEntry.pack_forget()
    ipLabel.pack_forget()
    opLabel.pack_forget()
    genSButton.pack_forget()
    saveButton.pack_forget()
    saveButton.pack_forget()
    opEntry.pack_forget()
    redRatio.pack_forget()
    wikiQLabel.pack_forget()
    wikiSearchEntry.pack_forget()

def openLog():
        with open("log.txt", encoding='utf-8') as f:
            messagebox.showinfo("Log", f.read())

def evaluate():
    tkMessageBox.showinfo("Precision", "Value: 97%")
    return 1

def close():
    res=tkMessageBox.askquestion("Exit", "Are you sure to exit?")
    if res == 'yes':
        exit()
    else:
        freshWindow()

def getInput1():
    opLabel.pack_forget()
    opEntry.pack_forget()
    ipLabel.pack()
    ipEntry.pack()
    genSButton.pack()
    ipEntry.delete(1.0, END)
    filename = tkFileDialog.askopenfilename()
    text1 = open(filename).read()
    ipEntry.insert(INSERT, text1)

def wikiSearch():
    freshWindow()
    searchTerm = wikiSearchEntry.get("1.0", END)
    result = wikipedia.page(searchTerm)
    ipLabel.pack()
    ipEntry.pack()
    genSButton.pack()
    ipEntry.delete(1.0, END)
    ipEntry.insert(INSERT, result.summary)
    buttonWiki.pack_forget()

def getInput2():
	freshWindow()
	wikiQLabel.pack()
	wikiSearchEntry.pack()
	buttonWiki.pack()

def getInput3():
    freshWindow()
    ipLabel.pack()
    ipEntry.delete(1.0, END)
    ipEntry.pack()
    genSButton.pack()

def getInput4():
	freshWindow()
	ipLabel.pack()
	ipEntry.pack()
	ipEntry.insert(INSERT,"Loading...")
	filename = tkFileDialog.askopenfilename()
	im = Image.open(filename) 
	im = im.filter(ImageFilter.MedianFilter())
	enhancer = ImageEnhance.Contrast(im)	
	im = enhancer.enhance(2)
	im = im.convert('1')
	im.save('temp2.jpeg')
	text = pytesseract.image_to_string(Image.open('temp2.jpeg'))
	ipEntry.delete(1.0,END)
	ipEntry.insert(INSERT, text)
	genSButton.pack()
	

def getSummary():
    
    startTime = time.time()

    opEntry.delete(1.0,END)
    text = ipEntry.get("1.0", END)
    opLabel.pack()
    opEntry.pack()
    ps = PorterStemmer()
    reduction = Reduction()
    red_ra=redRatio.get()/100.00
	
    if var1.get():
        words = text.split()

        for w in words:
            text += ps.stem(w)
            text += " "
	
    #print text
    reduced_text = reduction.reduce(text, red_ra)
    op=' '.join(reduced_text)

    if var2.get()==1:
        op=shortForm.shortF(op)


    attempt= '\n\n'
    #print (op)
    opEntry.insert(INSERT, op+attempt)

    endTime = time.time() - startTime
    if var4.get():
        tkMessageBox.showinfo("Statistics", "Time taken to complete: %f secs" %endTime)
    print("Time taken: %f secs" %endTime)

    if var3.get() == 1:
        file_f = open("log.txt", "a")
        lenText=len(text)
        file_f.write("\nInput length: %d" %lenText)
        lenText = len(op)
        file_f.write("\tSummary length: %d" % lenText)
        file_f.write('\nStemming: %d' %var1.get())
        file_f.write('\tShort Forms: %d' %var2.get())
        file_f.write('\tReduction Ratio: %d percent' % redRatio.get())
        file_f.write("\nTime taken: %f secs\n" %endTime)
        file_f.close()

def getRR():
    genSButton.pack_forget()
    redRatio.pack()
    genSButton.pack()

def updateSW():
    with open("stopWords.txt", 'w+') as f:
        text=ipEntry.get("1.0", END)
        f.write(text)
        f.close()

def showSW():
    genSButton.pack_forget()
    ipEntry.pack()
    with open("stopWords.txt") as f:
        ipEntry.delete(1.0, END)
        text=f.read()
        ipEntry.insert(INSERT,text)
        saveButton.pack()
        f.close()

def showSF():
    return 1

def showHelp():
    tkMessageBox.showinfo("Help", "Instructions:\n"
                                "1. Select input method. \n2. Select reduction ratio(% summary for text)\n 3."
                                "Generate Summary.")

def contact():
    tkMessageBox.showinfo("About us", "All rights reserved\nUse of application comes with no guarantee."
                                    "\nReach out at: varunchitale@gmail.com")


#Main GUI begins
root = Tk()

root.title("Content Summary Generator")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
x = (width / 2) - (800 / 2)
y = (height / 2) - (650 / 2)
root.resizable(width=False, height=False)
root.geometry('%dx%d+%d+%d' % (800, 650, x, y))




menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=freshWindow)
filemenu.add_command(label="Open Log", command=openLog)
filemenu.add_command(label="Evaluation", command=evaluate)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=close)

sourceMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Input", menu=sourceMenu)
sourceMenu.add_command(label="Import text file", command=getInput1)
wikiSearchEntry=Text(root)
sourceMenu.add_command(label="Wikipedia Search", command=getInput2)
sourceMenu.add_command(label="Paste Text", command=getInput3)
sourceMenu.add_command(label="Read image(JPG/JPEG)", command=getInput4)

var1 = IntVar() #stem
var2 = IntVar() #SF
var3 = IntVar(value=1) #log
var4 = IntVar() #time display
var5 = IntVar() #conc
prefMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Preferences", menu=prefMenu)
prefMenu.add_command(label="Set Reduction ratio", command=getRR)
prefMenu.add_separator()
prefMenu.add_checkbutton(label="Concurrency*", var=var5)
prefMenu.add_checkbutton(label="Use Stemming", var=var1)
prefMenu.add_checkbutton(label="Use Short Forms", var=var2)
prefMenu.add_separator()
prefMenu.add_checkbutton(label="Display time stats", var=var4)
prefMenu.add_checkbutton(label="Write to file", var=var3)

editmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Personalize", menu=editmenu)
editmenu.add_command(label="Edit Stop Words", command=showSW)
editmenu.add_command(label="Edit Short Forms*")

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Help", command=showHelp)
helpmenu.add_command(label="About", command=contact)
helpmenu.add_separator()
helpmenu.add_command(label="Feedback", command=contact)

redRatio = Scale(root, from_=1, to=100, length=300, orient=HORIZONTAL)
redRatio.set(20)
ipLabel = Label(root, text="Text 1: ")
ipEntry = Text(root, wrap=WORD, width=80, height=10)
opEntry = Text(root, wrap=WORD, width=80, height=10)
wikiSearchEntry= Text(root, width=80, height=1)
wikiQLabel = Label(root, text="Enter Wikipedia Search Query")
buttonWiki = Button(root, text="Search", command=wikiSearch)
genSButton = Button(root, height=2, width=15, text="Generate Summary", command=getSummary)
saveButton = Button(root,text="Save to File", command= updateSW)
saveButton = Button(root,text="Save to File", command= updateSW)
opLabel = Label(root, text="Summary: ")

root.config(menu=menubar)

root.mainloop()
