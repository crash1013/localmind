# ctkDatePicker

import tkinter as tk
import customtkinter as ctk # type: ignore
from datetime import datetime, date, timedelta
from tkcalendar import DateEntry # type: ignore
from typing import cast

class CTkDateRangePicker(ctk.CTkToplevel):
    def __init__(self, parent, **kwargs):

        self.font = kwargs.pop('font', None)
        self.tk_font = ((self.font.cget('family'), self.font.cget('size')))
        self.result = False
        
        self.end_year = kwargs.pop('end_year', datetime.now().year)
        self.end_month = kwargs.pop('end_month', datetime.now().month)
        self.end_day = kwargs.pop('end_day', datetime.now().day)

        self.start_year = kwargs.pop('start_year', (datetime.now() - timedelta(days=30)).year)
        self.start_month = kwargs.pop('start_month', (datetime.now() - timedelta(days=30)).month)
        self.start_day = kwargs.pop('start_day', (datetime.now() - timedelta(days=30)).day)
        
        self.date_pattern = kwargs.pop('date_pattern', 'y-mm-dd')
        self.begin_date_command = kwargs.pop('begin_date_command', None)
        self.end_date_command = kwargs.pop('end_date_command', None)

        super().__init__(**kwargs)

        self.transient(parent)

        self.begin_date_frame = self.labeled_frame("Begin Date", 0, 0, 1, column_weight=[1])
        self.end_date_frame = self.labeled_frame("End Date", 0, 1, 1, column_weight=[1])
        self.begin_date_picker = DateEntry(self.begin_date_frame, year=self.start_year, month=self.start_month, day=self.start_day, date_pattern=self.date_pattern, font=self.tk_font)
        self.begin_date_picker.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.begin_date_picker.bind('<<DateEntrySelected>>', self.on_begin_date_entry_selected)

        self.end_date_picker = DateEntry(self.end_date_frame, year=self.end_year, month=self.end_month, day=self.end_day, date_pattern=self.date_pattern, font=self.tk_font)
        self.end_date_picker.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.end_date_picker.bind('<<DateEntrySelected>>', self.on_end_date_entry_selected)

        self.ok_button = ctk.CTkButton(self, text="OK", command=self.on_ok_clicked, font=self.font)
        self.ok_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.on_cancel_clicked, font=self.font)
        self.cancel_button.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        self.center_on_parent(parent)
        
        self.protocol("WM_DELETE_WINDOW", self.on_cancel_clicked)  # Treat window close as 'Cancel'
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def labeled_frame(
        self,
        label: str,
        parent_row: int,
        parent_column: int,
        columns: int,
        columnspan: int = 1,
        column_weight: list[int] = [],
        row0_weight: int = 1,
        make_scrollable: bool = False,
    ) -> ctk.CTkFrame:
        """
        Create a labeled CTk frame consisting of an outer frame (label + inner frame)
        and return the inner frame. The returned inner frame is configured so row 0
        and all specified columns can expand to fill available space.

        The outer frame is placed into `parent` at (parent_row, parent_column)
        with the given columnspan and sticky='nsew' so it can expand.
        """
        if len(column_weight) == 0:
            column_weight = [1] * columns

        # OUTER container
        if not make_scrollable:
            frame_outer = ctk.CTkFrame(self)
        else:
            frame_outer = ctk.CTkScrollableFrame(self)
            
        frame_outer.grid(row=parent_row, 
                         column=parent_column,
                         columnspan=columnspan, 
                         padx=10, 
                         pady=10, 
                         sticky="nsew")

        # Let the outer frame expand inside its parent cell
        # (the parent must also give this grid cell weight; see caller below)
        frame_outer.grid_columnconfigure(0, weight=1)
        frame_outer.grid_rowconfigure(0, weight=0)  # label row
        frame_outer.grid_rowconfigure(1, weight=1)  # inner frame row expands

        ctk_label = ctk.CTkLabel(frame_outer, text=label, font=self.font)
        ctk_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # INNER container (we return this)
        frame_inner = ctk.CTkFrame(frame_outer)
        frame_inner.grid(row=1, column=0, columnspan=columnspan, padx=5, pady=5, sticky="nsew")

        # Make inner frame's row 0 expand (where your widgets usually go)
        frame_inner.grid_rowconfigure(0, weight=row0_weight)

        # Make requested columns expand
        cl = len(column_weight)
        for c in range(columns):
            frame_inner.grid_columnconfigure(c, weight=column_weight[c])

        return frame_inner

    def center_on_parent(self, parent):
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



    def on_ok_clicked(self):
        self.result = True
        self.begin_date = self.begin_date_picker.get_date()
        self.end_date = self.end_date_picker.get_date()
        self.destroy()
    
    def on_cancel_clicked(self):
        self.result = False
        self.destroy()

    def on_begin_date_entry_selected(self, event):
        if self.begin_date_command is not None:
            self.begin_date_command(self.begin_date_picker.get_date())

    def on_end_date_entry_selected(self, event):
        if self.end_date_command is not None:
            self.end_date_command(self.end_date_picker.get_date())
            
    def get_begin_date(self):
        return self.begin_date_picker.get_date()
    
    def set_begin_date(self, d):
        self.begin_date_picker.set_date(d)

    def get_end_date(self):
        return self.end_date_picker.get_date()

    def set_end_date(self, d):
        self.end_date_picker.set_date(d)