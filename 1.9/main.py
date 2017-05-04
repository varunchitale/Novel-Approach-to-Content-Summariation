#from tkinter import *
from Tkinter import *
#from Tkinter import messagebox
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
import modelVC
import requests #for reading web data


opTA=""
opPA=""

def freshWindow(): #clear GUI
	ipEntry.delete(1.0, END)
	ipEntry.pack_forget()
	ipLabel.pack_forget()
	opLabel.pack_forget()
	buttonSummary.pack_forget()
	buttonSave.pack_forget()
	buttonSave.pack_forget()
	opEntry.pack_forget()
	redRatio.pack_forget()
	wikiQLabel.pack_forget()
	wSearchEntry.pack_forget()
	buttonWiki.pack_forget()
	buttonWeb.pack_forget()
	opEntry.delete(1.0,END)
	logLabel.pack_forget()

def packIP(): #pack input area
	ipLabel.pack()
	ipEntry.pack()
	buttonSummary.pack()
	ipEntry.delete(1.0, END)

def openLog(): #display Log
		freshWindow()
		logLabel.pack()
		ipEntry.pack()
		ipEntry.delete(1.0,END)
		with open("log.txt") as f:
			ipEntry.insert(INSERT,f.read())
			
			
def evaluate(): #to be done
	count = 0
	stop_words=0
	swFile=open("stopWords.txt").read()
	global opPA,opTA
	
	if len(opPA)<len(opTA):
		for word in opPA:
			if word not in swFile:
				if word in opTA:
					count+=1
			else:
				stop_words+=1
				
	else:
		for word in opTA:
			if word not in swFile:
				if word in opPA:
					count+=1
			else:
				stop_words+=1

	den=float(len(opPA)+len(opTA))/2 - stop_words
	value = ((count)/den)*100
	tkMessageBox.showinfo("Closeness","Similarity of the two algorithms(ignoring stop words) is\n: %.2f percent " %value)
	return 1

def close(): #exit
	res=tkMessageBox.askquestion("Exit", "Are you sure to exit?")
	if res == 'yes':
		exit()
	else:
		freshWindow()

def getFile(): #import text file
	freshWindow()
	packIP()
	filename = tkFileDialog.askopenfilename()
	text1 = open(filename).read()
	ipEntry.insert(INSERT, text1.rstrip(''))

def wikiSearch(): #search wiki
	freshWindow()
	searchTerm = wSearchEntry.get("1.0", END)
	result = wikipedia.page(searchTerm)
	packIP()
	ipEntry.insert(INSERT, result.summary)
	buttonWiki.pack_forget()

def getInput2(): #wikipedia search entry
	freshWindow()
	wikiQLabel.pack()
	wSearchEntry.delete(1.0,END)
	wSearchEntry.pack()
	buttonWiki.pack()

def getPText(): #paste text
	freshWindow()
	packIP()

def getImage(): #open image file
	freshWindow()
	packIP()
	ipEntry.insert(INSERT,"Loading text from image...")
	filename = tkFileDialog.askopenfilename()	
	
	im = Image.open(filename) 
	im = im.filter(ImageFilter.MedianFilter())
	enhancer = ImageEnhance.Contrast(im)	
	im = enhancer.enhance(2)
	im = im.convert('1')
	im.save('temp2.jpeg')
	text = pytesseract.image_to_string(Image.open('temp2.jpeg'))
	text=processText(text)

	ipEntry.delete(1.0, END)
	ipEntry.insert(INSERT, text)

def processText(text):
		text=text.lower()
		text=text.replace("(","c")
		text=text.replace("8","b")
		text=text.replace("0","o")
		return text

def getInput5(): #web search
	freshWindow()
	wikiQLabel.pack()
	wSearchEntry.delete(1.0,END)
	wSearchEntry.pack()
	buttonWeb.pack()
	
def displayWeb(): #paste web search to ip box
	packIP()
	searchTerm = wSearchEntry.get("1.0", END)
	text = requests.get(searchTerm.strip()).text
	#print text	
	ipEntry.insert(INSERT,"Loading...")
	ipEntry.delete(1.0, END)
	ipEntry.insert(INSERT, text.strip())
	buttonWiki.pack_forget()
	
def getSummary(): #actually calculate summary
	opLabel.pack()
	opEntry.pack()
	opEntry.delete(1.0,END)
	opEntry.insert(INSERT,"Generating Summary...")

	startTime = time.time()
	text = ipEntry.get("1.0", END)
	
	ps = PorterStemmer()
	red_ra=redRatio.get()/100.00
	
	if var1.get():
		words = text.split()

		for w in words:
			text += ps.stem(w)
			text += " "
	
	if var6.get()==1:
		r = Reduction() #object of class Red..
		reduced_text = r.reduce(text, red_ra)
		op=' '.join(reduced_text)
		global opTA
		opTA=op
	else:
		m = modelVC.summary()
		op = m.summarize(text,red_ra)
		global opPA
		opPA=op

	if var2.get()==1:
		op=shortForm.shortF(op)

	opEntry.delete(1.0,END)
	opEntry.insert(INSERT, op)

	endTime = time.time() - startTime
	if var4.get():
		tkMessageBox.showinfo("Statistics", "Time taken to complete: %f secs" %endTime)
	print("Time taken: %f secs" %endTime)

	if var3.get() == 1:
		file_f == open("log.txt", "a")
		lenText=len(text)
		file_f.write("\nInput length: %d" %lenText)
		lenText = len(op)
		file_f.write("\tSummary length: %d" % lenText)
		file_f.write('\nStemming: %d' %var1.get())
		file_f.write('\tShort Forms: %d' %var2.get())
		file_f.write('\tReduction Ratio: %d percent' % redRatio.get())
		file_f.write('\tModel: %d ' % var6.get())
		file_f.write("\nTime taken: %f secs\n" %endTime)
		file_f.close()

def getRR(): #set RR
	opLabel.pack_forget()
	opEntry.pack_forget()
	buttonSummary.pack_forget()
	redRatio.pack()
	buttonSummary.pack()

def updateSW(): #stopWords.txt editing
	with open("stopWords.txt", 'w+') as f:
		text=ipEntry.get("1.0", END)
		f.write(text)
		f.close()

def showSW(): #display Stop Words in ip box
	buttonSummary.pack_forget()
	ipEntry.pack()
	with open("stopWords.txt") as f:
		ipEntry.delete(1.0, END)
		text=f.read()
		ipEntry.insert(INSERT,text)
		buttonSave.pack()
		f.close()

def showSF(): #to be done
	return 1

def showHelp():
	tkMessageBox.showinfo("Help", "Instructions:\n"
								"1. Select input method. \n2. Select reduction ratio(% summary for text)\n 3."
								"Generate Summary.")

def contact():
	tkMessageBox.showinfo("About us", "All rights reserved\nUse of application comes with no guarantee."
									"\nInfo at: https://github.com/varunchitale")


#Main GUI begins
root = Tk()

root.title("Content Summary Generator")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
x = (width / 2) - (800 / 2)
y = (height / 2) - (650 / 2)
root.resizable(width=False, height=False)
root.geometry('%dx%d+%d+%d' % (800, 600, x, y))

#Menu Bar with all its elements
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
sourceMenu.add_command(label="Import text file", command=getFile)
wSearchEntry=Text(root)
sourceMenu.add_separator()
sourceMenu.add_command(label="Web Search", command=getInput5)
sourceMenu.add_command(label="Wikipedia Search", command=getInput2)
sourceMenu.add_separator()
sourceMenu.add_command(label="Paste Text", command=getPText)
sourceMenu.add_command(label="Read image(JPG/JPEG)*", command=getImage)

var1 = IntVar() #stem
var2 = IntVar() #SF
var3 = IntVar(value=1) #log
var4 = IntVar() #time display
var5 = IntVar() #conc
var6 = IntVar(value=2) #textRank #personal algo
prefMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Preferences", menu=prefMenu)
prefMenu.add_radiobutton(label="Text Rank Algorithm", var=var6, value=1)
prefMenu.add_radiobutton(label="Personal Algorithm", var=var6, value=2)
prefMenu.add_separator()
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
#Menu Bar ends

#define elements
redRatio = Scale(root, from_=1, to=99, length=300, orient=HORIZONTAL)
redRatio.set(20)
logLabel = Label(root, text="Log: ")
ipLabel = Label(root, text="Input Text: ")
ipEntry = Text(root, wrap=WORD, width=80, height=15)
opEntry = Text(root, wrap=WORD, width=80, height=15)
wSearchEntry= Text(root, width=80, height=1)
wikiQLabel = Label(root, text="Enter Search Query")
buttonWiki = Button(root, text="Search", command=wikiSearch)
buttonWeb = Button(root, text="Search", command=displayWeb)
buttonSummary = Button(root, height=2, width=15, text="Generate Summary", command=getSummary)
buttonSave = Button(root,text="Save to File", command= updateSW)
opLabel = Label(root, text="Summary: ")
#end of definitions

root.config(menu=menubar)

root.mainloop()
