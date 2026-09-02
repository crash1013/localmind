# CTkRadioListbox 
# A custom widget that allows you to create a list of checkboxes in a scrollable frame. 
# It is an extension of the CustomTkinter library, which is an extension of the Tkinter 
# library for creating modern and customizable GUI applications in Python.

import customtkinter as ctk # type: ignore
from localmind.gui.CTkAppView import FontSpec
from typing import Optional, cast

class CTkRadioListbox(ctk.CTkToplevel):

    def is_number(self, s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False

    def __init__(self, parent, title: str= 'Selection', items: list[str] = [], selected_item: str | None = None, font: Optional[FontSpec]=None, sort: bool = True, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.title(title)
        self.font = font
        self.selected_item = selected_item
        self.result: str | None = None
        if sort:
            if all(self.is_number(item) for item in items):
                self.items = sorted(items, key=lambda x: float(x))
            else:
                self.items = sorted(items)
        else:
            self.items = items
        self.initialize_widgets()


    def initialize_widgets(self) -> None:
        self.transient(self.parent)
        self.var = ctk.StringVar(value=self.selected_item)
        self.radio_buttons = []
        self.radio_frame = ctk.CTkScrollableFrame(self, bg_color='transparent')
        for i, item in enumerate(self.items):
            rb = ctk.CTkRadioButton(self.radio_frame, text=item, value=item,variable=self.var, font=self.font)
            rb.pack(anchor='w', padx=10, pady=5)
            self.radio_buttons.append(rb)
        self.radio_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.button_frame = ctk.CTkFrame(self, bg_color='transparent')
        self.button_frame.pack(padx=10, pady=10)
        self.ok_button = ctk.CTkButton(self.button_frame, text="Ok", command=self.ok_clicked, font=self.font)
        self.ok_button.pack(side='left', padx=10, pady=10)
        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", command=self.cancel_clicked, font=self.font)
        self.cancel_button.pack(side='left', padx=10, pady=10)
        self.center_on_parent(self.parent)
        self.after(200, self.focus_on_first_checkbox)
        self.protocol("WM_DELETE_WINDOW", self.cancel_clicked)  # Treat window close as 'No'
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def focus_on_first_checkbox(self) -> None:
        if self.radio_buttons:
            self.radio_buttons[0].focus_set()
            self.radio_buttons[0].update_idletasks()

    #def get_selected_items(self) -> list[str]:
    #     return [item for item, var in zip(self.items, self.vars) if var.get()]

    #def set_selected_items(self, selected_items: list[str]) -> None:
    #    for item, var in zip(self.items, self.vars):
    #        var.set(item in selected_items)

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

    def cancel_clicked(self) -> None:
        self.result = None
        self.destroy()

    def ok_clicked(self) -> None:
        #self.selected_items = self.get_selected_items()
        self.result = self.var.get()
        self.destroy()