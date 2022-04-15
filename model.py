import sqlite3
import os
import datetime
database_location = os.path.join(os.getcwd(),"Database","cemetery.db")

class Model:
    def __init__(self):
        self.conn = sqlite3.connect(database_location)
        self.c = self.conn.cursor()

    #create the tables if they don't exist.
    def create_tables(self):
        self.conn = sqlite3.connect(database_location)
        self.c = self.conn.cursor()

        self.create_sections_table = """CREATE TABLE IF NOT EXISTS sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                plot_name TEXT
            )"""
        self.c.execute(self.create_sections_table)
        self.conn.commit()
        
        create_plots_table = """CREATE TABLE IF NOT EXISTS plots (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                plot_owner TEXT,
                plot_section TEXT,
                plot_number INTEGER
            )"""
        self.c.execute(create_plots_table)
        self.conn.commit()

        self.create_deceased_table = """CREATE TABLE IF NOT EXISTS deceased (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                plot_id INTEGER,
                fname TEXT,
                sname TEXT,
                dod DATE
            )"""
        self.c.execute(self.create_deceased_table)
        self.conn.commit()

    def create_section(self,name):
        with self.conn:
            self.c.execute("INSERT INTO sections VALUES(Null,?)",[name])
            self.conn.commit()

    def create_plot(self,owner,section,number):
        with self.conn:
            self.c.execute("INSERT INTO plots VALUES(Null,?,?,?)", (owner, section, number))
            self.conn.commit()

    def create_deceased(self,plot,fname,sname,dod):
        with self.conn:
            self.c.execute("INSERT INTO deceased VALUES(Null,?,?,?,?)", (plot,fname, sname, dod))
            self.conn.commit()
        
    def section_lookup(self,section_id):
        with self.conn:
        ##section info
            self.c.execute("SELECT * from sections WHERE id = (?)", (section_id, ))
            self.items = self.c.fetchall()
            print(self.items[0][0])

        ##deceased info
            self.c.execute("SELECT fname,sname from deceased WHERE plot_id = (?)", (section_id, ))
            self.items = self.c.fetchall()
        
            for item in self.items:
                print(item)
        
            self.conn.commit()
            self.conn.close()

    def get_section_names(self):
        with self.conn:
            ##plot info
            self.c.execute("SELECT * FROM sections ORDER BY plot_name COLLATE NOCASE")
            return(self.c.fetchall())

    def update_section_name(self,id,old,new):
        with self.conn:
            self.c.execute("UPDATE sections SET plot_name = ? WHERE id = ?",(new,id))
            self.c.execute("UPDATE plots SET plot_section = ? WHERE plot_section = ?",(new,old))

    def update_plot(self,id,owner,section,number):
        print(str(id) + " " + owner + " " + section + " "+ str(number))
        with self.conn:
            self.c.execute("UPDATE plots SET plot_owner = ? WHERE id = ?",(owner,id))
            self.c.execute("UPDATE plots SET plot_section = ? WHERE id = ?",(section,id))
            self.c.execute("UPDATE plots SET plot_number = ? WHERE id = ?",(number,id))

    def update_deceased(self,id,fname,sname,date):
        print(str(id) + " " + fname + " " + sname + " "+ str(date))
        with self.conn:
            self.c.execute("UPDATE deceased SET fname = ? WHERE id = ?",(fname,id))
            self.c.execute("UPDATE deceased SET sname = ? WHERE id = ?",(sname,id))
            self.c.execute("UPDATE deceased SET dod = ? WHERE id = ?",(date,id))

    def query_plot_owners(self,value):
        with self.conn:
            if(value == "All"):
                self.c.execute("SELECT * FROM plots ORDER BY plot_section ASC, plot_number ASC;")
                return(self.c.fetchall())
            else:
                self.c.execute("SELECT * FROM plots WHERE plot_section = ? ORDER BY plot_section ASC, plot_number ASC;", (value,))
                return(self.c.fetchall())

    def query_plot(self,section,number):
        with self.conn:
            self.c.execute("SELECT * FROM plots WHERE plot_section = ? AND plot_number = ? ORDER BY plot_section COLLATE NOCASE", (section,number))
            return(self.c.fetchall())

    def query_plot_number(self,value):
        with self.conn:
            self.c.execute("SELECT * FROM plots WHERE plot_number = ?", (value,))
            return(self.c.fetchall())

    def query_deceased_by_id(self,id):
        with self.conn:
            self.c.execute("SELECT * FROM deceased WHERE plot_id=?",(id,))
            return self.c.fetchall()
