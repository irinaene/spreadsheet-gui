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
        
        # set max lengths for output formatting of the fields
        self.desc_len = 50  # max len for description field
        self.cat_len = 20  # max len for category field
        
        # create input and output lists
        self.listbox_in = self.createListbox(side="left")
        self.listbox_out = self.createListbox(side="right")
        
        # button frame
        btn_frame = tk.Frame(self, padx=10, pady=10)
        btn_frame.pack(side="left", fill="y")
        for idx in range(0, 9):
            btn_frame.rowconfigure(idx, weight=1)
        
        # add buttons
        # button: move items from input list to output list
        self.createButton(btn_frame, 0, 0, text="Move Right", command=self.move_items)
        # button: move items from output list back to input list
        self.createButton(btn_frame, 1, 0, text="Move Left", command=lambda: self.move_items(left="out"))
        # button: clear selection from input list
        self.createButton(btn_frame, 2, 0, text="Clear selection", command=self.clear_selection)
        # label: change category
        self.cat_label = tk.Label(btn_frame, text="Change category to:").grid(row=3, column=0, sticky="s")
        # button: change category to apartment
        self.createButton(btn_frame, 4, 0, text="Apartment", command=lambda: self.change_category("Apartment"))
        # button: change category to food
        self.createButton(btn_frame, 5, 0, text="Food", command=lambda: self.change_category("Food"))
        # button: export output list to csv
        self.createButton(btn_frame, 7, 0, text="Export to", command=self.export_all)
        # label: name of output file
        self.out_label = tk.Label(btn_frame, text='out.csv').grid(row=8, column=0, sticky="n")

    def createListbox(self, side="left"):
        """Function to create a tkinter Listbox."""
        
        # define listbox with multiple selection and scrollbars h/v
        listbox = tk.Listbox(self, selectmode=tk.EXTENDED, font="TkFixedFont")
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

    def move_items(self, left="in"):
        """Move items from left listbox to right listbox."""
        
        # define the two lists
        left_lst = self.listbox_in if left == "in" else self.listbox_out
        right_lst = self.listbox_out if left == "in" else self.listbox_in
        
        right_lst.delete(tk.END)
        selections = left_lst.curselection()
        for i in selections:
            entry = left_lst.get(i)
            # add formated entry to output list
            right_lst.insert(tk.END, entry)
        # fix last line not showing properly b/c of scrollbar
        right_lst.insert(tk.END, "")

        # delete selected items from input list by sorting indeces in reverse order
        reversed_selections = selections[::-1]
        for item in reversed_selections:
            left_lst.delete(item)
    
    def clear_selection(self):
        """Clears the current selection of the input listbox."""
        
        self.listbox_in.selection_clear(0, tk.END)
            
    def change_category(self, category):
        """Change selected item category to provided category."""
        
        selections = self.listbox_out.curselection()
        for i in selections:
            entry = self.listbox_out.get(i)
            
            entry_items = entry.split(" | ")
            # change the category field
            entry_items[2] = category.ljust(self.cat_len)
            new_entry = " | ".join(entry_items)
            
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
    # get all relevant files from input_dir
    files = glob.glob(f"{input_dir}/*.csv")
    files.extend(glob.glob(f"{input_dir}/*.CSV"))
    # add header with column descriptions, nicely formatted
    c1 = "Date".ljust(10)
    c2 = "Description".ljust(window.desc_len)
    c3 = "Category".ljust(window.cat_len)
    header_line = f"{c1} | {c2} | {c3} | Amount"
    window.listbox_in.insert(tk.END, header_line)
    # define separator line between different files
    # desc_len, cat_len = 50, 20  # max lengths for various entries
    sep_line = "-" * 10 + "-|-" + "-" * window.desc_len + "-|-" + "-" * window.cat_len + "-|-" + "-" * 11
    window.listbox_in.insert(tk.END, sep_line)
    for input_file in files:
        print(input_file)
        # import data using csv module
        with open(input_file) as fin:
            csv_reader = csv.reader(fin, delimiter=',', quotechar='"')
            header = ",".join(next(csv_reader))
            for row in csv_reader:
                row_str = " ".join(row).lower()
                # skip the autopay lines and empty line
                if ("autopay" in row_str) or ("automatic payment" in row_str) or (len(row) == 0):
                    continue
                # format row depending on csv header info
                new_row = formatRow(row, header=header, desc_len=window.desc_len, cat_len=window.cat_len)
                # create one long string per row
                concat_row = " | ".join(new_row)
                # add to input listbox
                window.listbox_in.insert(tk.END, concat_row)
        # add a line to separate between the different data sources
        window.listbox_in.insert(tk.END, sep_line)
    # fix last line not showing properly b/c of scrollbar
    window.listbox_in.insert(tk.END, "")

def formatRow(row, header, desc_len, cat_len):
    """Function to format a row given the header of the input csv file."""
    
    # use header to decide what info is contained in row
    if header == "Date,Description,Amount":
        # change the date to yyyy-mm-dd format
        date = datetime.strptime(row[0], "%m/%d/%Y").strftime("%Y-%m-%d")
        row[0] = date
        # add a default category
        row.insert(2, "Food")
        # amount: ensure consistent signs, debit -, credit +
        row[3] = f"{-1 * float(row[3]):.2f}"
    elif header == "Transaction Date,Posted Date,Card No.,Description,Category,Debit,Credit":
        idx = [0, 3, 4, 5, 6]
        row = [row[id] for id in idx]
        # amount: ensure consistent signs, debit -, credit +
        if row[3] == "":
            row[3] = row[4]
        else:
            row[3] = f"{-1 * float(row[3]):.2f}"
        # remove credit info
        row.pop(len(row) - 1)
    elif header == "Details,Posting Date,Description,Amount,Type,Balance,Check or Slip #":
        idx = [1, 2, 3]
        row = [row[id] for id in idx]
        # change the date to yyyy-mm-dd format
        date = datetime.strptime(row[0], "%m/%d/%Y").strftime("%Y-%m-%d")
        row[0] = date
        # add a default category
        row.insert(2, "Food")
    elif header == "Transaction Date,Post Date,Description,Category,Type,Amount,Memo":
        idx = [0, 2, 3, 5]
        row = [row[id] for id in idx]
        # change the date to yyyy-mm-dd format
        date = datetime.strptime(row[0], "%m/%d/%Y").strftime("%Y-%m-%d")
        row[0] = date
    # set max length for description
    if len(row[1]) < desc_len:
        row[1] = row[1].ljust(desc_len)
    else:
        row[1] = row[1][:desc_len]
    # set max length for category
    if len(row[2]) < cat_len:
        row[2] = row[2].ljust(cat_len)
    else:
        row[2] = row[2][:cat_len]
    
    return row


# run the main tkinter loop
window = Window()
readInputData(window)
window.mainloop()
