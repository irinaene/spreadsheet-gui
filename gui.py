#!/usr/bin/env python

import sys
import csv

# import tkinter depends on py version
if sys.version_info.major > 2:
    import tkinter as tk
else:
    import Tkinter as tk

# start the widgets
window = tk.Tk()
window.geometry('1000x500')
window.title('Spreadsheet GUI')

def createListbox(side="left"):
    """Function to create a tkinter Listbox."""
    
    # define listbox with multiple selection and scrollbars h/v
    listbox = tk.Listbox(window, selectmode=tk.MULTIPLE)
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

# create listbox
listboxA = createListbox(side="left")
listboxB = createListbox(side="right")

def moveDown():
    '''move items from list A to list B'''
    selections = listboxA.curselection()
    for i in selections:
        entry = listboxA.get(i)
        
        entry_items = entry.split(";")
        new_entry = '"' + entry_items[1] + '"' + ";" + entry_items[0] + ";food;" + \
                    entry_items[4] + ";" + entry_items[3] + "; ;" + \
                    entry_items[3]

        # add formated entry to list B
        listboxB.insert(tk.END, new_entry)

    # delete selected items from list A by sorting indeces in reverse order
    reversed_selections = selections[::-1]
    for item in reversed_selections:
        listboxA.delete(item)
        
def add_apt():
    '''change category from food to apartment'''
    selections = listboxB.curselection()
    for i in selections:
        entry = listboxB.get(i)
        
        entry_items = entry.split(";")
        new_entry = entry_items[0] + ";" + entry_items[1] + ";" + \
                    "apartment" + ";" + \
                    entry_items[3] + ";" + entry_items[4] + "; ;" + \
                    entry_items[6]
        
        # replace entry with formatted entry
        listboxB.delete(i)
        listboxB.insert(i, new_entry)
        
        
def export_all():
    '''move all items from list B to csv'''
    all_items = listboxB.get(0, tk.END)
    
    f = open('out.csv', "w")
    for item in all_items:
        f.write(item + "\n")
    f.close()

def createButton(text, command, side):
    """Function to add button for a particular command."""
    
    btn = tk.Button(window, text=text, command=command)
    btn.pack(side=side, expand=True)

# add button: move items from input list to output list
createButton(text="Move Right", command=moveDown, side="top")
# add button: change category to apartment
createButton(text="Apartment", command=add_apt, side="top")
# add button: export output list to csv
createButton(text="Export", command=export_all, side="bottom")

def readInputData():
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
            listboxA.insert(tk.END, concat_row)

# populate the input listbox
readInputData()
    
# run the main tkinter loop  
window.mainloop()
