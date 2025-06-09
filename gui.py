#!/usr/bin/env python

import sys
import csv

# import tkinter depends on py version
if sys.version_info.major > 2:
    import tkinter as tk
else:
    import Tkinter as tk


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # set window properties
        self.geometry('1000x500')
        self.title('Spreadsheet GUI')
        
        # create input and output lists
        self.listbox_in = self.createListbox(side="left")
        self.listbox_out = self.createListbox(side="right")
        
        # add buttons
        # button: move items from input list to output list
        self.createButton(text="Move Right", command=self.move_right, side="top")
        # button: change category to apartment
        self.createButton(text="Apartment", command=self.add_apt, side="top")
        # button: export output list to csv
        self.createButton(text="Export", command=self.export_all, side="bottom")
        
        # populate the input listbox
        self.readInputData()

    def createListbox(self, side="left"):
        """Function to create a tkinter Listbox."""
        
        # define listbox with multiple selection and scrollbars h/v
        listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        scrollbarH = tk.Scrollbar(listbox, orient="horizontal")
        scrollbarV = tk.Scrollbar(listbox, orient="vertical")
        
        # configure scrollbars and listbox so they know about each other
        scrollbarH.config(command=listbox.xview)
        scrollbarV.config(command=listbox.yview)
        listbox.config(xscrollcommand=scrollbarH.set, yscrollcommand=scrollbarV.set)
        
        # place the elements
        scrollbarH.pack(side="bottom", fill="x")
        scrollbarV.pack(side="right", fill="y")
        listbox.pack(side=side, fill="both", expand=True)
        
        return listbox
    
    def createButton(self, text, command, side):
        """Function to add button for a particular command."""
        
        btn = tk.Button(self, text=text, command=command)
        btn.pack(side=side, expand=True)

    def move_right(self):
        """Move items from input list to output list."""
        selections = self.listbox_in.curselection()
        for i in selections:
            entry = self.listbox_in.get(i)
            
            entry_items = entry.split(";")
            new_entry = '"' + entry_items[1] + '"' + ";" + entry_items[0] + ";food;" + \
                        entry_items[4] + ";" + entry_items[3] + "; ;" + \
                        entry_items[3]

            # add formated entry to output list
            self.listbox_out.insert(tk.END, new_entry)

        # delete selected items from input list by sorting indeces in reverse order
        reversed_selections = selections[::-1]
        for item in reversed_selections:
            self.listbox_in.delete(item)
            
    def add_apt(self):
        """Change selected item category from food to apartment."""
        selections = self.listbox_out.curselection()
        for i in selections:
            entry = self.listbox_out.get(i)
            
            entry_items = entry.split(";")
            new_entry = entry_items[0] + ";" + entry_items[1] + ";" + \
                        "apartment" + ";" + \
                        entry_items[3] + ";" + entry_items[4] + "; ;" + \
                        entry_items[6]
            
            # replace entry with formatted entry
            self.listbox_out.delete(i)
            self.listbox_out.insert(i, new_entry)
            
    def export_all(self):
        """Export items from output list to csv."""
        all_items = self.listbox_out.get(0, tk.END)
        
        f = open('out.csv', "w")
        for item in all_items:
            f.write(item + "\n")
        f.close()
    
    def readInputData(self):
        """Function to read data from file provided as CLI argument.
        Data is then used to populate the input listbox."""
        
        # get file name from CLI args
        input_file = sys.argv[1]
        # import data using csv module
        with open(input_file) as fin:
            csv_reader = csv.reader(fin, delimiter=',', quotechar='"')
            for row in csv_reader:
                # create one long string per row
                concat_row = ''
                for elem in row:
                    concat_row += elem + ";"
                # add to list A
                self.listbox_in.insert(tk.END, concat_row)


# run the main tkinter loop
window = Window()
window.mainloop()
