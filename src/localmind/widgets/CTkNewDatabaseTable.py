# CTkNewDatabaseTable

import customtkinter as ctk # type: ignore
from customtkinter import CTkFont # type: ignore
import tkinter as tk # type: ignore
from typing import Union, Tuple, Optional

class CTkNewDatabaseTable(ctk.CTkToplevel):
    def __init__(self, parent: ctk.CTk,  font: Optional[Union[ctk.CTkFont, Tuple[str, int, str]]]=None) -> None:
        super().__init__(parent)
        
        self.result : str = ""  # Store the result here (True for Yes, False for No)
        self.transient(parent)
        self.title("New Database Table")
        self.geometry("400x200")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.grid_rowconfigure(1, weight=1)
        self.font = font
        if self.font is None:
            self.font = ctk.CTkFont(family="Arial", size=12)
        self.initialize_widgets()
        self.center_on_parent(parent)
        # self.after(200, self.focus_on_text_box)
        self.protocol("WM_DELETE_WINDOW", self.cancel_clicked)  # Treat window close as 'No'
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def labeled_frame(self, parent, label: str, parent_row: int, parent_column: int, columns: int, columnspan: int=1) -> ctk.CTkFrame:

        frame_outer = ctk.CTkFrame(parent)
        frame_outer.grid(row=parent_row, column=parent_column, columnspan=columnspan, padx=10, pady=10, sticky='ew')
        frame_outer.grid_columnconfigure(0, weight=1)
        ctk_label = ctk.CTkLabel(frame_outer, text=label, font=self.font)
        ctk_label.grid(row=0, column=0, padx = 5, pady=5, sticky='ew')
        frame_inner = ctk.CTkFrame(frame_outer)
        frame_inner.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        column_configure = [x for x in range(columns)]
        frame_inner.grid_columnconfigure(column_configure, weight=1)
        return frame_inner

    def initialize_widgets(self) -> None:
        """ Initialize the widgets for the dialog """
        self.label = ctk.CTkLabel(self, text="Create a new database table?", font=self.font)
        self.label.grid(row=0, column=0, padx=20, pady=20)
        # create a labeled frames for the table name and description
        self.table_name_frame = self.labeled_frame(self, "Table Name", 1, 0, 1)
        self.table_name_var = ctk.StringVar(self, value="Table Name")
        self.table_name_entry = ctk.CTkEntry(self.table_name_frame, textvariable=self.table_name_var, font=self.font)
        # Create a frame for the list boxes
        self.listbox_frame = ctk.CTkFrame(self)
        self.listbox_frame.grid(row=2, column=0, padx=20, pady=10)
        # Create a listbox for the table names
        self.table_listbox = tk.listbox(self.listbox_frame, font=self.font)
        self.table_listbox.bind('<ButtonRelease-1>', self.table_changed)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=3, column=0, padx=20, pady=10)

        self.ok_button = ctk.CTkButton(self.button_frame, text="OK", command=self.ok_clicked, font=self.font)
        self.ok_button.pack(side="left", padx=(0, 10))

        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", command=self.cancel_clicked, font=self.font)
        self.cancel_button.pack(side="left")

    def table_changed(self, event) -> None:
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.table_name_var.set(event.widget.get(index))
            
    def center_on_parent(self, parent) -> None:
        # Update the geometry to get accurate dimensions
        self.update_idletasks()
        parent.update_idletasks()
        # Calculate position to center the dialog over the main application window
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        dialog_width = self.winfo_reqwidth()
        dialog_height = self.winfo_reqheight()

        position_x = parent_x + (parent_width / 2) - (dialog_width / 2)
        position_y = parent_y + (parent_height / 2) - (dialog_height / 2)

        # Set position
        self.geometry("+%d+%d" % (position_x, position_y))

    def ok_clicked(self) -> None:
        self.destroy()

    def cancel_clicked(self) -> None:
        self.destroy()
