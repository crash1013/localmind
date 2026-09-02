# FontPicker.py

import customtkinter # type: ignore
import tkinter as tk
import tkinter.font as tkfont

from localmind.widgets.IntSpinbox import IntSpinbox

class CTkFontPicker(customtkinter.CTkToplevel):
    def __init__(self, parent, title, current_font):
        super().__init__(parent)
        self.transient(parent)

        if title:
            self.title(title)
        self.result = None
        self.textfont = customtkinter.CTkFont(family=current_font.cget('family'), size=current_font.cget('size'), weight=current_font.cget('weight'))
        self.size = current_font.cget('size')
        self.family = current_font.cget('family')
        self.weight = current_font.cget('weight')
        self.slant = current_font.cget('slant')
        self.weight = current_font.cget('weight')
        self.underline = current_font.cget('underline')
        self.overstrike = current_font.cget('overstrike')
        
        #make the textfield fill all available space
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        
        #something to type in ~ uses the persistent font reference
        self.picker_frame = customtkinter.CTkFrame(self)
        self.picker_frame.grid_rowconfigure(0, weight=1)
        self.picker_frame.grid_columnconfigure([0,1], weight=1)
        self.picker_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        tb = customtkinter.CTkTextbox(self.picker_frame, font=self.textfont)
        tb.grid(row=0, column=0, sticky='nswe')
        tb.insert("0.0", "Sample Text")
        
        #font chooser
        self.fc = tk.Listbox(self.picker_frame, font=('Righteous', 14))
        self.fc.grid(row=0, column=1, sticky='nswe')

        #insert all the fonts
        families = sorted(tkfont.families())
        for f in families:
            self.fc.insert('end', f)

        #switch textfont family on release
        def fc_changed(ev):
            selection = self.fc.curselection()
            if selection:            
                family = self.fc.get(self.fc.curselection())
                self.textfont.configure(family=family, size=self.size)
                self.family_label.configure(text=family)
                self.family = family
            else:
                print("No font selected yet.")
            
            
        self.fc.bind('<ButtonRelease-1>', fc_changed)
        
        #scrollbar ~ you can actually just use the mousewheel to scroll
        self.vsb = customtkinter.CTkScrollbar(self)
        self.vsb.grid(row=0, column=2, sticky='ns')
        
        #connect the scrollbar and font chooser
        self.fc.configure(yscrollcommand=self.vsb.set)
        self.vsb.configure(command=self.fc.yview)

        
        self.info_frame = customtkinter.CTkFrame(self)
        self.info_frame.grid_rowconfigure(0, weight=1)
        for i in range(4):
            self.info_frame.grid_columnconfigure(i, weight=1)
        self.info_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        # self.info_frame.grid_rowconfigure(0, weight=1)
        self.family_label_label = customtkinter.CTkLabel(self.info_frame, text='family:', font=current_font)
        self.family_label_label.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.family_label = customtkinter.CTkLabel(self.info_frame, text=self.textfont.cget('family'), font=current_font)
        self.family_label.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.size_label = customtkinter.CTkLabel(self.info_frame, text='size:', font=current_font)
        self.size_label.grid(row=0, column=2, padx=10, pady=10, sticky='ew')
        self.size_spinner= IntSpinbox(self.info_frame, min=8, max=24, current=self.size, command=self.font_size_changed)
        self.size_spinner.grid(row=0, column=3, padx=10, pady=10, sticky='ew')
        
        # add a button frame below the font information

        self.checkbox_frame = customtkinter.CTkFrame(self)
        self.checkbox_frame.grid_columnconfigure(0, weight=1)
        self.checkbox_frame.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        self.cb_italic_var = customtkinter.StringVar(value=self.slant)
        self.cb_italic = customtkinter.CTkCheckBox(self.checkbox_frame, text='italic', command=self.slant_changed, onvalue='italic', offvalue='roman', variable=self.cb_italic_var, font=current_font)
        self.cb_italic.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        
        self.cb_weight_var = customtkinter.StringVar(value=self.weight)
        self.cb_weight = customtkinter.CTkCheckBox(self.checkbox_frame, text='bold', command=self.weight_changed, onvalue='bold', offvalue='normal', variable=self.cb_weight_var, font=current_font)
        self.cb_weight.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        
        self.cb_underline_var = customtkinter.IntVar(value=self.underline)
        self.cb_underline = customtkinter.CTkCheckBox(self.checkbox_frame, text='underline', command=self.underline_changed, onvalue=1, offvalue=0, variable=self.cb_underline_var, font=current_font)
        self.cb_underline.grid(row=0, column=2, padx=10, pady=10, sticky='ew')
        
        self.overstrike_var = customtkinter.IntVar(value=self.overstrike)
        self.cb_overstrike = customtkinter.CTkCheckBox(self.checkbox_frame, text='overstrike', command=self.overstrike_changed, onvalue=1, offvalue=0, variable=self.overstrike_var, font=current_font)
        self.cb_overstrike.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

        self.control_frame = customtkinter.CTkFrame(self)
        self.control_frame.grid(row=3, column=0, padx=10, pady=10, sticky='ew')
        self.control_frame.grid_columnconfigure([0,1], weight=1)

        self.ok_button = customtkinter.CTkButton(self.control_frame, text='Ok', command=self.on_ok, font=current_font)
        self.ok_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.cancel_button = customtkinter.CTkButton(self.control_frame, text='Cancel', command=self.on_cancel, font=current_font)
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        self.result = None

        self.center_on_parent(parent)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def on_ok(self):
        self.result = True
        self.destroy()

    def on_cancel(self):
        self.result = False
        self.destroy()

    def slant_changed(self):
        self.slant = self.cb_italic.get()
        self.textfont.configure(slant=self.slant)

    def weight_changed(self):
        self.weight = self.cb_weight.get()
        self.textfont.configure(weight=self.weight)

    def underline_changed(self):
        self.underline = bool(self.cb_underline.get())
        self.textfont.configure(underline=self.underline)

    def overstrike_changed(self):
        self.overstrike = bool(self.cb_overstrike.get())
        self.textfont.configure(overstrike=self.overstrike)

    def font_size_changed(self, new_value):
        self.size = new_value
        self.textfont.configure(size=new_value)

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
