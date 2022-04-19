from datetime import datetime
from tkinter import END, W, commondialog
from setuptools import Command
from model import Model
from view import View
class Controller:
    def __init__(self,root):
        self.root = root
        self.model = Model()
        self.view = View(self.root)

        self.model.create_tables()

        #self.view.ch1_top_btn_on.config(command=self.ch1_btn_on_click)
        self.view.section_list_tree.bind("<ButtonRelease-1>",self.section_click)
        self.view.plot_tree.bind("<ButtonRelease-1>",self.plot_click)
        self.view.record_tree.bind("<ButtonRelease-1>",self.record_click)
        
        self.view.section_add_button.config(command=self.add_new_section)
        self.view.section_edit_button.config(command=self.edit_section_name)
        
        self.view.plot_add_button.config(command=self.add_plot)
        self.view.plot_edit_button.config(command=self.edit_plot)
        
        self.view.deceased_add_button.config(command=self.add_deceased)
        self.view.deceased_edit_button.config(command=self.edit_deceased)

        self.display_section_names(self.model.get_section_names())

    def section_click(self,event):
        self.view.deceased_add_button["state"] = "disabled"
        #Check to see if ALL was clicked and if so, we want to show the section but if they click a section that isn't all, we want to show which section
        self.selected = self.view.section_list_tree.focus()
        values = list(self.view.section_list_tree.item(self.selected,'values'))
        if len(values)>0:
            #Update the edit box
            self.view.section_edit_entry.delete(0,END)
            self.view.section_edit_entry.insert(END,values[1])
            if values[1] == "All":
                self.view.section_edit_button["state"] = "disabled"
                self.view.plot_add_button["state"] = "disabled"
                self.view.plot_tree.column("section", anchor=W, width=40,stretch=1)
                self.view.plot_tree.column("section_owner", anchor=W, width=110)
            else:
                self.view.section_edit_button["state"] = "normal"
                self.view.plot_add_button["state"] = "normal"
                self.view.plot_tree.column("section", anchor=W, width=0,stretch=0)
                self.view.plot_tree.column("section_owner", anchor=W, width=150)

            self.view.plot_tree.delete(*self.view.plot_tree.get_children())
            self.view.record_tree.delete(*self.view.record_tree.get_children())
            self.display_plot_owners(self.model.query_plot_owners(values[1]))
            
            #Update the plot entry information
            self.view.plot_add_entry_section["state"] = "normal"
            self.view.plot_add_entry_section.delete(0,END)
            self.view.plot_add_entry_section.insert(END,values[1])
            self.view.plot_add_entry_section["state"] = "disabled"
    
    def display_section_names(self,items):
        self.view.section_list_tree.insert(parent='',index='end',iid=0,text="Parent",values=("","All"))
        for count, item in enumerate(items,start=1):
            self.view.section_list_tree.insert(parent='',index='end',iid=count,text="Parent",values=(item[0],item[1]))

    def display_section_names(self,items):
        self.view.section_list_tree.insert(parent='',index='end',iid=0,text="Parent",values=("","All"))
        for count, item in enumerate(items,start=1):
            self.view.section_list_tree.insert(parent='',index='end',iid=count,text="Parent",values=(item[0],item[1]))

    def display_plot_owners(self,items):
        for count, item in enumerate(items):
            self.view.plot_tree.insert(parent='',index='end',iid=count,text="Parent",values=(item[0], item[1],item[2],item[3]))
    def display_deceased_records(self,items):
        for count, item in enumerate(items):
            self.view.record_tree.insert(parent='',index='end',iid=count,text="Parent",values=item)

    def add_new_section(self):
        input_name = self.view.section_add_entry.get().capitalize()
        valid_name = True
        for item in self.model.get_section_names():
            if input_name == item[1]:
                self.view.create_messagebox("Duplicate Plot Name: Please enter a different name.")
                valid_name = False
                break
        if valid_name == True:
            self.model.create_section(input_name)
            self.refresh_section()
        
    def edit_section_name(self):
        input_name = self.view.section_add_entry.get()
        selected = self.view.section_list_tree.focus()
        values = list(self.view.section_list_tree.item(selected,'values'))

        if input_name== "All" or input_name in self.model.get_section_names():
            self.view.create_messagebox("Duplicate Section Name: Please enter a different name.")
        elif ' ' in input_name:
            self.view.create_messagebox("Section must not contain whitespace.")
        else:
            self.model.update_section_name(values[0],values[1],self.view.section_edit_entry.get())
            self.refresh_section()

            #Clear the edit entry.
            self.view.section_edit_entry.delete(0,END)
            self.view.section_edit_button["state"] = "disabled"

            #Clear the Plot List
            self.view.plot_tree.delete(*self.view.plot_tree.get_children())

            #Clear the Plot Section Add
            self.view.plot_add_entry_section["state"] = "normal"
            self.view.plot_add_entry_section.delete(0,END)
            self.view.plot_add_entry_section["state"] = "disabled"

    def add_plot(self):
        input_section = self.view.plot_add_entry_section.get()
        input_name = self.view.plot_add_entry_owner.get()
        input_plot_number = self.view.plot_add_entry_number.get()

        check_num = False
        check_plot = False

        if input_plot_number.isdigit():
            #check to see if a plot number already exists:
            if len(self.model.query_plot(input_section,input_plot_number)) == 0:
                check_plot = True
        else:
            self.view.create_messagebox("Plot Number must be a whole number.")
        if check_plot == True and len(input_name) > 0:
            self.model.create_plot(input_name,input_section,input_plot_number)
            self.view.plot_tree.delete(*self.view.plot_tree.get_children())
            self.display_plot_owners(self.model.query_plot_owners(input_section))

            #Clear the box after entered.
            self.view.plot_add_entry_owner.delete(0,END)
            self.view.plot_add_entry_number.delete(0,END)
        else:
            self.view.create_messagebox("Unable to create plot. Check Plot Owner has been entered.")

    def edit_plot(self):
        input_section = self.view.plot_edit_entry_section.get()
        input_name = self.view.plot_edit_entry_owner.get()
        input_number = self.view.plot_edit_entry_number.get()

        selected = self.view.plot_tree.focus()
        values = self.view.plot_tree.item(selected,'values')

        self.model.update_plot(values[0],input_name,input_section,input_number)
        self.refresh_plots()
        self.view.plot_edit_button["state"] = "disabled"

        self.view.plot_edit_entry_owner.delete(0,END)
        self.view.plot_edit_entry_number.delete(0,END)

    def add_deceased(self):
        #Plot Information:
        selected = self.view.plot_tree.focus()
        values = self.view.plot_tree.item(selected,'values')

        input_fname = self.view.deceased_add_entry_fname.get()
        input_sname = self.view.deceased_add_entry_sname.get()
        input_date = self.view.deceased_add_entry_date.get()

        if len(input_fname) and len(input_sname) and len(input_date) > 0:
            if self.check_date(input_date):
                self.model.create_deceased(values[0],input_fname,input_sname,input_date)
                self.refresh_deceased()
                self.view.deceased_add_entry_fname.delete(0,END)
                self.view.deceased_add_entry_date.delete(0,END)
            else:
                pass
                 #messagebox.showerror("Error", "Date Format Error: Make sure date is: YYYY-MM-DD. Example: 2010,12,20")
        else:
            self.view.create_messagebox("Error", "All boxes must be filled.")


    def edit_deceased(self):
        input_fname = self.view.deceased_edit_entry_fname.get()
        input_sname = self.view.deceased_edit_entry_sname.get()
        input_date = self.view.deceased_edit_entry_date.get()

        selected = self.view.record_tree.focus()
        values = self.view.record_tree.item(selected,'values')

        self.model.update_deceased(values[0],input_fname,input_sname,input_date)
        self.refresh_deceased()
        self.view.deceased_edit_button["state"] = "disabled"

        self.view.deceased_edit_entry_fname.delete(0,END)
        self.view.deceased_edit_entry_sname.delete(0,END)
        self.view.deceased_edit_entry_date.delete(0,END)

    def section_click(self,event):
        self.view.deceased_add_button["state"] = "disabled"
        #Check to see if ALL was clicked and if so, we want to show the section but if they click a section that isn't all, we want to show which section
        selected = self.view.section_list_tree.focus()
        values = list(self.view.section_list_tree.item(selected,'values'))
        if len(values)>0:
            #Update the edit box
            self.view.section_edit_entry.delete(0,END)
            self.view.section_edit_entry.insert(END,values[1])
            if values[1] == "All":
                self.view.section_edit_button["state"] = "disabled"
                self.view.plot_add_button["state"] = "disabled"
                self.view.plot_tree.column("section", anchor=W, width=40,stretch=1)
                self.view.plot_tree.column("section_owner", anchor=W, width=110)
            else:
                self.view.section_edit_button["state"] = "normal"
                self.view.plot_add_button["state"] = "normal"
                self.view.plot_tree.column("section", anchor=W, width=0,stretch=0)
                self.view.plot_tree.column("section_owner", anchor=W, width=150)

            self.view.plot_tree.delete(*self.view.plot_tree.get_children())
            self.view.record_tree.delete(*self.view.record_tree.get_children())
            self.display_plot_owners(self.model.query_plot_owners(values[1]))
            
            #Update the plot entry information
            self.view.plot_add_entry_section["state"] = "normal"
            self.view.plot_add_entry_section.delete(0,END)
            self.view.plot_add_entry_section.insert(END,values[1])
            self.view.plot_add_entry_section["state"] = "disabled"


    def plot_click(self,event):
        selected = self.view.plot_tree.focus()
        values = self.view.plot_tree.item(selected,'values')

        if len(values) > 0:
            #Change Plot display
            self.view.plot_edit_entry_owner.delete(0,END)
            self.view.plot_edit_entry_owner.insert(END, values[1])
            self.view.plot_edit_entry_section.delete(0,END)
            self.view.plot_edit_entry_section.insert(END, values[2])
            self.view.plot_edit_entry_number.delete(0,END)
            self.view.plot_edit_entry_number.insert(END, values[3])
            self.view.plot_edit_button["state"] = "normal"

            #Change Deceased Display
            self.view.deceased_add_entry_plot["state"] = "normal"
            self.view.deceased_add_entry_plot.delete(0,END)
            self.view.deceased_add_entry_plot.insert(END,values[1])
            self.view.deceased_add_entry_plot["state"] = "disabled"
            self.view.deceased_add_button["state"] = "normal"
            
            #Clear the input boxes.
            self.view.record_tree.delete(*self.view.record_tree.get_children())
            self.display_deceased_records(self.model.query_deceased_by_id(values[0]))

        #self.load_image()
    
    def record_click(self,event):
        selected = self.view.record_tree.focus()
        values = self.view.record_tree.item(selected,'values')

        if len(values) > 0:
            self.view.deceased_edit_entry_fname.delete(0,END)
            self.view.deceased_edit_entry_fname.insert(END,values[2])
            self.view.deceased_edit_entry_sname.insert(END,values[3])
            self.view.deceased_edit_entry_date.insert(END,values[4])
            self.view.deceased_edit_button["state"] = "normal"
    
    def refresh_section(self):
        self.view.section_list_tree.delete(*self.view.section_list_tree.get_children())
        self.display_section_names(self.model.get_section_names())
    
    def refresh_plots(self):
        selected = self.view.section_list_tree.focus()
        values = list(self.view.section_list_tree.item(selected,'values'))

        self.view.plot_tree.delete(*self.view.plot_tree.get_children())
        self.display_plot_owners(self.model.query_plot_owners(values[1]))
    
    def refresh_deceased(self):
        selected = self.view.plot_tree.focus()
        values = list(self.view.plot_tree.item(selected,'values'))

        self.view.record_tree.delete(*self.view.record_tree.get_children())
        self.display_deceased_records(self.model.query_deceased_by_id(values[0]))
    
    def check_date(self,input_date):
        try:
            return bool(datetime.strptime(input_date, "%d/%m/%Y"))
        except ValueError:
            return False
