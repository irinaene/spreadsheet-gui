#!/usr/bin/env python

import sys
import csv

# import tkinter depends on py version
if sys.version_info.major > 2:
    import tkinter as tk
else:
    import Tkinter as tk

# start the widgets
master = tk.Tk()
master.geometry('1000x500')

# define list A and scrollbars h/v
listboxA = tk.Listbox(master, selectmode=tk.MULTIPLE)
scrollbarA = tk.Scrollbar(listboxA, orient="horizontal")
scrollbarAA = tk.Scrollbar(listboxA, orient="vertical")
# config scroll and list so they know about each other
scrollbarA.config(command=listboxA.xview)
scrollbarAA.config(command=listboxA.yview)
listboxA.config(xscrollcommand=scrollbarA.set, yscrollcommand=scrollbarAA.set)
# place the elems
scrollbarA.pack(side="bottom", fill="x")
scrollbarAA.pack(side="right", fill="y")
listboxA.pack(side="left",fill="both", expand=True)

# define list B and scrollbars h/v
listboxB = tk.Listbox(master, selectmode=tk.MULTIPLE)
scrollbarB = tk.Scrollbar(listboxB, orient="horizontal",)
scrollbarBB = tk.Scrollbar(listboxB, orient="vertical",)
# config scroll and list so they know about each other
scrollbarB.config(command=listboxB.xview)
scrollbarBB.config(command=listboxB.yview)
listboxB.config(xscrollcommand=scrollbarB.set, yscrollcommand=scrollbarBB.set)
# place the elems
scrollbarB.pack(side="bottom", fill="x")
scrollbarBB.pack(side="right", fill="y")
listboxB.pack(side="right",fill="both", expand=True)

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

# button: move items to right list
moveBtn = tk.Button(master, text="Move Right", command=moveDown)
moveBtn.pack(side="top",expand=True)
# button: change category to apartment
aptBtn = tk.Button(master, text="Apartment", command=add_apt)
aptBtn.pack(side="top", expand=True)
# button: export all to csv
expBtn = tk.Button(master, text="Export", command=export_all)
expBtn.pack(side="bottom", expand=True)

## read input data
# read the data file into a list
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

# populate list A
#for item in chem_list[1:]:
#    listboxA.insert(tk.END, item)
    
# run the main tkinter loop  
master.mainloop()

