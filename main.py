#!/usr/bin python
import sys
import PIL
from Tkinter import *
from PIL import ImageTk, Image
from tkFileDialog import askopenfilename, askdirectory


# My frame for form
class simpleform_ap(Tk):

    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.disk_image_path = StringVar()
        self.file_type = StringVar()
        self.dir_output_path = StringVar()
        self.input_path = ""
        self.output_path = ""
        self.conf_path = ""
        self.initialize()
        self.grid()


    #############################GUI Initialization###################################
    def initialize(self):

        #Set GUI's size and title
        self.geometry('750x650+200+100')
        self.title('ScalGUI v1.0')

        #Filepath of target disk image for recoverty
        label_1 = Label(self, text = "Step 1: Select disk image", fg = 'blue',
font = "Helvetica 14 bold italic").place(x= 5,y = 10) #Label 
        fbutton = Button(self,text='Browse an Disk Image',command=self.askopenfile)
        fbutton.config(width = 15)
        fbutton.place( x = 5, y = 40)
        self.disk_image_path.set("Image Path Selected:  None")
        label_DIPath = Label(self, textvariable = self.disk_image_path, fg = 'black',
            font = "Helvetica 11 italic bold").place(x= 5,y = 70) #Label

        #OptionMenu for file type
        optionList = ["JPG/GIF/PNG","BMP/TIFF","AVI","MPEG Videos",
"Outlook Files","Microsoft Docs","HTML Files","PDF","ODT", "Other Types"]
        image = Image.open("images/arrow.png")
        image = image.resize((8, 8), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        label_2 = Label(self, text = "Step 2: Select type of files to recover", 
fg = 'blue', font = "Helvetica 14 bold italic").place( x= 5,y = 130) #Label
        filetype = StringVar(self)
        filetype.set("JPG/GIF/PNG") # default value
        w = OptionMenu(self, filetype, *optionList, command=self.filetype_select)
        w.config(indicatoron = 0, compound = 'right', image = self.img, width = 120)
        w.place(x = 5,y = 160)
        self.file_type.set("File Type Selected:  None")
        label_FTPath = Label(self, textvariable = self.file_type, fg = 'black',
            font = "Helvetica 11 italic bold").place(x= 5,y = 190) #Label    

        #OutputDir for recovered files
        label_3 = Label(self, text = "Step 3: Select directory for recovered files", 
fg = 'blue', font = "Helvetica 14 bold italic").place(x= 5,y = 250) #Label 
        dbutton = Button(self,text='Browse an Directory',command=self.askopendir)
        dbutton.config(width = 15)
        dbutton.place( x = 5, y = 280)
        self.dir_output_path.set("Output Directory Selected:  None")
        label_ODPath = Label(self, textvariable = self.dir_output_path, fg = 'black',
            font = "Helvetica 11 italic bold").place(x= 5,y = 310) #Label  

        #Other Options      
        label_4 = Label(self, text = "Step 4: Other Options", 
fg = 'blue', font = "Helvetica 14 bold italic").place(x= 5,y = 370) #Label 

        #Recover Button
        rbutton = Button(self,text='Start Recovering',command=self.recover,font = "Helvetica 14 bold italic")
        rbutton.config(width = 15)
        rbutton.place(rely=1.0, relx=1.0, x=-10, y=-15, anchor=SE)  


    #############################Event Handlers###################################
    #event handler for disk image selection
    def askopenfile(self):
        filename = askopenfilename() 
        self.disk_image_path.set("Image Path Selected:  " + filename)
        self.input_path = filename

    #event handler for output directory selection
    def askopendir(self):
        dirname = askdirectory() 
        self.dir_output_path.set("Output Directory Selected:  " + dirname)
        self.output_path = dirname

    #event handler for option menu 
    def filetype_select(self,value):
        self.file_type.set("File Type Selected:  " + value)
        self.conf_path = value

    #event handler for starting file recovery
    def recover(self):
        if len(self.conf_path) == 0:
            print("Error: unable to find configuration file")
        if len(self.input_path) == 0:
            print("Error: unable to find input disk image")
        if len(self.output_path) == 0:
            print("Error: unable to locate output directory")

    	scalpel_commands = "scalpel -c " + self.conf_path + " " + self.input_path + " -o " + self.output_path
        print(scalpel_commands)



#Create the GUI
def create_form(argv):
    form = simpleform_ap(None)
    form.mainloop()


if __name__ == "__main__":
    create_form(sys.argv)
