# ctkDatePicker

import tkinter as tk
import customtkinter # type: ignore
from datetime import date
from tkcalendar import DateEntry # type: ignore

class CTkDatePicker(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        self.font = kwargs.pop('font', None)
        self.tk_font = ((self.font.cget('family'), self.font.cget('size')))
        self.year = kwargs.pop('year', 2000)
        self.month = kwargs.pop('month', 1)
        self.day = kwargs.pop('day', 1)
        self.date_pattern = kwargs.pop('date_pattern', 'y-mm-dd')
        self.command = kwargs.pop('command', None)
        super().__init__(master, **kwargs)

        self.date_picker = DateEntry(self, year=self.year, month=self.month, day=self.day, date_pattern=self.date_pattern, font=self.tk_font)
        self.date_picker.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.date_picker.bind('<<DateEntrySelected>>', self.on_date_entry_selected)

    def on_date_entry_selected(self, event):
        if self.command is not None:
            self.command(self.date_picker.get_date())
            
    def get_date(self):
        return self.date_picker.get_date()
    
    def set_date(self, d):
        self.date_picker.set_date(d)