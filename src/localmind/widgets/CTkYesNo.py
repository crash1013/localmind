# CTkYesNo.py

import customtkinter as ctk # type: ignore
from localmind.gui.CTkAppView import FontSpec
from typing import Optional, Union, Tuple, List

class CTkYesNo(ctk.CTkToplevel):
    def __init__(self, parent, title: str='Title', message: str='No message', font: Optional[FontSpec]=None):
        super().__init__(parent)
        
        self.result: bool | None = None  # Store the result here (True for Yes, False for No)
        self.transient(parent)
        self.title(title)
        self.geometry("400x120")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure([0,1], weight=1)
        # self.grid_rowconfigure(1, weight=1)
        #self.grid_columnconfigure(1, weight=1)
        #self.grid_rowconfigure(1, weight=1)

        message_label = ctk.CTkLabel(self, text=message, font=font)
        message_label.grid(row=0, column=0, padx=10, pady=(10,10), sticky='ew')
        

        # Buttons frame
        button_frame = ctk.CTkFrame(self, bg_color='transparent')
        button_frame.grid_rowconfigure(1, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        #button_frame.pack(pady=10)
        button_frame.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="ew")
        self.yes_button = ctk.CTkButton(button_frame, text="Yes",  command=self.yes_clicked, font=font)
        self.yes_button.grid(row=0, column=0, padx=10, pady=(10,10), sticky='ew')
        self.no_button = ctk.CTkButton(button_frame, text="No", command=self.no_clicked, font=font)
        self.no_button.grid(row=0, column=1, padx=10, pady=(10,10), sticky='ew')
        # Center the dialog over parent
        self.center_on_parent(parent)
        
        self.protocol("WM_DELETE_WINDOW", self.no_clicked)  # Treat window close as 'No'
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def center_on_parent0(self, parent):
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
        
    def center_on_parent(self, parent: ctk.CTk | ctk.CTkToplevel) -> None:
        self.update_idletasks()
        parent.update_idletasks()

        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        dialog_width = self.winfo_reqwidth()
        dialog_height = self.winfo_reqheight()

        position_x = round(
            parent_x + (parent_width - dialog_width) / 2
        )
        position_y = round(
            parent_y + (parent_height - dialog_height) / 2
        )

        # The :+d formatter produces +500 or -500 correctly.
        self.geometry(
            f"{dialog_width}x{dialog_height}{position_x:+d}{position_y:+d}"
        )

    def yes_clicked(self):
        self.result = True
        self.destroy()

    def no_clicked(self):
        self.result = False
        self.destroy()
