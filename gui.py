#!/usr/bin/env python

import sys
import csv
import glob
from datetime import datetime

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
        
        # button frame
        btn_frame = tk.Frame(self, padx=10, pady=10)
        btn_frame.pack(side="left", fill="y")
        btn_frame.rowconfigure(0, weight=3)
        for idx in range(1, 7):
            btn_frame.rowconfigure(idx, weight=1)
        
        # add buttons
        # button: move items from input list to output list
        self.createButton(btn_frame, 0, 0, text="Move Right", command=self.move_right)
        # label: change category
        self.cat_label = tk.Label(btn_frame, text="Change category to:").grid(row=1, column=0, sticky="s")
        # button: change category to apartment
        self.createButton(btn_frame, 2, 0, text="Apartment", command=lambda: self.change_category("apartment"))
        # button: change category to food
        self.createButton(btn_frame, 3, 0, text="Food", command=lambda: self.change_category("food"))
        # button: export output list to csv
        self.createButton(btn_frame, 5, 0, text="Export to", command=self.export_all)
        # label: name of output file
        self.out_label = tk.Label(btn_frame, text='out.csv').grid(row=6, column=0, sticky="n")

    def createListbox(self, side="left"):
        """Function to create a tkinter Listbox."""
        
        # define listbox with multiple selection and scrollbars h/v
        listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, font="TkFixedFont")
        scrollbarH = tk.Scrollbar(listbox, orient="horizontal")
        scrollbarV = tk.Scrollbar(listbox, orient="vertical")
        
        # configure scrollbars and listbox so they know about each other
        scrollbarH.config(command=listbox.xview)
        scrollbarV.config(command=listbox.yview)
        listbox.config(xscrollcommand=scrollbarH.set, yscrollcommand=scrollbarV.set)
        
        # place the elements
        scrollbarH.pack(side="bottom", fill="x")
        scrollbarV.pack(side="right", fill="y")
        listbox.pack(side=side, fill="both", expand=True, padx=10, pady=10)
        
        return listbox
    
    def createButton(self, frame, row, col, text, command):
        """Function to add button for a particular command."""
        
        btn = tk.Button(frame, text=text, command=command)
        btn.grid(row=row, column=col)

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
            
    def change_category(self, category):
        """Change selected item category to provided category."""
        selections = self.listbox_out.curselection()
        for i in selections:
            entry = self.listbox_out.get(i)
            
            entry_items = entry.split(";")
            new_entry = entry_items[0] + ";" + entry_items[1] + ";" + \
                        str(category) + ";" + \
                        entry_items[3] + ";" + entry_items[4] + "; ;" + \
                        entry_items[6]
            
            # replace entry with formatted entry
            self.listbox_out.delete(i)
            self.listbox_out.insert(i, new_entry)
            
    def export_all(self):
        """Export items from output list to csv."""
        all_items = self.listbox_out.get(0, tk.END)
        
        f_out = self.out_label["text"]
        f = open(f_out, "w")
        for item in all_items:
            f.write(item + "\n")
        f.close()

### functions to handle the different formats for the input data

def readInputData(window):
    """Function to read data from file provided as CLI argument.
    Data is then used to populate the input listbox."""
    
    # get dir name from CLI args
    input_dir = sys.argv[1]
    files = glob.glob(f"{input_dir}/*.csv")
    files.extend(glob.glob(f"{input_dir}/*.CSV"))
    # add header with column descriptions
    window.listbox_in.insert(tk.END, "Date - Description - Category - Amount")
    for input_file in files[:3]:
        print(input_file)
        # import data using csv module
        with open(input_file) as fin:
            csv_reader = csv.reader(fin, delimiter=',', quotechar='"')
            header = " - ".join(next(csv_reader))
            for row in csv_reader:
                # skip the autopay lines and empty line
                if ("autopay" in " ".join(row).lower()) or (len(row) == 0):
                    continue
                # format row depending on csv header info
                new_row = formatRow(row, header=header)
                # create one long string per row
                concat_row = " - ".join(new_row)
                # add to list A
                window.listbox_in.insert(tk.END, concat_row)
        # add a line to separate between the different data sources
        window.listbox_in.insert(tk.END, "-" * 100)
    # fix last line not showing properly
    window.listbox_in.insert(tk.END, "")

def formatRow(row, header):
    """Function to format a row given the header of the input csv file."""
    
    # max lengths for various entries
    desc_len, cat_len = 42, 14
    # use header to decide what info is contained in row
    if header == "Date - Description - Amount":
        # change the date to yyyy-mm-dd format
        date = datetime.strptime(row[0], "%m/%d/%Y").strftime("%Y-%m-%d")
        row[0] = date
        # add a default category
        row.insert(2, "food")
    elif header == "Transaction Date - Posted Date - Card No. - Description - Category - Debit - Credit":
        # print(new_row)
        idx = [0, 3, 4, 5]
        row = [row[id] for id in idx]
    # set max length for description
    if len(row[1]) < desc_len:
        row[1] = row[1].ljust(desc_len)
    # set max length for category
    if len(row[2]) < cat_len:
        row[2] = row[2].ljust(cat_len)
    
    return row


# run the main tkinter loop
window = Window()
readInputData(window)
window.mainloop()
