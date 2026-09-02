import customtkinter as ctk # type: ignore
from localmind.gui.CTkAppView import FontSpec
from typing import Optional

class CTkNewDatabaseObject(ctk.CTkToplevel):
    def __init__(self, parent, title: str='New', font: Optional[FontSpec]=None, db_type: str = 'sqlite'):
        super().__init__(parent)
        
        if db_type != 'sqlite' and db_type != 'mssql':
            raise ValueError(f"Unknown database type: '{db_type}', expected: 'sqqlite' or 'mssql'")
        self.font = font
        self.result = None  # Store the result here (0 for no selection, 1 for Database, 2 for Table)
        self.transient(parent)
        self.title(title)
        self.geometry("400x200")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        
        message_label = ctk.CTkLabel(self, text="Select the type of new item", font=font)
        message_label.grid(row=0, column=0, padx=10, pady=(10,10), sticky='ew')
        
        # Create radio buttons
        self.radio_frame = ctk.CTkFrame(self)
        self.radio_frame.grid_rowconfigure(0, weight=1)
        self.radio_frame.grid_columnconfigure(0, weight=1)
        self.radio_frame.grid_columnconfigure(1, weight=1)
        self.radio_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.radio_var = ctk.IntVar(value=0)
        self.radio_database = ctk.CTkRadioButton(self.radio_frame, text="Database" if db_type == 'mssql' else 'Database File', variable=self.radio_var, value=1, font=self.font)
        self.radio_table = ctk.CTkRadioButton(self.radio_frame, text="Table", variable=self.radio_var, value=2, font=self.font)
        
        # Create OK and Cancel buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid_rowconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.ok_button = ctk.CTkButton(self.button_frame, text="OK", command=self.on_ok, font=self.font)
        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", command=self.on_cancel, font=self.font)

        
        # Layout using grid
        self.radio_database.grid(row=0, column=0, padx=20, pady=10, sticky='ew')
        self.radio_table.grid(row=0, column=1, padx=20, pady=10, sticky='ew')
        self.ok_button.grid(row=0, column=0, padx=10, pady=20, sticky='ew')
        self.cancel_button.grid(row=0, column=1, padx=10, pady=20, sticky='ew')
        
        # Center the dialog on the parent
        self.center_on_parent(parent)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)  # Treat window close as 'No'
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

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
        #self.geometry("+%d+%d" % (position_x, position_y))
        self.geometry(f"+{int(position_x)}+{int(position_y)}")

    
    def on_ok(self):
        self.result = self.radio_var.get()
        self.destroy()
    
    def on_cancel(self):
        self.result = 0
        self.destroy()
    

# Example usage
if __name__ == "__main__":
    app = ctk.CTk()
    dialog = CTkNewDatabaseObject(app, title="Select New Database Object")
    #app.wait_window(dialog)
    print(f"Selected option: {dialog.result}")
