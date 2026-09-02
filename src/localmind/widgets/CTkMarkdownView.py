# CTkMarkdownView.py

import customtkinter as ctk # type: ignore
from localmind.gui.CTkAppView import FontSpec
from typing import Union, Tuple, Optional
# from ctk_markdown import CTkMarkdown # type: ignore
from localmind.widgets.ctk_markdown import CTkMarkdown



class CTkMarkdownView(ctk.CTkToplevel):
    def __init__(self, parent: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame, title: str='Title', message='No message', markdown: str='', font: Optional[FontSpec]=None) -> None:
        super().__init__(parent)
        
        if isinstance(parent, (ctk.CTk, ctk.CTkToplevel)):
            self.transient(parent)
        self.title(title)
        #self.geometry("600x400")
        self.geometry("1200x800")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure([1], weight=1)

        self.message_label_frame = ctk.CTkFrame(self, bg_color='transparent')
        self.message_label_frame.grid(row=0, column=0, padx=5, pady=(5,0), sticky='new')
        self.message_label_frame.grid_columnconfigure(0, weight=1)
        self.message_label_frame.grid_rowconfigure(0, weight=1)
        self.message_label = ctk.CTkLabel(self.message_label_frame, text=message, font=font)
        self.message_label.grid(row=0, column=0, padx=5, pady=(5,5), sticky='ew')
        
        # Textbox Frame
        self.text_frame = ctk.CTkFrame(self, bg_color='transparent')
        self.text_frame.grid(row=1, column=0, padx=5, pady=(5, 0), sticky='nsew')
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)

        # self.text_box = ctk.CTkTextbox(self.text_frame, height=40, font=font)
        self.text_box = CTkMarkdown(self.text_frame, font=font)
        self.text_box.set_markdown(markdown)
        
        self.text_box.grid(row=0, column=0, padx=5, pady=(5,0), sticky='nsew')

        # Buttons frame
        self.button_frame = ctk.CTkFrame(self, bg_color='transparent')
        self.button_frame.grid(row=2, column=0, padx=5, pady=(5, 5), sticky="sew")
        self.button_frame.grid_rowconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)

        self.yes_button = ctk.CTkButton(self.button_frame, text="Ok",  command=self.ok_clicked, font=font)
        self.yes_button.grid(row=0, column=0, padx=5, pady=(5,5), sticky='ew')
        # self.no_button = ctk.CTkButton(self.button_frame, text="Cancel", command=self.cancel_clicked, font=font)
        # self.no_button.grid(row=0, column=1, padx=10, pady=(10,10), sticky='ew')
        # Center the dialog over parent
        self.center_on_parent(parent)
        self.after(200, self.focus_on_text_box)
        self.protocol("WM_DELETE_WINDOW", self.cancel_clicked)  # Treat window close as 'No'
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def get_markdown_box(self) -> CTkMarkdown:
        return self.text_box

    def set_markdown(self, markdown: str) -> None:
        self.text_box.set_markdown(markdown)
        self.text_box.update_idletasks()

    def focus_on_text_box(self) -> None:
        self.text_box.focus_set()
        self.text_box.update_idletasks()

    def center_on_parent0(self, parent) -> None:
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

    def center_on_parent(self, parent: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame) -> None:
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

    def ok_clicked(self) -> None:
        self.destroy()

    def cancel_clicked(self) -> None:
        self.destroy()
