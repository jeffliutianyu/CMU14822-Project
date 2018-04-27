#!/usr/bin python
import sys
import PIL
import tkMessageBox
from Tkinter import *
import Tkinter as tk
from PIL import ImageTk, Image
from tkFileDialog import askopenfilename, askdirectory

#class for file table
class SimpleTable(tk.Frame):
    def __init__(self, parent, rows, columns):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            if row == 0:
                label = tk.Label(self, text="Recoverd Files:", borderwidth=1, fg = 'Blue',
font = "Helvetica 14 bold italic", anchor="w")
                label.grid(row=row, column=0, sticky="nswe")
                label = tk.Label(self, text="", borderwidth=1,fg = 'black',
font = "Helvetica 12 bold italic")
                label.grid(row=row, column=1, sticky="nswe")
                self._widgets.append(current_row)
                continue
            for column in range(columns):
                label = tk.Label(self, text="", borderwidth=1, width=45, fg = 'black',
font = "Helvetica 10 bold italic",bg = 'white')
                label.grid(row=row, column=column, sticky="nswe", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)


# My frame for form
class simpleform_ap(Tk):

    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.parent = parent
        #pathes
        self.disk_image_path = StringVar()
        self.file_type = StringVar()
        self.dir_output_path = StringVar()
        self.input_path = ""
        self.output_path = ""
        self.conf_path = "JPG/GIF/PNG"
        self.conf_filename = "conf/jpg.conf"
        #other options
        self.footer = IntVar() 
        self.database = IntVar()
        self.extension = IntVar()
        self.dashb = 0
        self.dashd = 0
        self.dashn = 0
        self.other_flags = ""
        #text box for commands
        self.entry_text = StringVar()
        self.initialize()
        self.grid()


    #############################GUI Initialization###################################
    def initialize(self):

        #Set GUI's size and title
        self.geometry('1150x900+100+100')
        self.title('ScalGUI v1.0')

        #Filepath of target disk image for recoverty
        label_1 = Label(self, text = "Step 1: Select disk image", fg = 'blue',
font = "Helvetica 14 bold italic").place(x= 5,y = 0) #Label 
        fbutton = Button(self,text='Browse Disk Image',command=self.askopenfile)
        fbutton.config(width = 18)
        fbutton.place( x = 5, y = 30)
        self.disk_image_path.set("Image Path Selected:  None")
        label_DIPath = Label(self, textvariable = self.disk_image_path, fg = 'black',
font = "Helvetica 11 italic bold").place(x= 5,y = 60) #Label

        #OptionMenu for file type
        optionList = ["JPG/GIF/PNG","BMP/TIFF","AVI","MPEG Videos",
"Outlook Files","Microsoft Docs","HTML Files","PDF","ODT", "Other Types"]
        image = Image.open("images/arrow.png")
        image = image.resize((8, 8), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        label_2 = Label(self, text = "Step 2: Select type of files to recover", 
fg = 'blue', font = "Helvetica 14 bold italic").place( x= 5,y = 120) #Label
        filetype = StringVar(self)
        filetype.set("JPG/GIF/PNG") # default value
        w = OptionMenu(self, filetype, *optionList, command=self.filetype_select)
        w.config(indicatoron = 0, compound = 'right', image = self.img, width = 160)
        w.place(x = 5,y = 150)
        self.file_type.set("Conf file selected:  conf/jpg.conf")
        label_FTPath = Label(self, textvariable = self.file_type, fg = 'black',
font = "Helvetica 11 italic bold").place(x= 5,y = 180) #Label    

        #OutputDir for recovered files
        label_3 = Label(self, text = "Step 3: Select directory for recovered files", 
fg = 'blue', font = "Helvetica 14 bold italic").place(x= 5,y = 240) #Label 
        dbutton = Button(self,text='Browse Output Directory',command=self.askopendir)
        dbutton.config(width = 18)
        dbutton.place( x = 5, y = 270)
        self.dir_output_path.set("Output Directory Selected:  None")
        label_ODPath = Label(self, textvariable = self.dir_output_path, fg = 'black',
font = "Helvetica 11 italic bold").place(x= 5,y = 300) #Label  

        #Other Options      
        label_4 = Label(self, text = "Step 4: Other Options", 
fg = 'blue', font = "Helvetica 14 bold italic").place(x= 5,y = 360) #Label 
        #Option 1 - No footer discovered
        footercheck=Checkbutton(self, text="Carve even if defined footers aren't discovered within max carve size",
variable=self.footer, command=self.activatefooter, font = "Helvetica 10 italic")
        footercheck.place(x = 0, y = 390)
        #Option 2 - No footer discovered
        databasecheck=Checkbutton(self, text="Generate Header/Footer Database",
variable=self.database, command=self.activatedatabase, font = "Helvetica 10 italic")
        databasecheck.place(x = 0, y = 410)
        #Option 3 - No footer discovered
        extensioncheck=Checkbutton(self, text="Don't add extensions to extracted files",
variable=self.extension, command=self.activateextension, font = "Helvetica 10 italic")
        extensioncheck.place(x = 0, y = 430)


        #Recover Percentage
        label_5 = Label(self, text = "Progress: 0.0%", fg = 'black', 
font = "Helvetica 14 bold italic").place(rely=1.0, relx=0, x=5, y=-75, anchor=SW) #Label 

        #Text box for commands
        label_5 = Label(self, text = "scalpel commands:", fg = 'black', 
font = "Helvetica 11 bold italic").place(rely=1.0, relx=0, x=5, y=-45, anchor=SW) #Label 
        large_font = ('Verdana',9)
        entry = Entry(self, textvariable=self.entry_text,font=large_font)
        entry.configure(background = "black", width = 95, foreground="white")
        entry.place(rely=1.0, relx=0, x=5, y=-25, anchor=SW)  

        #Recover Button
        rbutton = Button(self,text='Start Recovering',command=self.recover,
font = "Helvetica 14 bold italic")
        rbutton.config(width = 15)
        rbutton.place(rely=1.0, relx=1.0, x=-10, y=-15, anchor=SE) 

        #Table for recovered files
        t = SimpleTable(self, 16, 2)
        t.pack(side="right", fill="x", anchor="n")
        t.set(1,0,"Carved Files (First 15)") 
        t.set(1,1,"MD5 Hash") 


    #############################Event Handlers###################################
    #event handler for disk image selection
    def askopenfile(self):
        filename = askopenfilename() 
        self.input_path = filename
        if len(filename) == 0 : 
           self.disk_image_path.set("Image Path Selected:  None")
        else:
           self.disk_image_path.set("Image Path Selected:  " + filename)
        self.updatecommands()

    #event handler for output directory selection
    def askopendir(self):
        dirname = askdirectory() 
        self.output_path = dirname
        if len(dirname) == 0:
            self.dir_output_path.set("Output Directory Selected:  None")
        else:
            self.dir_output_path.set("Output Directory Selected:  " + dirname)
        self.updatecommands()

    #event handler for option menu 
    def filetype_select(self,value):
        self.file_type.set("Conf file selected:  " + value)
        self.conf_path = value
        if (value == "Other Types"):
            self.file_type.set("Conf file selected:  Please select a configuration file")
            self.conf_filename = askopenfilename()
            if len(self.conf_filename) == 0:
                tkMessageBox.showerror("Error", "No conf file selected!")
                self.file_type.set("Conf file selected:  None")
            else:
                self.file_type.set("Conf file selected:  " + self.conf_filename)
        else:
            self.get_conf_filename()
            self.file_type.set("Conf file selected:  " + self.conf_filename)
        self.updatecommands()

    #conf file name and type mapping
    def get_conf_filename(self):
        choices = {"JPG/GIF/PNG":"conf/jpg.conf","BMP/TIFF":"conf/bmp.conf",
"AVI":"conf/avi.conf", "MPEG Videos":"conf/mpeg.conf", "Outlook Files":"conf/outlook.conf",
"Microsoft Docs":"conf/office.conf","HTML Files":"conf/html.conf","PDF":"conf/pdf.conf",
"ODT":"conf/odt.conf"}
        self.conf_filename = choices.get(self.conf_path,'defult')
 
    #event handler for starting file recovery
    def recover(self):
        if len(self.input_path) == 0:
            tkMessageBox.showerror("Error", "No disk image selected!")
            return
        if len(self.conf_filename) == 0:
            tkMessageBox.showerror("Error", "No conf file selected!")
            return
        if len(self.output_path) == 0:
            tkMessageBox.showerror("Error", "No output directory selected!")
            return
        self.updatecommands()

    #ignore footer
    def activatefooter(self):
        if self.footer.get() == 1:
            self.dashb = 1
        else:
            self.dashb = 0
        self.updatecommands()
    def activatedatabase(self):
        if self.database.get() == 1:
            self.dashd = 1
        else:
            self.dashd = 0
        self.updatecommands()
    def activateextension(self):
        if self.extension.get() == 1:
            self.dashn = 1
        else:
            self.dashn = 0
        self.updatecommands()
    def updateflags(self):
        self.other_flags = ""
        if self.dashb == 1:
            self.other_flags = self.other_flags + " -b"
        if self.dashd == 1:
            self.other_flags = self.other_flags + " -d"
        if self.dashn == 1:
            self.other_flags = self.other_flags + " -n"
    def updatecommands(self):
        self.updateflags()
        commands = "scalpel -c " + self.conf_filename + self.other_flags + " " + self.input_path + " -o " + self.output_path
        self.entry_text.set(commands)



#Create the GUI
def create_form(argv):
    form = simpleform_ap(None)
    form.mainloop()


#Main Funciont
if __name__ == "__main__":
    create_form(sys.argv)
