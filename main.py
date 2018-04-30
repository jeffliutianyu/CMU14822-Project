#!/usr/bin python
import sys
import PIL
import tkMessageBox
from Tkinter import *
import Tkinter as tk
from PIL import ImageTk, Image
from tkFileDialog import askopenfilename, askdirectory
from pwn import *
import time
import string
import os
import fnmatch
import psutil

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
                label = tk.Label(self, text="", borderwidth=1, width=40, fg = 'black',
font = "Arial 10",bg = 'white',anchor=W)
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
        self.percentage = StringVar()
        self.num_files_recovered = StringVar()
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
        self.commands_to_execute = ""
        self.t = SimpleTable(self, 32, 2)
        self.initialize()
        self.grid()
        self.pss = 0
        # the scalpel command received from GUI
        self.cmd = ""
        # status of executing the command
        # -1: command itself constructed with errors
        # 0: command executed correctly
        # 1: command executed with error
        self.status = -2
        # Scalpel version
        self.version = ""
        # Author Informaiton
        self.authorInfo = ""
        # Images to be carved
        self.target = ""

        ##### TODO, multiple images support #####

        # percentage info for allocation, contains two float numbers:
        # 1, percentage info as NUM, such as 4.9 %
        # 2, bytes carved as NUM, such as 10.0 MB
        self.allocating_queue = ["", ""]
        # Carving signature list, contains four strings:
        # 1, type of carving files, such as "gif", "jpg"
        # 2, header, such as "\x47\x49\x46\x38\x37\x61"
        # 3, footer, such as "\x00\x3b"
        # 4, number of files carved for this signature, such as "20" files
        self.carving_list = []
        # percentage info for processing of images, contains two float numbers:
        # 1, percentage info as NUM, such as 48.8 %
        # 2, bytes carved as NUM, such as 100.0 MB
        self.image_processing = ["", ""]

        ##### TODO                          #####

        # Total number of file carved
        self.num_file_carving = -1
        # Total time consumed
        self.time_consumed = -1
        # Error informaiton if occured
        self.error_info = ""
        # MD5 list of all carved files
        self.md5list = {}




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
        self.percentage.set("Progress: 0.0% processed, 0 MB carved")
        label_5 = Label(self, textvariable = self.percentage, fg = 'black', 
font = "Helvetica 14 bold italic").place(rely=1.0, relx=0, x=5, y=-105, anchor=SW)
        self.num_files_recovered.set("Number of files recovered: 0")
        label_6 = Label(self, textvariable = self.num_files_recovered , fg = 'black',
font = "Helvetica 14 bold italic").place(rely=1.0, relx=0, x=5, y=-75, anchor=SW)

        #Text box for commands
        label_7 = Label(self, text = "scalpel commands:", fg = 'black', 
font = "Helvetica 12 bold italic").place(rely=1.0, relx=0, x=5, y=-45, anchor=SW) #Label 
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
        self.t.pack(side="right", fill="x", anchor="n")
        self.t.set(1,0,"Carved Files (First 30 Files)") 
        self.t.set(1,1,"MD5 Hash") 


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
        self.executecommands()


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
        self.commands_to_execute = commands
        self.entry_text.set(self.commands_to_execute)
    def executecommands(self):
        self.emptyfiletable()
        self.cmd = self.commands_to_execute
        self.entry_text.set("")
        self.update()
        self.execute()
        if self.status == 0:
           self.num_files_recovered.set("Number of files recovered: " + str(self.num_file_carving))
           self.updatefiletable()
           return
        if self.status == 1:
           tkMessageBox.showerror("Error", self.error_info)
           return
        if self.status == -1:
           tkMessageBox.showerror("Error", "Invalid Scalpel Commands: "+ self.commands_to_execute)
           return
    def updatefiletable(self):
        count = 2
        for key,value in self.md5list.iteritems():
            y = key.replace(self.output_path+"/","")
            real_count = count - 1
            self.t.set(count,0,str(real_count)+ ". "+ y)
            self.t.set(count,1,value)
            count = count + 1
            if count >= 32:
                break
        self.update()
    def emptyfiletable(self):
        for count in range(2,31):
            self.t.set(count,0,"")
            self.t.set(count,1,"")
        self.update()

    ###################Functions from Passing.py#############################################
    # Main function to execute and parse result
    def execute(self):
        self.pss = 0
        # the scalpel command received from GUI
        # status of executing the command
        # -1: command itself constructed with errors
        # 0: command executed correctly
        # 1: command executed with error
        self.status = -2
        # Scalpel version
        self.version = ""
        # Author Informaiton
        self.authorInfo = ""
        # Images to be carved
        self.target = ""

        ##### TODO, multiple images support #####

        # percentage info for allocation, contains two float numbers:
        # 1, percentage info as NUM, such as 4.9 %
        # 2, bytes carved as NUM, such as 10.0 MB
        self.allocating_queue = ["", ""]
        # Carving signature list, contains four strings:
        # 1, type of carving files, such as "gif", "jpg"
        # 2, header, such as "\x47\x49\x46\x38\x37\x61"
        # 3, footer, such as "\x00\x3b"
        # 4, number of files carved for this signature, such as "20" files
        self.carving_list = []
        # percentage info for processing of images, contains two float numbers:
        # 1, percentage info as NUM, such as 48.8 %
        # 2, bytes carved as NUM, such as 100.0 MB
        self.image_processing = ["", ""]

        ##### TODO                          #####

        # Total number of file carved
        self.num_file_carving = -1
        # Total time consumed
        self.time_consumed = -1
        # Error informaiton if occured
        self.error_info = ""
        # MD5 list of all carved files
        self.md5list = {}
        if "scalpel" not in self.cmd:
            self.status = -1
            return
        else:
            p = process(self.cmd, shell=True)
            process_checker = 1
            front = p.recvlines(5)
            path = ""

            # Assign version and author information
            for line in front:
                if "Scalpel version" in line:
                    self.version = line.split(" ")[2].strip()
                if "Golden G. Richard III" in line:
                    self.authorInfo = line

            if "ERROR:" in front[2]:
                for line in front[2:]:
                    self.error_info += line + "\n"
                self.status = 1
                return
            # Assign images to be processed
            else:
                self.status = 0
                for line in front:
                    if "Opening target" in line:
                        self.target = line.split(" ")[2].strip('"')
                    else:
                        continue

            while p.can_recv():
                result = ""
                try:
                    result = p.recvuntil('\r')
                    if "ETA" in result and "Allocating work queues" not in result and "Processing of image" not in result:
                        percentage = float(result.split(":")[1].split("%")[0].strip())
                        byte = float(result.split(":")[1].split("%")[1].strip().split(" ")[0])
                        if process_checker == 1:
                            self.allocating_queue[0] = percentage
                            self.allocating_queue[1] = byte
                            self.percentage.set("Progress: " + str(self.allocating_queue[0]) + "% processed, " + str(self.allocating_queue[1]) + " MB carved")
                            self.update()
                        else:
                            self.image_processing[0] = percentage
                            self.image_processing[1] = byte
                            self.percentage.set("Progress: " + str(self.allocating_queue[0]) + "% processed, " + str(self.allocating_queue[1]) + " MB carved")
                            self.update()
                            if percentage > 97.0:
                                break
                    elif "Allocating work queues" in result:
                        percentage = float(result.splitlines()[0].split(":")[1].split("%")[0].strip())
                        byte = float(result.split(":")[1].split("%")[1].strip().split(" ")[0])
                        if process_checker == 1:
                            self.allocating_queue[0] = percentage
                            self.allocating_queue[1] = byte
                            self.percentage.set("Progress: " + str(self.allocating_queue[0]) + "% processed, " + str(self.allocating_queue[1]) + " MB carved")
                            self.update()
                            process_checker = 2

                        for line in result.splitlines()[1:]:
                            if "header" in line and "footer" in line:
                                temp = []
                                temp.append(line.split(" ")[0].strip())
                                temp.append(line.split(" ")[3].strip('"'))
                                temp.append(line.split(" ")[6].strip('"'))
                                temp.append(line.split(" ")[8].strip())
                                self.carving_list.append(temp)
                    else:
                        continue

                except EOFError:
                    break
            # Handle the rest of parsing info
            end = p.recvall()
            for line in end.splitlines():
                if "Processing of image" in line:
                    self.image_processing[0] = float(line.split(":")[1].split("%")[0].strip())
                    self.image_processing[1] = float(line.split(":")[1].split("%")[1].strip().split(" ")[0])
                elif "Scalpel is done," in line:
                    self.num_file_carving = int(line.split(" ")[6].strip(','))
                    self.time_consumed = int(line.split(" ")[9].strip())
                else:
                    continue

            if self.status == 0:
                parameter = self.cmd.split(" ")
                for i in range(0,len(parameter)):
                    if parameter[i] == "-o":
                        path = parameter[i+1]
                        break
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file == "audit.txt":
                            continue
                        else:
                            filename = os.path.join(root, file)
                            self.md5list[filename] = self.md5(filename)

    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        f.close()
        return hash_md5.hexdigest()



#Create the GUI
def create_form(argv):
    form = simpleform_ap(None)
    form.mainloop()


#Main Funciont
if __name__ == "__main__":
    create_form(sys.argv)
