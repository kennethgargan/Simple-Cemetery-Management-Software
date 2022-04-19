from email.mime import image
from os import stat
import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tkinter import scrolledtext
from turtle import width

import model as db

class View:
    def __init__(self,root):
        self.root = root
        self.root.title('Cemetery Database')
        self.root.geometry('{}x{}'.format(1200, 900))

        # create all of the main containers
        self.top_frame = Frame(self.root, width=450, height=50)
        self.middle_upper_frame = Frame(self.root, bg='gray2', width=50, height=40)
        self.middle_lower_frame = Frame(self.root, bg='gray2', width=450, height=100)
        self.footer_frame = Frame(self.root, width=450, height=50)

        # layout all of the main containers
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2,weight=1)

        self.top_frame.grid(row=0, sticky="ew")
        self.middle_upper_frame.grid(row=1, sticky="nsew")
        self.middle_lower_frame.grid(row=2, sticky="nsew")
        self.footer_frame.grid(row=4, sticky="ew")


        # create the self.middle_upper_frame widgets
        self.middle_upper_frame.grid_rowconfigure(0, weight=1)
        self.middle_upper_frame.grid_columnconfigure(2, weight=1)

        self.middle_upper_ctr_left = LabelFrame(self.middle_upper_frame, text="Section", width=200, height=190)
        self.middle_upper_ctr_mid = LabelFrame(self.middle_upper_frame, text="Plot", width=200, height=190)
        self.middle_upper_ctr_right = LabelFrame(self.middle_upper_frame, text="Deceased", width=250, height=190)

        self.middle_upper_ctr_left.grid(row=0, column=0, sticky="nsew")
        self.middle_upper_ctr_mid.grid(row=0, column=1, sticky="nsew")
        self.middle_upper_ctr_right.grid(row=0, column=2, sticky="nsew")

        #section List
        self.section_list_tree = ttk.Treeview(self.middle_upper_ctr_left)
        self.section_list_tree['columns'] = ('id','section')
        self.section_list_tree.column("#0", width = 0,stretch=0)
        self.section_list_tree.column("id", width = 0,stretch=0)
        self.section_list_tree.column("section", anchor=W, width=195)
       
        self.section_list_tree.heading("#0", text="", anchor=W)
        self.section_list_tree.heading("id", text="", anchor=W)
        self.section_list_tree.heading('section', text="Section")
        self.section_list_tree.bind("<ButtonRelease-1>")

        self.section_list_tree.pack(expand=True, fill='y')

        #plot List
        self.plot_tree = ttk.Treeview(self.middle_upper_ctr_mid)
        self.plot_tree['columns'] = ('id','section_owner','section','section_number')
        self.plot_tree.column("#0", width = 0,stretch=0)
        self.plot_tree.column("id", width = 0,stretch=0)
        self.plot_tree.column("section_owner", anchor=W, width=110)
        self.plot_tree.column("section", anchor=W, width=40)
        self.plot_tree.column("section_number", anchor=W, width=45)

        self.plot_tree.heading("#0", text="", anchor=W)
        self.plot_tree.heading("id", text="", anchor=W)
        self.plot_tree.heading('section', text="")
        self.plot_tree.heading('section_owner', text="Plot Owner")
        self.plot_tree.heading('section_number', text="#")
        self.plot_tree.bind("<ButtonRelease-1>")

        self.plot_tree.pack(expand=True, fill='y')

        #Deceased List
        self.record_tree = ttk.Treeview(self.middle_upper_ctr_right)
        self.record_tree['columns'] = ('id','section_id','fname','sname','dod')
        self.record_tree.column("#0", width = 0,stretch=0)
        self.record_tree.column("id", width = 0,stretch=0)
        self.record_tree.column("section_id", anchor=W,width=0,stretch=0)
        self.record_tree.column("fname", anchor=W)
        self.record_tree.column("sname", anchor=W)
        self.record_tree.column("dod", anchor=W)

        self.record_tree.heading("#0", text="", anchor=W)
        self.record_tree.heading("id", text="", anchor=W)
        self.record_tree.heading('section_id', text="")
        self.record_tree.heading('fname', text="First Name")
        self.record_tree.heading('sname', text="Surname")
        self.record_tree.heading('dod', text="Deceased")
        self.record_tree.grid(row=0, column=2, sticky="nsew")
        self.record_tree.bind("<ButtonRelease-1>")
        self.record_tree.pack(expand=True, fill='both')
        
        self.middle_upper_ctr_right.grid_columnconfigure(2, weight=1)
        self.middle_lower_frame.grid_rowconfigure(0, weight=1)
        self.middle_lower_frame.grid_columnconfigure(2, weight=1)


        self.middle_lower_ctr_left = LabelFrame(self.middle_lower_frame, text="Section Management", width=200, height=190)
        self.middle_lower_ctr_mid = LabelFrame(self.middle_lower_frame, text="Plot Management", width=200, height=190)
        self.middle_lower_ctr_mid_two = LabelFrame(self.middle_lower_frame, text="Deceased Management", width=250, height=190)
        self.middle_lower_ctr_right = LabelFrame(self.middle_lower_frame, text="Image Preview", width=250, height=190)
        self.middle_lower_ctr_left.grid(row=0, column=0, sticky="nsew")
        self.middle_lower_ctr_mid.grid(row=0, column=1, sticky="nsew")
        self.middle_lower_ctr_mid_two.grid(row=0, column=2, sticky="nsew")
        self.middle_lower_ctr_right.grid(row=0, column=3, sticky="nsew")

        #Section list - Add / Edit
        self.section_notebook = ttk.Notebook(self.middle_lower_ctr_left, width=195)
        self.section_notebook.grid(row=0, column=0, sticky="nsew")
        self.section_management_frame_add = Frame(self.middle_lower_frame, width=200, height=190)
        self.section_management_frame_edit = Frame(self.middle_lower_frame, width=200, height=190)
        self.section_management_frame_add.grid(row=0, column=0, sticky="nsew")
        self.section_management_frame_edit.grid(row=0, column=0, sticky="nsew")
        self.section_notebook.add(self.section_management_frame_add,text="Add")
        self.section_notebook.add(self.section_management_frame_edit,text="Edit")
        self.middle_lower_ctr_left.grid_rowconfigure(0, weight=1)

        #Add
        self.section_add_label=Label(self.section_management_frame_add,text="Enter Section Name:")
        self.section_add_label.pack()
        self.section_add_entry = Entry(self.section_management_frame_add)
        self.section_add_entry.pack()
        self.section_add_button = Button(self.section_management_frame_add, text="Add")
        self.section_add_button.pack()
        
        #Edit
        self.section_edit_label=Label(self.section_management_frame_edit,text="Edit Section Name:")
        self.section_edit_label.pack()
        self.section_edit_entry = Entry(self.section_management_frame_edit)
        self.section_edit_entry.pack()
        self.section_edit_button = Button(self.section_management_frame_edit, text="Edit", state="disabled")
        self.section_edit_button.pack()

        #plot List - Add / Edit
        self.plot_notebook = ttk.Notebook(self.middle_lower_ctr_mid,width=190)
        self.plot_notebook.grid(row=0, column=0, sticky="nsew")
        self.plot_management_frame_add = Frame(self.middle_lower_frame, width=200, height=190)
        self.plot_management_frame_edit = Frame(self.middle_lower_frame, width=200, height=190)
        self.plot_management_frame_add.grid(row=0, column=0, sticky="nsew")
        self.plot_management_frame_edit.grid(row=0, column=0, sticky="nsew")
        self.plot_notebook.add(self.plot_management_frame_add,text="Add")
        self.plot_notebook.add(self.plot_management_frame_edit,text="Edit")
        self.middle_lower_ctr_mid.grid_rowconfigure(0, weight=1)

        #Add
        self.plot_add_label_section=Label(self.plot_management_frame_add,text="Adding to Section:")
        self.plot_add_label_section.pack()
        self.plot_add_entry_section = Entry(self.plot_management_frame_add, state="disabled")
        self.plot_add_entry_section.pack()
        self.plot_add_label_owner=Label(self.plot_management_frame_add,text="Enter Plot Owner:")
        self.plot_add_label_owner.pack()
        self.plot_add_entry_owner = Entry(self.plot_management_frame_add)
        self.plot_add_entry_owner.pack()
        self.plot_add_label_plot=Label(self.plot_management_frame_add,text="Enter Plot Number")
        self.plot_add_label_plot.pack()
        self.plot_add_entry_number = Entry(self.plot_management_frame_add)
        self.plot_add_entry_number.pack()
        self.plot_add_button = Button(self.plot_management_frame_add, text="Add", state="disabled")
        self.plot_add_button.pack()
        
        #Edit
        self.plot_edit_label_section=Label(self.plot_management_frame_edit,text="Edit Plot Section:")
        self.plot_edit_label_section.pack()
        self.plot_edit_entry_section = Entry(self.plot_management_frame_edit)
        self.plot_edit_entry_section.pack()
        self.plot_edit_label_owner=Label(self.plot_management_frame_edit,text="Edit Plot Owner:")
        self.plot_edit_label_owner.pack()
        self.plot_edit_entry_owner = Entry(self.plot_management_frame_edit)
        self.plot_edit_entry_owner.pack()
        self.plot_edit_label_number=Label(self.plot_management_frame_edit,text="Edit Plot Number:")
        self.plot_edit_label_number.pack()
        self.plot_edit_entry_number = Entry(self.plot_management_frame_edit)
        self.plot_edit_entry_number.pack()
        self.plot_edit_button = Button(self.plot_management_frame_edit, text="Edit",state="disabled")
        self.plot_edit_button.pack()

        #Deceased List - Add / Edit
        self.deceased_notebook = ttk.Notebook(self.middle_lower_ctr_mid_two)
        self.deceased_notebook.grid(row=0, column=0, sticky="nsew")
        self.deceased_management_frame_add = Frame(self.middle_lower_frame, width=200, height=190)
        self.deceased_management_frame_edit = Frame(self.middle_lower_frame, width=200, height=190)
        self.deceased_management_frame_add.grid(row=0, column=0, sticky="nsew")
        self.deceased_management_frame_edit.grid(row=0, column=0, sticky="nsew")
        self.deceased_notebook.add(self.deceased_management_frame_add,text="Add")
        self.deceased_notebook.add(self.deceased_management_frame_edit,text="Edit")
        self.middle_lower_ctr_mid_two.grid_rowconfigure(0, weight=1)
        self.middle_lower_ctr_mid_two.grid_columnconfigure(0,weight=1)

        #Add
        self.deceased_add_label_plot=Label(self.deceased_management_frame_add,text="Adding to Plot")
        self.deceased_add_label_plot.pack()
        self.deceased_add_entry_plot = Entry(self.deceased_management_frame_add, state="disabled")
        self.deceased_add_entry_plot.pack()
        self.deceased_add_label_fname=Label(self.deceased_management_frame_add,text="First Name:")
        self.deceased_add_label_fname.pack()
        self.deceased_add_entry_fname = Entry(self.deceased_management_frame_add)
        self.deceased_add_entry_fname.pack()
        self.deceased_add_label_sname=Label(self.deceased_management_frame_add,text="Surname:")
        self.deceased_add_label_sname.pack()
        self.deceased_add_entry_sname = Entry(self.deceased_management_frame_add)
        self.deceased_add_entry_sname.pack()
        self.deceased_add_label_plot=Label(self.deceased_management_frame_add,text="Deceased Date (YYYY/MM/DD):")
        self.deceased_add_label_plot.pack()
        self.deceased_add_entry_date = Entry(self.deceased_management_frame_add)
        self.deceased_add_entry_date.pack()
        self.deceased_add_button = Button(self.deceased_management_frame_add, text="Add",state="disabled")
        self.deceased_add_button.pack()
        
        #Edit
        self.deceased_edit_label_fname=Label(self.deceased_management_frame_edit,text="First Name:")
        self.deceased_edit_label_fname.pack()
        self.deceased_edit_entry_fname = Entry(self.deceased_management_frame_edit)
        self.deceased_edit_entry_fname.pack()
        self.deceased_edit_label_sname=Label(self.deceased_management_frame_edit,text="Surname:")
        self.deceased_edit_label_sname.pack()
        self.deceased_edit_entry_sname = Entry(self.deceased_management_frame_edit)
        self.deceased_edit_entry_sname.pack()
        self.deceased_edit_label_plot=Label(self.deceased_management_frame_edit,text="Deceased Date:")
        self.deceased_edit_label_plot.pack()
        self.deceased_edit_entry_date = Entry(self.deceased_management_frame_edit)
        self.deceased_edit_entry_date.pack()
        self.deceased_edit_button = Button(self.deceased_management_frame_edit, text="Edit",state="disabled")
        self.deceased_edit_button.pack()

        self.canvas= Canvas(self.middle_lower_ctr_right, width= 250, height=400)
        self.canvas.pack()
        
    def create_messagebox(self,text):
         messagebox.showerror(title="Error", message=text)