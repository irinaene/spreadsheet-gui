#!/usr/bin/env python

import tkinter as tk
import sys

# start the widgets
master = tk.Tk()
master.geometry('1000x500')

listboxA = tk.Listbox(master, selectmode=tk.MULTIPLE)
scrollbarA = tk.Scrollbar(listboxA, orient="horizontal")

# config scroll and list so they know about each other
scrollbarA.config(command=listboxA.xview)
listboxA.config(xscrollcommand=scrollbarA.set)

scrollbarA.pack(side="bottom", fill="x")
listboxA.pack(side="left",fill="both", expand=True)

listboxB = tk.Listbox(master, selectmode=tk.MULTIPLE)
scrollbarB = tk.Scrollbar(listboxB, orient="horizontal",)
# config scroll and list so they know about each other
scrollbarB.config(command=listboxB.xview)
listboxB.config(xscrollcommand=scrollbarB.set)
scrollbarB.pack(side="bottom", fill="x")
listboxB.pack(side="right",fill="both", expand=True)

def moveDown():
    '''move items from list A to list B'''
    selections = listboxA.curselection()
    for i in selections:
        entry = listboxA.get(i)
        
        entry_items = entry.split(",")
        new_entry = entry_items[1] + "," + entry_items[0] + ",food," + \
                    entry_items[4] + "," + entry_items[3] + ", ," + \
                    entry_items[3]

        # add formated entry to list B
        listboxB.insert(tk.END, new_entry)

    # delete selected items from list A by sorting indeces in reverse order
    reversed_selections = selections[::-1]
    for item in reversed_selections:
        listboxA.delete(item)
        
def add_apt():
    '''test'''
    selections = listboxB.curselection()
    for i in selections:
        entry = listboxB.get(i)
        
        entry_items = entry.split(",")
        new_entry = entry_items[0] + "," + entry_items[1] + "," + \
                    "apartment" + "," + \
                    entry_items[3] + "," + entry_items[4] + ", ," + \
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
# fin = open("transactions.csv", "r")
input_file = sys.argv[1]
fin = open(input_file, "r")
chem_list = fin.readlines()
fin.close()
# strip the trailing newline char
chem_list = [chem.rstrip() for chem in chem_list]

# populate list A
for item in chem_list[1:]:
    listboxA.insert(tk.END, item)
    
# run the main tkinter loop  
master.mainloop()

