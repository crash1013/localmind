# CTkDialog.py
import customtkinter as ctk # type: ignore
from localmind.gui.CTkAppView import FontSpec
from typing import Optional, Tuple, Union

class CTkDialog(ctk.CTkToplevel):
    def __init__(self, parent, title: Optional[str]=None, message: Optional[str]=None, font: Optional[FontSpec]=None):
        super().__init__(parent)
        self.transient(parent)

        if title is not None:
            self.title(title)
        self.grid_rowconfigure([0,1], weight=1)
        self.grid_columnconfigure([0], weight=1)
        if message is not None:
            message_label = ctk.CTkLabel(self, text=message, font=font)
            message_label.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        button = ctk.CTkButton(self, text="OK", command=self.destroy, font=font)
        button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        
        # Center the dialog over parent
        #self.geometry("+%d+%d" % (parent.winfo_rootx() + 300, parent.winfo_rooty() + 200))
        #self.geometry("+%d+%d" % (parent.winfo_rootx() + parent.winfo_width()/2, parent.winfo_rooty() + parent.winfo_height()/2))
        self.center_on_parent(parent)        

        
        self.protocol("WM_DELETE_WINDOW", self.destroy)
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
