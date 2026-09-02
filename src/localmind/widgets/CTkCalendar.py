# CTkCalendar.py

import customtkinter # type: ignore
from datetime import datetime

from localmind.widgets.CTkDialog import CTkDialog

from tkcalendar import Calendar # type: ignore


def center_on_parent(w, parent):
    # Calculate position to center the dialog over the main application window
    parent_x = parent.winfo_x()
    parent_y = parent.winfo_y()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    dialog_width = w.winfo_reqwidth()
    dialog_height = w.winfo_reqheight()

    position_x = parent_x + (parent_width / 2) - (dialog_width / 2)
    position_y = parent_y + (parent_height / 2) - (dialog_height / 2)

    # Set position
    w.geometry("+%d+%d" % (position_x, position_y))

class CTkCalendarDialog(customtkinter.CTkToplevel):

    def __init__(self, parent, title=None, font=None, initial_date=None):
        super().__init__()
        self.result = None  # Store the result here 
        self.transient(parent)
        if initial_date is None:
            initial_date = datetime.now()
        self.title(title)
        self.grid_columnconfigure(0, weight=1)
        if font is not None:
            self.cal = Calendar(self, font=f"{font.cget('family')} {font.cget('size')}", selectmode='day', locale='en_US',
                              cursor="hand1", year=initial_date.year, month=initial_date.month, day=initial_date.day)
        else:
            self.cal = Calendar(self, selectmode='day', locale='en_US',
                       cursor="hand1", year=initial_date.year, month=initial_date.month, day=initial_date.day)
            
        self.cal.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.button = customtkinter.CTkButton(self, text="Ok", command=self.on_ok, font=font)
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        center_on_parent(self, parent)
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def on_ok(self):
        self.result = self.cal.selection_get()
        self.destroy()

class TestDateWidget(customtkinter.CTk):
        
    def __init__(self, mode='dark'):
        super().__init__()
      
        customtkinter.set_default_color_theme('blue')
        customtkinter.set_appearance_mode(mode_string=mode)
        self.custom_font = customtkinter.CTkFont(family='Righteous', size=18)
        self.geometry('250x125')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure([0,1], weight=1)
        self.button_date = customtkinter.CTkButton(self, text="Get Date", font=self.custom_font, command=self.get_date )
        self.button_date.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.button_ok  = customtkinter.CTkButton(self, text="Ok", font=self.custom_font, command=self.on_ok )
        self.button_ok.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.protocol("WM_DELETE_WINDOW", self.on_ok)  # Treat window close as 'No'
        today = datetime.now()
        self.selected_date = datetime(year=today.year, month=today.month, day=today.day) 

    def get_date(self):
        self.selected_date = CTkCalendarDialog(self, "Select a Date", font=self.custom_font, initial_date=datetime.now()).result
        CTkDialog(self, title="Selected Date", message=f"You selected '{self.selected_date}'", font=self.custom_font)
        return

    def on_ok(self):

        self.destroy()

if __name__=="__main__":
    app = TestDateWidget('blue')
    app.title("Work Instruction App")
    app.mainloop()
