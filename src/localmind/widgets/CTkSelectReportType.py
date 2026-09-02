# CTkSelectReportType.py

import customtkinter as ctk # type: ignore
from localmind.gui.CTkAppView import FontSpec
from localmind.utils.CTkLabeledFrame import labeled_frame
from typing import Optional, Union, Tuple, List

class CTkSelectReportType(ctk.CTkToplevel):
    def __init__(self, parent, title: str='Report Type', message='Select the report type', font: FontSpec | None = None):
        """
        
        A dialog window that allows the user to select a report type (PDF or Markdown).
        The result is stored in self.result, which will be either "pdf", "markdown", or None if the dialog was closed without a selection.
        Added a checkbox yo select open PDF after generation. The result is stored in self.open_pdf, which will be either True or False.

        """

        super().__init__(parent)
        
        if font is None:
            font = ctk.CTkFont(size=18) 
        self.result: str | None = None  # Store the result here ("pdf" for PDF, "markdown" for Markdown)
        self.open_pdf: bool = True  # Store the checkbox state here (True if checked, False if unchecked)
        self.transient(parent)
        self.title(title)
        self.geometry("400x240")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        button_frame = labeled_frame(parent=self, 
                                     label="Select Report Type", 
                                     parent_row=0, 
                                     parent_column=0, 
                                     columns=2, 
                                     columnspan=1, 
                                     column_weight=[1,1], 
                                     row0_weight=1, 
                                     make_scrollable=False,
                                     font=font)
        self.type_button_var = ctk.StringVar(value="pdf")  # Default selection is PDF
        self.type_button_var.trace_add("write", lambda *args: self.radio_clicked())  # Call radio_clicked when the variable changes
        self.pdf_button = ctk.CTkRadioButton(button_frame, text="PDF", variable=self.type_button_var, value="pdf", command=self.radio_clicked, font=font)
        self.pdf_button.grid(row=1, column=0, padx=10, pady=(10,10), sticky='ew')
        self.markdown_button = ctk.CTkRadioButton(button_frame, text="Markdown", variable=self.type_button_var, value="markdown", command=self.radio_clicked, font=font)
        self.markdown_button.grid(row=1, column=1, padx=10, pady=(10,10), sticky='ew')
        self.open_pdf_var = ctk.BooleanVar(value=self.open_pdf)  # Default is to open PDF
        self.open_pdf_checkbox = ctk.CTkCheckBox(button_frame, text="Open PDF after generation", variable=self.open_pdf_var, font=font)
        self.open_pdf_checkbox.grid(row=2, column=0, columnspan=2, padx=10, pady=(10,10), sticky='ew')
        self.open_pdf = self.open_pdf_var.get()

        self.ok_button = ctk.CTkButton(button_frame, text="OK", command=self.on_clicked_ok, font=font)
        self.ok_button.grid(row=3, column=0, padx=10, pady=(10,10), sticky='ew')
        self.cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=self.on_clicked_cancel, font=font)
        self.cancel_button.grid(row=3, column=1, padx=10, pady=(10,10), sticky='ew')
        # Center the dialog over parent
        self.center_on_parent(parent)
        
        self.protocol("WM_DELETE_WINDOW", self.on_clicked_cancel)  # Treat window close as 'No'
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
        self.geometry("+%d+%d" % (position_x, position_y))


    def on_clicked_cancel(self):
        self.result = None
        self.destroy()

    def on_clicked_ok(self):
        self.result = self.type_button_var.get()
        self.open_pdf = self.open_pdf_var.get()  # Update the open_pdf attribute when the checkbox changes
        self.destroy()

    def radio_clicked(self):
        if self.type_button_var.get() != "pdf":
            self.open_pdf_checkbox.grid_forget()  # Hide the checkbox when PDF is selected
        else:
            self.open_pdf_checkbox.grid(row=2, column=0, columnspan=2, padx=10, pady=(10,10), sticky='ew')  # Show the checkbox when PDF is selected
