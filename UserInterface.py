#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat April  5 23:36:17 2022

@author: Ghee, Zexi
"""
# importing tkinter gui
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, OptionMenu
from tkinter import filedialog as fd
# from tkmacosx import Button
from tkinter.filedialog import askdirectory
import sys
import os, re
import inspect
import similarity_algorithm
import downloadFinal
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkdnd
from tkinter import Text as txt
from tkinter import Scrollbar as scroll
from PIL import Image, ImageTk


class UserInterface(TkinterDnD.Tk):
    def __init__(self, *args, **kwargs):
        TkinterDnD.Tk.__init__(self, *args, **kwargs)
        self.title("Plagiarism Checker")
        self.geometry('650x375')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: UserInterface.on_closing(self))
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.sideBarContainer = tk.Frame(self)
        self.sideBarContainer.pack(side="left", fill="both", expand=0)
        self.mainContainer = tk.Frame(self)
        self.mainContainer.pack(side="right", fill="both", expand=1)
        self.mainContainer.grid_rowconfigure(0, weight=1)
        self.mainContainer.grid_columnconfigure(0, weight=1)
        self.sideBar()
        self.frames = {}

        page_name = MainPage.__name__
        frame = MainPage(parent=self.mainContainer)
        self.frames[page_name] = frame

        # put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.destroy()
            self.quit()

    def sideBar(self):
        self.update()  # For the width to get updated

        sid_bar_frame = tk.Frame(self.sideBarContainer, bg="#191970", width=140, height=self.winfo_height())
        sid_bar_frame.pack(side=tk.LEFT)

        img = Image.open('resource/Uni_logo.png')
        uni_Logo = ImageTk.PhotoImage(img.resize((105, 35)))

        # Make the buttons with the icons to be shown
        uni_label = tk.Label(sid_bar_frame, image=uni_Logo, highlightbackground='black', activebackground='black')
        uni_label.image = uni_Logo


        home_b = tk.Button(sid_bar_frame,
                        text="Home",
                        bg="#191970",
                        fg="white",
                        width=17,


                        command=lambda: self.show_frame("MainPage"))

        info_b = tk.Button(sid_bar_frame,
                        text="Help",
                        bg="#191970",
                        fg="white",
                        width=17,


                        command=lambda: self.infoButtonFunc())

        # Put them on the frame
        uni_label.grid(row=0, column=0, padx=1, pady=10)
        home_b.grid(row=1, column=0, padx=1, pady=30)
        info_b.grid(row=2, column=0, padx=5, pady=30)

        # So that it does not depend on the widgets inside the frame
        sid_bar_frame.grid_propagate(False)

    def infoButtonFunc(self):

        top = tk.Toplevel(
            master=self,
            width=self.winfo_width(),
            height=self.winfo_height(),
        )
        top.title("help")

        top_side_frame = tk.Frame(
            top,
            bg="#191970",
            width=200,
            height=self.winfo_height(),
        )

        # So that it does not depend on the widgets inside the frame
        top_side_frame.grid_propagate(False)

        # button
        Description_and_introduction_b = tk.Button(
            top_side_frame,
            text="Description and introduction    ",
            bg="#D7E4F0",
            fg="black",
            width=25,
            relief="flat",
            command=lambda: switch_text("resource/description.txt"),
        )

        Function_is_introduced_b = tk.Button(
            top_side_frame,
            text="Function and introduced  ",
            bg="#D7E4F0",
            fg="black",
            width=25,
            relief="flat",
            command=lambda: switch_text("resource/func.txt"),
        )
        Support_b = tk.Button(
            top_side_frame,
            text="Support",
            bg="#D7E4F0",
            fg="black",
            width=25,
            relief="flat",
            command=lambda: switch_text("resource/support.txt"),
        )
        Other_b = tk.Button(
            top_side_frame,
            text="Other",
            bg="#D7E4F0",
            fg="black",
            width=25,
            relief="flat",
            command=lambda: switch_text("resource/other.txt"),
        )

        Description_and_introduction_b.grid(
            row=0,
            column=0,
            padx=5,
            pady=10,
        )
        Function_is_introduced_b.grid(
            row=1,
            column=0,
            padx=5,
            pady=30,
        )
        Support_b.grid(
            row=2,
            column=0,
            padx=5,
            pady=10,
        )
        Other_b.grid(
            row=3,
            column=0,
            padx=5,
            pady=30,
        )

        top_main = tk.Frame(
            top,
            bg="#F5F5F5",
            width=self.winfo_width() - 200,
            height=(self.winfo_height()),
        )

        def switch_text(file):
            show_data_area.delete(1.0, "end")
            with open(file, "r", encoding="utf-8") as read_p:
                line = read_p.readline()
                while line:
                    update_text(line.strip("\n"), show_data_area)
                    line = read_p.readline()

        def update_text(result, txt):
            txt.insert(tk.END, result + "\n")
            txt.update()

        s1 = scroll(top_main)

        show_data_area = txt(
            master=top_main,
            height=30,
            font=("Helvetica", 12),
            yscrollcommand=s1.set,
        )

        s1.config(command=show_data_area.yview)
        s1.pack(side=tk.RIGHT, fill=tk.Y, pady=(15, 15))
        show_data_area.pack(fill=tk.BOTH, padx=(1, 0), pady=(15, 15))

        top_main.grid_propagate(False)

        top_side_frame.pack(side=tk.LEFT)
        top_main.pack(side=tk.RIGHT)

        switch_text("resource/description.txt")

        # Display until closed manually.
        top.mainloop()


class MainPage(tk.Frame):
    global names
    names = []
    global trans
    trans = []
    global allfloderpath  # mark all upload file path, avoid repetition
    allfloderpath = []
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    global parentdir
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)
    global folderPath
    folderPath = ""
    global transferDicList
    transferDicList = None

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        container = tk.Frame(self, bg="#F5F5F5")
        container.pack(side="right", fill="both", expand=True)

        topFrame = tk.Frame(container, bg='#F5F5F5', width=container.winfo_width(),
                            height=container.winfo_height() / 5 * 3)
        topFrame.pack(side=tk.TOP, fill="both", expand=1)
        middleFrame = tk.Frame(container, bg='#F5F5F5', width=container.winfo_width(),
                               height=container.winfo_height() / 5 * 1)
        middleFrame.pack(side=tk.TOP, expand=1)
        botFrame = tk.Frame(container, bg='#F5F5F5', width=container.winfo_width(),
                            height=container.winfo_height() / 5 * 2)
        botFrame.pack(side=tk.BOTTOM, fill="x", expand=1)

        # dropdown box
        stater = tk.IntVar()
        stater.set(0)

        # #code change button
        dropDownFrame = tk.Frame(middleFrame, bg='#F5F5F5', width=100,
                               height=5)
        dropDownFrame.pack(side=tk.TOP)
        # listBox and upload button
        listBoxFrame = tk.Frame(topFrame, bg='#F5F5F5', width=100,
                                height=60)
        listBoxFrame.grid(column=0, row=3, padx=10, columnspan=2)
        studentWork = tk.Label(topFrame, text='\nStudent Files \n', bg='#F5F5F5', fg='black', font=(0, 20))
        studentWork.grid(column=0, row=1, padx=10, columnspan=2)
        self.listBox = tk.Listbox(listBoxFrame, bg='white', fg='black', width=66, selectmode=tk.SINGLE)
        self.listBox.grid(column=0, row=1, padx=10, columnspan=2, rowspan=2)
        selection = tk.Button(botFrame, highlightbackground='#F5F5F5', text="Upload Folder", width=15, bg='white',
                           command=lambda: self.openFile())
        selection.grid(column=6, row=0, rowspan=2, columnspan=5, padx=50)

        self.listBox.drop_target_register(DND_FILES)
        self.listBox.dnd_bind('<<Drop>>', lambda e: self.dropdata(e.data))

        # button for start\cancel plagiarism check
        check = tk.Button(botFrame, bg='#00FF7F', text="Confirm", fg="black", width=11,
                       command=lambda: self.checkFile())
        check.grid(column=12, row=0, rowspan=2, columnspan=5, padx=40)

        cancel = tk.Button(botFrame, bg="#FF0000", text="Cancel", fg="black", width=11,
                        command=lambda: self.cancelFile())
        cancel.grid(column=1, row=0, rowspan=2, columnspan=5, padx=30)

    def checkFile(self, ):
        global folderPath
        global transferDicList
        global trans
        if folderPath is None:
            messagebox.showerror(title='Warning', message="Please upload a folder / files.")
        else:
            textmark = len(trans)
            txtmany = 0  # how many text file
            print(folderPath)
            for item in trans:
                if os.path.splitext(item)[-1][1:] == "py":
                    transferDicList = similarity_algorithm.check_python(folderPath)
                    self.repage()
                    break
                elif os.path.splitext(item)[-1][1:] == "java":
                    transferDicList = similarity_algorithm.check_java(folderPath)
                    print(transferDicList)
                    self.repage()
                    break
                elif os.path.splitext(item)[-1][1:] == "cpp":
                    transferDicList = similarity_algorithm.check_cpp(folderPath)
                    self.repage()
                    break
                elif os.path.splitext(item)[-1][1:] == "php":
                    transferDicList = similarity_algorithm.check_PHP(folderPath)
                    self.repage()
                    break
                elif os.path.splitext(item)[-1][1:] == "c":
                    transferDicList = similarity_algorithm.check_C(folderPath)
                    self.repage()
                    break
                elif os.path.splitext(item)[-1][1:] == "sql":
                    transferDicList = similarity_algorithm.check_sql(folderPath)
                    self.repage()
                    break
                elif os.path.splitext(item)[-1][1:] == "txt":
                    txtmany += 1
                else:
                    messagebox.showerror(title='Warning',
                                         message="Please only upload the following files:"
                                                 ".py"
                                                 ".java"
                                                 ".cpp"
                                                 ".php"
                                                 ".c"
                                                 ".sql"
                                                 ".txt")
            if txtmany == textmark:
                messagebox.showinfo(title="Language Selection", message="Please select the language you want")
                self.lanChoice()

    def lanChoice(self):
        Top = tk.Toplevel(self)
        Top.resizable(False, False)
        Top.geometry('400x150')

        container = tk.Frame(Top, bg="#F5F5F5")
        container.pack(side="right", fill="both", expand=True)

        topFrame = tk.Frame(container, bg='#F5F5F5', width=container.winfo_width(),
                            height=(container.winfo_height() / 5 * 4))
        topFrame.pack(side=tk.TOP, fill="both", expand=1)

        studentWork_l = tk.Label(topFrame, text='\nlanguage selection \n', bg='#F5F5F5', fg='black', font=(0, 20))
        studentWork_l.grid(column=0, row=0, padx=30)

        # dropdown box
        stater = tk.IntVar()
        stater.set(0)

        def changeCode():
            global transferDicList
            # change code message
            num = stater.get()
            if num == 1:
                transferDicList = similarity_algorithm.check_python(folderPath)
                self.repage()
            elif num == 2:
                transferDicList = similarity_algorithm.check_java(folderPath)
                self.repage()
            elif num == 3:
                transferDicList = similarity_algorithm.check_cpp(folderPath)
                self.repage()
            elif num == 4:
                transferDicList = similarity_algorithm.check_PHP(folderPath)
                self.repage()
            elif num == 5:
                transferDicList = similarity_algorithm.check_C(folderPath)
                self.repage()
            elif num == 6:
                transferDicList = similarity_algorithm.check_sql(folderPath)
                self.repage()
            Top.destroy()

        # code change button
        dropDownFrame = tk.Frame(topFrame, bg='#F5F5F5', width=100,
                                 height=5)
        dropDownFrame.grid(column=0, row=1, padx=30)
        codeButton1 = tk.Radiobutton(dropDownFrame, text='Python', variable=stater, value=1,
                                     command=changeCode)
        codeButton1.grid(column=0, row=4)
        codeButton2 = tk.Radiobutton(dropDownFrame, text='Java', variable=stater, value=2,
                                     command=changeCode)
        codeButton2.grid(column=1, row=4)
        codeButton3 = tk.Radiobutton(dropDownFrame, text='C++', variable=stater, value=3,
                                     command=changeCode)
        codeButton3.grid(column=2, row=4)
        codeButton4 = tk.Radiobutton(dropDownFrame, text='PHP', variable=stater, value=4,
                                     command=changeCode)
        codeButton4.grid(column=3, row=4)
        codeButton5 = tk.Radiobutton(dropDownFrame, text='C', variable=stater, value=5,
                                     command=changeCode)
        codeButton5.grid(column=4, row=4)
        codeButton6 = tk.Radiobutton(dropDownFrame, text='SQL', variable=stater, value=6,
                                     command=changeCode)
        codeButton6.grid(column=5, row=4)

    def transferList(self):
        # Declare global variables and pass parameters to result
        global transferDicList
        return transferDicList

    def openFile(self):
        global folderPath
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        folderPath = fd.askdirectory()
        if folderPath != "":
            folderPath = folderPath + '/'
            self.updateListBox()

    def cancelFile(self):
        # Cancel uploaded file
        global folderPath
        global names
        global trans
        self.listBox.delete("0", tk.END)
        folderPath = ""
        names = []
        trans = []

    def tansFloder(self):
        global folderPath
        return folderPath

    def updateListBox(self):
        global names
        global trans  # Global variables store uploaded files (Prevent redundant parameter input)
        global folderPath

        if folderPath != "":
            print(similarity_algorithm.walk_dir(folderPath))
            for i in similarity_algorithm.walk_dir(folderPath)[0]:
                if i not in names:  # Prevent duplicate uploads
                    names.append(i)
        self.listBox.delete(0, tk.END)
        for i in names:
            if not i.startswith("."):  # delete wrong files
                self.listBox.insert(tk.END, i)
                trans.append(i)
        return trans

    # drop upload file
    def dropdata(self, data):
        global folderPath
        if "{" in data:  # if folder name have ""
            resLeft = data.split("{")
            resRight = resLeft[1].split("}")
            data = resRight[0]
        path, file = os.path.split(data)
        if "." not in file:  # Determine if it is a folder
            folderPath = data + "/"
            print(folderPath)
            self.updateListBox()
        else:
            messagebox.showerror(title='Warning', message="Please upload folder")

    def repage(self):
        global filename
        filename = None

        # setting frame
        Top = tk.Toplevel(self)
        Top.resizable(False, False)
        Top.geometry('1400x710')

        container = tk.Frame(Top, bg="#F5F5F5")
        container.pack(side="right", fill="both", expand=True)


        #side frame for result
        sideFrame = tk.Frame(container, bg='#191970', width=60,
                            height=(container.winfo_height()))
        sideFrame.pack(side="left", fill= 'y', expand=False)

        studentWork_l = tk.Label(sideFrame, text='Plagiarism\nResult', bg='#191970', fg='white', font=(0, 20))
        studentWork_l.grid(column=0, row=0, padx=10, pady=5)
        # setting treeview
        listBoxFrame = tk.Frame(sideFrame, bg='#191970', width=80,
                                height=60)
        listBoxFrame.grid(column=0, row=1, padx=10)
        listBoxButtonFrame = tk.Frame(sideFrame, bg='#191970', width=80,
                                      height=50)
        listBoxButtonFrame.grid(column=0, row=2, padx=10)
        colums = ['File Name', 'Rate']  # the treeview head setting
        self.resultListBox = ttk.Treeview(listBoxFrame, columns=colums, show='headings', heigh=25)
        self.resultListBox.grid(column=1, row=1, padx=20)
        self.resultListBox.heading('File Name', text='File Name', )
        self.resultListBox.heading('Rate', text='Rate', )
        self.resultListBox.column('File Name', width=100)
        self.resultListBox.column('Rate', width=60)

        # setting defferent rate to different color
        self.resultListBox.tag_configure('tag_green',
                                         foreground='green')
        self.resultListBox.tag_configure('tag_origin',
                                         foreground='orange')
        self.resultListBox.tag_configure('tag_red',
                                         foreground='red')

        # for right frame to show result
        resultFrame = tk.Frame(container, bg='#F5F5F5', width=(container.winfo_width()-150),
                            height=(container.winfo_height()))
        resultFrame.pack(side="right", fill='both', expand=True)

        #seperate frame for result and button
        resultTextFrame = tk.Frame(resultFrame, bg='#F5F5F5', width=(resultFrame.winfo_width()),
                                   height=(resultFrame.winfo_height()))
        resultTextFrame.pack(side=tk.TOP, fill='both', expand=True)
        #result frame on right side
        resultButtonFrame = tk.Frame(resultFrame, bg='#F5F5F5', width=(resultFrame.winfo_width()),
                                     height=(resultFrame.winfo_height()))
        resultButtonFrame.pack(side=tk.BOTTOM, fill='both', expand=True)

        #where the result shown
        leftFrame = tk.Frame(resultTextFrame, bg='#F5F5F5', width=((resultTextFrame.winfo_width()) / 2),
                             height=(resultTextFrame.winfo_height()/5*4))
        leftFrame.pack(side=tk.LEFT, fill='both', padx = 10, pady=5)
        rightFrame = tk.Frame(resultTextFrame, bg='#F5F5F5', width=((resultTextFrame.winfo_width()) / 2),
                             height=(resultTextFrame.winfo_height()/5*4))
        rightFrame.pack(side=tk.RIGHT, fill='both',padx=10, pady=5)


        singleReportButton = tk.Button(resultButtonFrame, text="Download selected report", fg="black", width=40,
                                    command=lambda: self.creatPathSin())
        singleReportButton.pack(side=tk.RIGHT, padx=50)
        result = tk.Button(resultButtonFrame, text="Download all report", fg="black", width=40,
                        command=lambda: self.creatPathSMui())
        result.pack(side=tk.LEFT, padx=50)

        #label
        studentFileName_l_p1 = tk.Label(leftFrame, text='Report 1 \n', bg='#F5F5F5', fg='black', font=(0, 15))
        studentFileName_l_p1.pack(side=tk.TOP, pady=10, padx=10)
        studentFileName_l_p2 = tk.Label(rightFrame, text='Report 2 \n', bg='#F5F5F5', fg='black', font=(0, 15))
        studentFileName_l_p2.pack(side=tk.TOP, pady=10, padx=10)
        # right textbox
        scrolly_p1 = tk.Scrollbar(rightFrame)
        scrolly_p1.pack(side=tk.RIGHT, fill=tk.Y)

        scrollx_p1 = tk.Scrollbar(rightFrame, orient=tk.HORIZONTAL)
        scrollx_p1.pack(side=tk.BOTTOM, fill=tk.X)
        # set textbox and link scrollbar
        self.reportListBox1 = tk.Text(rightFrame, wrap='none')
        self.reportListBox1.pack(fill=tk.BOTH, expand=tk.YES)
        self.reportListBox1.config(yscrollcommand=scrolly_p1.set)
        self.reportListBox1.config(xscrollcommand=scrollx_p1.set)
        scrolly_p1.config(command=self.reportListBox1.yview)
        scrollx_p1.config(command=self.reportListBox1.xview)

        #left textbox
        # set scrollbar
        scrolly_p2 = tk.Scrollbar(leftFrame)
        scrolly_p2.pack(side=tk.RIGHT, fill=tk.Y)

        scrollx_p2 = tk.Scrollbar(leftFrame, orient=tk.HORIZONTAL)
        scrollx_p2.pack(side=tk.BOTTOM, fill=tk.X)

        # set textbox and link scrollbar
        self.reportListBox = tk.Text(leftFrame, wrap='none')
        self.reportListBox.pack(fill=tk.BOTH, expand=tk.YES)
        self.reportListBox.config(yscrollcommand=scrolly_p2.set)
        self.reportListBox.config(xscrollcommand=scrollx_p2.set)
        scrolly_p2.config(command=self.reportListBox.yview)
        scrollx_p2.config(command=self.reportListBox.xview)

        self.reportListBox.bind('<KeyPress>', lambda e: 'break')
        self.reportListBox1.bind('<KeyPress>', lambda e: 'break')# Limit user input




        # button for show result and show report
        showRep_b1 = tk.Button(listBoxButtonFrame, text="Show on\nreport 1",bg='white', fg="#191970", width=10,
                       command=lambda: self.clickReport1())
        showRep_b2 = tk.Button(listBoxButtonFrame, text="Show on\nreport 2",bg='white', fg="#191970", width=10,
                       command=lambda: self.clickReport2())
        showRep_b1.pack(side=tk.LEFT, padx=5, pady=50)
        showRep_b2.pack(side=tk.RIGHT, padx=5, pady=50)

        self.path = tk.StringVar()  # store user want path

        thisDict = MainPage.transferList(self=MainPage)  # get the result
        if thisDict is None:
            messagebox.showerror(title='Warning', message="No Result")
        else:
            resultList = thisDict[0]  # get the file and rate(dic)
            i = 0
            my_list = []
            for row in self.resultListBox.get_children():
                # initialization treeview
                self.resultListBox.delete(row)
            for key, val in resultList.items():
                newCalue1 = float(resultList[key])  # get the result rate
                newCalue2 = newCalue1 * 100
                newCalue3 = float('%.2f' % newCalue2)
                newvalue = str(newCalue3) + "%"
                my_list.append((key, newvalue))  # add file name and rate to the new list
            for value in my_list:
                new1 = value[1].strip("%")  # throw the %
                new2 = float(new1)
                # Determine repetition rate and add color
                if new2 <= 20:
                    tag = 'tag_green'
                elif new2 > 50:
                    tag = 'tag_red'
                else:
                    tag = 'tag_origin'
                self.resultListBox.insert(parent='', index=i, iid=i, values=value, tags=tag)
                i += 1



    def show_selected(self):
        # get user selection
        global filename
        # messagebox.showinfo(title="Report Generation", message="Please click Preview on the Report page to view the report")
        for item in self.resultListBox.selection():  # get selection
            item_text = self.resultListBox.item(item, "values")  # get the filename and rate
            filename = item_text[0]  # get the name
        return filename

    def clickReport1(self):
        if self.show_selected() is None:
            messagebox.showerror(title='Warning', message="Please select a file.")
        else:
            self.showOnText1()

    def showOnText1(self):

        global filename

        self.path = tk.StringVar()  # store user want path
        thisName = self.show_selected()  # get user selection
        reportResult = MainPage.transferList(self=MainPage)  # get result
        folderPath = MainPage.tansFloder(self=MainPage)
        l = downloadFinal.download.trans(folderPath, trans, thisName, reportResult)[0]  # get report content
        self.reportListBox.delete("1.0", "end")  # clear textbox

        a=1.0
        for i in range(0, len(l)):
            # set color
            a+=1.0
            self.reportListBox.tag_add('warning', a)
            self.reportListBox.tag_configure('warning',
                                             foreground='red')
            self.reportListBox.tag_add('normal', a)
            self.reportListBox.tag_configure('normal',
                                             foreground='black')
            self.reportListBox.tag_add('repeat', a)
            self.reportListBox.tag_configure('repeat',
                                             foreground='blue')

            # mark the duplicate row
            if "#!#" in l[i]:
                res = l[i].split("#!#", 1)
                self.reportListBox.insert(a, res[0], 'repeat')
                a+=1.0
                self.reportListBox.insert(a, res[1], 'warning')
            elif "#@# Repeated mark" in l[i]:
                res = l[i].split("#@# Repeated mark", 1)
                self.reportListBox.insert(a, res[0] + "\n", 'repeat')
            else:
                self.reportListBox.insert(a, l[i], 'normal')



    def clickReport2(self):
        if self.show_selected() is None:
            messagebox.showerror(title='Warning', message="Please select a file.")
        else:
            self.showOnText2()

    def showOnText2(self):
        global filename

        self.path = tk.StringVar()  # store user want path
        thisName = self.show_selected()  # get user selection
        reportResult = MainPage.transferList(self=MainPage)  # get result
        folderPath = MainPage.tansFloder(self=MainPage)
        l = downloadFinal.download.trans(folderPath, trans, thisName, reportResult)[0]  # get report content
        self.reportListBox1.delete("1.0", "end")  # clear textbox

        a=1.0
        for i in range(0, len(l)):
            # set color
            a+=1.0
            self.reportListBox1.tag_add('warning', a)
            self.reportListBox1.tag_configure('warning',
                                             foreground='red')
            self.reportListBox1.tag_add('normal', a)
            self.reportListBox1.tag_configure('normal',
                                             foreground='black')
            self.reportListBox1.tag_add('repeat', a)
            self.reportListBox1.tag_configure('repeat',
                                             foreground='blue')

            # mark the duplicate row
            if "#!#" in l[i]:
                res = l[i].split("#!#", 1)
                self.reportListBox1.insert(a, res[0], 'repeat')
                a+=1.0
                self.reportListBox1.insert(a, res[1], 'warning')
            elif "#@# Repeated mark" in l[i]:
                res = l[i].split("#@# Repeated mark", 1)
                self.reportListBox1.insert(a, res[0] + "\n", 'repeat')
            else:
                self.reportListBox1.insert(a, l[i], 'normal')

    # choice report save path and save the report
    def creatPathSin(self):
        path_ = askdirectory()
        self.path.set(path_)
        self.downSinFile()

    def creatPathSMui(self):
        path_ = askdirectory()
        self.path.set(path_)
        self.downMuiFIle()

    def downSinFile(self):
        path = self.path.get()
        reportResult = MainPage.transferList(self=MainPage)
        messagebox.showinfo(title="Report Generation", message="This Plagiarism Result has been generated")
        downloadFinal.download.use(folderPath, trans, self.show_selected(), reportResult, path)

    def downMuiFIle(self):
        path = self.path.get()
        reportResult = MainPage.transferList(self=MainPage)
        messagebox.showinfo(title="Report Generation", message="All Plagiarism Result has been generated")
        downloadFinal.download.alluse(folderPath, trans, reportResult, path)


if __name__ == "__main__":
    app = UserInterface()
    app.mainloop()
