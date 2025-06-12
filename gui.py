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
        self.geometry('1600x800+300+300')
        self.title('Spreadsheet GUI')
        
        # set max lengths for output formatting of the fields
        self.desc_len = 50  # max len for description field
        self.cat_len = 20  # max len for category field
        
        # create input and output lists
        self.list_in = []
        self.listvar_in = tk.StringVar(value=self.list_in)
        self.listbox_in = self.createListbox(side="left", listvar=self.listvar_in)
        self.list_out = []
        self.listvar_out = tk.StringVar(value=self.list_out)
        self.listbox_out = self.createListbox(side="right", listvar=self.listvar_out)
        
        # button frame
        btn_frame = tk.Frame(self, padx=10, pady=10)
        btn_frame.pack(side="left", fill="y")
        for idx in range(0, 10):
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
        # button: change category to rent
        self.createButton(btn_frame, 6, 0, text="Rent", command=lambda: self.change_category("Rent"))
        # button: change category to monthly gift
        self.createButton(btn_frame, 7, 0, text="Monthly Gift", command=lambda: self.change_category("Monthly Gift"))
        # button: export output list to csv
        self.createButton(btn_frame, 8, 0, text="Export to", command=self.export_all)
        # label: name of output file
        self.out_label = tk.Label(btn_frame, text='out.csv')
        self.out_label.grid(row=9, column=0, sticky="n")

    def createListbox(self, side="left", listvar=None):
        """Function to create a tkinter Listbox."""
        
        # define listbox with multiple selection and scrollbars h/v
        listbox = tk.Listbox(self, selectmode=tk.EXTENDED, font="TkFixedFont", listvariable=listvar)
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
        
        # define the two directions, left and right
        if left == "in":
            # moves right, from in to out
            left_lb = self.listbox_in
            left_lst = self.list_in
            left_lvar = self.listvar_in
            right_lst = self.list_out
            right_lvar = self.listvar_out
        else:
            # moves left, from out to in
            left_lb = self.listbox_out
            left_lst = self.list_out
            left_lvar = self.listvar_out
            right_lst = self.list_in
            right_lvar = self.listvar_in
        
        if len(right_lst) > 0:
            right_lst.pop()
        # subselect rows that can be moved (e.g. not header, not separator line)
        allowed_sel = []
        for i in left_lb.curselection():
            if (left_lst[i] == "") or (left_lst[i][:4] in ["Date", "----"]):
                continue
            allowed_sel.append(i)
        # move allowed items
        for i in allowed_sel:
            right_lst.append(left_lst[i])
        # sort the rows by date only for list_out
        if left == "in":
            right_lst.sort(key=lambda x: x[:10], reverse=False)
        # fix last line not showing properly b/c of scrollbar
        right_lst.append("")
        # update the StringVar
        right_lvar.set(right_lst)
        
        # delete selected items from input list by sorting indices in reverse order
        for item in allowed_sel[::-1]:
            left_lst.pop(item)
        # update the StringVar
        left_lvar.set(left_lst)
        
    def clear_selection(self):
        """Clears the current selection of the input listbox."""
        
        self.listbox_in.selection_clear(0, tk.END)
            
    def change_category(self, category):
        """Change selected item category to provided category.
        Applies only to items in the output list."""
        
        selections = self.listbox_out.curselection()
        for i in selections:
            entry = self.list_out[i]
            entry_items = entry.split(" | ")
            # change the category field
            entry_items[2] = category.ljust(self.cat_len)
            new_entry = " | ".join(entry_items)
            # replace entry with formatted entry
            self.list_out[i] = new_entry
        # update the StringVar
        self.listvar_out.set(self.list_out)
            
    def export_all(self):
        """Export items from output list to csv."""
        
        f_out = self.out_label["text"]
        # map between order of fields in listbox and in output file
        field_map = {0: 1, 1: 0, 2: 2, 4: 3, 6: 3}
        
        all_items = self.listbox_out.get(0, tk.END)[:-1]  # last item is empty line
        with open(f_out, "w") as f:
            for item in all_items:
                fields = item.split(" | ")
                fields = [field.strip() for field in fields]
                # construct list with new fields to write in output file
                new_fields = [""] * 7
                for k in field_map:
                    new_fields[k] = fields[field_map[k]]
                ## postprocessing
                # add default value for purchase method
                new_fields[3] = "cc"
                # change date format
                date = datetime.strptime(new_fields[1], "%Y-%m-%d").strftime("%m/%d/%Y")
                new_fields[1] = date
                # fix sign for amount fields
                for i in [4, 6]:
                    new_fields[i] = f"{-1 * float(new_fields[i]):.2f}"
                # special case: monthly gift
                if new_fields[2] == "Monthly Gift":
                    new_fields[6] = ""
                new_entry = ",".join(new_fields)
                f.write(new_entry + "\n")
        print(f"Exported data to file: {f_out}")

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
    window.list_in.append(header_line)
    # define separator line between different files
    sep_line = "-" * 10 + "-|-" + "-" * window.desc_len + "-|-" + "-" * window.cat_len + "-|-" + "-" * 11
    window.list_in.append(sep_line)
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
                window.list_in.append(concat_row)
        # add a line to separate between the different data sources
        window.list_in.append(sep_line)
    # fix last line not showing properly b/c of scrollbar
    window.list_in.append("")
    # update the StringVar
    window.listvar_in.set(window.list_in)

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
