# CTkGetText.py

import customtkinter as ctk # type: ignore
from localmind.gui.CTkAppView import FontSpec
from typing import Any, Optional

class CTkOpenChoice(ctk.CTkToplevel):
    def __init__(self, parent,
                 item_id: str, 
                 entry: dict[str, Any], 
                 choices: list[str], 
                 font: Optional[FontSpec]=None) -> None:
        super().__init__(parent)
        
        self.result : str = ""  # Store the result here (True for Yes, False for No)
        self.transient(parent)
        self.title(f"Select {entry.get('primary', 'value')}")
        self.geometry("400x200")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.font = font if font is not None else ctk.CTkFont(size=14)
        self.entry = entry
        #self.grid_columnconfigure(1, weight=1)
        #self.grid_rowconfigure(1, weight=1)

        self.message_label = ctk.CTkLabel(self, text=f"Select value for {entry.get('primary', '')}", font=font)
        self.message_label.grid(row=0, column=0, padx=10, pady=(10,10), sticky='ew')
        self.selected_value = ctk.StringVar(value=str(entry.get("value") or ""))
        
        # Textbox Frame
        self.combo_frame = ctk.CTkFrame(self, bg_color='transparent')
        self.combo_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.combo_frame.grid_columnconfigure(0, weight=1)
        self.combo = ctk.CTkComboBox(
            self.combo_frame,
            values=[str(choice) for choice in choices],
            variable=self.selected_value,
            font=self.font if self.font is not None else ctk.CTkFont(size=14),
            dropdown_font=self.font if self.font is not None else ctk.CTkFont(size=14),
            state="readonly",
        )
        self.combo.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # Buttons frame
        self.button_frame = ctk.CTkFrame(self, bg_color='transparent')
        self.button_frame.grid(row=2, column=0, padx=10, pady=(10, 10), sticky="sew")
        self.button_frame.grid_rowconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        #button_frame.pack(pady=10)
        self.yes_button = ctk.CTkButton(self.button_frame, text="Ok",  command=self.ok_clicked, font=font)
        self.yes_button.grid(row=0, column=0, padx=10, pady=(10,10), sticky='ew')
        self.no_button = ctk.CTkButton(self.button_frame, text="Cancel", command=self.cancel_clicked, font=font)
        self.no_button.grid(row=0, column=1, padx=10, pady=(10,10), sticky='ew')
        # Center the dialog over parent
        self.center_on_parent(parent)
        self.after(200, self.focus_on_text_box)
        self.protocol("WM_DELETE_WINDOW", self.cancel_clicked)  # Treat window close as 'No'
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def focus_on_text_box(self) -> None:
        self.combo.focus_set()
        self.combo.update_idletasks()

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

    def ok_clicked(self) -> None:
        self.result = self.selected_value.get()
        #self.result = self.text_box.get("1.0", "end")
        #self.entry["value"] = self.selected_value.get()
        #self._refresh_item(item_id, entry)
        #self._update_changed_label()

        self.destroy()

    def cancel_clicked(self) -> None:
        self.result = ""
        self.destroy()
