"""Define the GUI windows class using TKinter."""

import os
import sys
from datetime import datetime

# import tkinter depends on py version
if sys.version_info.major > 2:
    import tkinter as tk
    from tkinter import font, messagebox, ttk
else:
    import Tkinter as tk
    from TKinter import messagebox, ttk


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # set window properties
        width, height = 1700, 800
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.title('Spreadsheet GUI')
        
        # set some default max display lengths for list items
        self.desc_len = 30
        self.cat_len = 10
        
        # create frames to hold the widgets
        self.in_frame = ttk.Frame(self)
        self.btn_frame = ttk.Frame(self)
        self.out_frame = ttk.Frame(self)
        self.in_frame.place(relx=0.01, rely=0.01, relwidth=0.42, relheight=0.98)
        self.btn_frame.place(relx=0.45, rely=0.125, relwidth=0.1, relheight=0.75)
        self.out_frame.place(relx=0.57, rely=0.01, relwidth=0.42, relheight=0.98)
        
        # create input and output lists
        self.list_in = []
        self.listvar_in = tk.StringVar(value=self.list_in)
        self.listbox_in = self.createListbox(self.in_frame, listvar=self.listvar_in)
        self.list_out = []
        self.listvar_out = tk.StringVar(value=self.list_out)
        self.listbox_out = self.createListbox(self.out_frame, listvar=self.listvar_out)
        
        # add buttons
        # button: move items from input list to output list
        self.createButton(self.btn_frame, relx=0.5, rely=0.05, text="Move Right", command=self.move_items_dir)
        # button: move items from output list back to input list
        self.createButton(self.btn_frame, relx=0.5, rely=0.15, text="Move Left", command=lambda: self.move_items_dir(direction="out_to_in"))
        # # button: clear selection from input list
        # self.createButton(self.btn_frame, 0.5, 0.25, text="Clear selection", command=self.clear_selection)
        # separator
        sep1 = ttk.Separator(self.btn_frame, orient="horizontal")
        sep1.place(relx=0, rely=0.3, relwidth=1.)
        # label: change category
        self.cat_label = tk.Label(self.btn_frame, text="Change category to:")
        self.cat_label.place(relx=0.5, rely=0.35, anchor="center")
        # button: change category to apartment
        self.createButton(self.btn_frame, 0.5, 0.45, text="Apartment", command=lambda: self.change_category("Apartment"))
        # button: change category to food
        self.createButton(self.btn_frame, 0.5, 0.55, text="Food", command=lambda: self.change_category("Food"))
        # button: change category to rent
        self.createButton(self.btn_frame, 0.5, 0.65, text="Rent", command=lambda: self.change_category("Rent"))
        # button: change category to monthly gift
        self.createButton(self.btn_frame, 0.5, 0.75, text="Monthly Gift", command=lambda: self.change_category("Monthly Gift"))
        # separator
        sep2 = ttk.Separator(self.btn_frame, orient="horizontal")
        sep2.place(relx=0, rely=0.8, relwidth=1.)
        # label: name of output file
        self.out_label = tk.Label(self.btn_frame, text='Export to: out.csv', wraplength=160)
        self.out_label.place(relx=0.5, rely=0.85, anchor="center")
        # button: export output list to csv
        self.createButton(self.btn_frame, 0.5, 0.9, text="Export", command=self.export_with_confirmation)

    def createListbox(self, frame, listvar=None):
        """Function to create a tkinter Listbox."""
        
        # define listbox with multiple selection and scrollbars h/v
        lb_font = font.Font(family="Courier", size=12)  # default font, mono spaced
        listbox = tk.Listbox(frame, selectmode=tk.EXTENDED, font=lb_font, listvariable=listvar)
        scrollbarH = tk.Scrollbar(listbox, orient="horizontal")
        scrollbarV = tk.Scrollbar(listbox, orient="vertical")
        
        # configure scrollbars and listbox so they know about each other
        scrollbarH.config(command=listbox.xview)
        scrollbarV.config(command=listbox.yview)
        listbox.config(xscrollcommand=scrollbarH.set, yscrollcommand=scrollbarV.set)
        
        # place the elements
        scrollbarH.pack(side="bottom", fill="x")
        scrollbarV.pack(side="right", fill="y")
        # place listbox to cover the whole frame
        listbox.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        return listbox
    
    def createButton(self, frame, relx, rely, text, command):
        """Function to add button for a particular command."""
        
        btn = tk.Button(frame, text=text, command=command)
        btn.place(relx=relx, rely=rely, anchor="center")

    def move_items(self, selection, left_lst, right_lst, sort_right_lst=False):
        """Move selected items (as given by selection) from left list to right list.
        Optionally sorts the right list."""
        
        # before adding any items, remove the empty line at the end
        if len(right_lst) > 0:
            right_lst.pop()
        # subselect rows that can be moved (e.g. not header, not separator line)
        allowed_sel = []
        for i in selection:
            if (left_lst[i] == "") or (left_lst[i][:4] in ["Date", "----"]):
                continue
            allowed_sel.append(i)
        # move allowed items
        for i in allowed_sel:
            right_lst.append(left_lst[i])
        # sort the rows by date, only if moving from in to out
        if sort_right_lst:
            right_lst.sort(key=lambda x: x[:10], reverse=False)
        # fix last line not showing properly b/c of scrollbar
        right_lst.append("")
        # delete selected items from left list by sorting indices in reverse order
        for item in allowed_sel[::-1]:
            left_lst.pop(item)
    
    def move_items_dir(self, direction="in_to_out"):
        """Moves items from input listbox to output listbox or vice versa."""
        
        # define the two allowed directions
        if direction == "in_to_out":
            left_lb = self.listbox_in
            left_lst = self.list_in
            left_lvar = self.listvar_in
            right_lst = self.list_out
            right_lvar = self.listvar_out
            sort_right_lst = True
        elif direction == "out_to_in":
            left_lb = self.listbox_out
            left_lst = self.list_out
            left_lvar = self.listvar_out
            right_lst = self.list_in
            right_lvar = self.listvar_in
            sort_right_lst = False
        else:
            print("Unsupported direction provided to move_items_dir, please double check!")
            return
        
        # move the selected items
        self.move_items(left_lb.curselection(), left_lst, right_lst, sort_right_lst=sort_right_lst)
        
        # post-processing: update the StringVars to propagate changes to ListBoxes
        left_lvar.set(left_lst)
        right_lvar.set(right_lst)
        
        # clear the current selection to start fresh for the next move
        left_lb.select_clear(0, tk.END)
        
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
            old_cat = entry_items[2].strip()
            # change the category field only if new value is different from old value
            if category != old_cat:
                entry_items[2] = category.ljust(self.cat_len)
                new_entry = " | ".join(entry_items)
                # replace entry with formatted entry
                self.list_out[i] = new_entry
        # update the StringVar
        self.listvar_out.set(self.list_out)
            
    def export_all(self, f_out):
        """Export items from output list to csv file f_out."""
        
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
        # print(f"Exported data to file: {f_out}")
    
    def export_with_confirmation(self):
        """Export items to csv using a confirmation box for overwriting."""
        
        f_out = self.out_label["text"].split(":")[1].strip()
        # check if file exists
        if os.path.exists(f_out):
            title = "Confirmation"
            msg = f"The file {f_out} already exists. Do you want to overwrite it?"
            # pop overwrite window
            response = messagebox.askyesno(title, msg, parent=self)
        # export if file doesn't exist or response is yes
        if not os.path.exists(f_out) or response:
            self.export_all(f_out)
    
    def importData(self, list_in, format_dict):
        """Function to import data contained in list_in into the input listbox."""
        
        # update the relevant data list
        self.list_in = list_in
        # update the relevant StringVar
        self.listvar_in.set(self.list_in)
        # update the max lengths for display of fields
        self.desc_len = format_dict['desc_len']
        self.cat_len = format_dict['cat_len']
