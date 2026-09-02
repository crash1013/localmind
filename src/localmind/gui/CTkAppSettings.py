# MyDaySettings.py

import os
import sys
from pathlib import Path
import customtkinter as ctk # type: ignore
from typing import List, Union, Tuple
#
from localmind.widgets.CTkDialog import CTkDialog
from localmind.widgets.CTkYesNo import CTkYesNo
from localmind.widgets.CTkFontPicker import CTkFontPicker
from localmind.gui.CTkSettings import CTkSettings
from localmind.gui.CTkAppView import CTkAppView
from localmind.gui.CTkAppData import CTkAppData



# 
class CTkAppSettings(CTkAppView):

    def __init__(self, parent, frame: ctk.CTkFrame, font: Union[ctk.CTkFont, Tuple[str, int, str]], data: CTkAppData, gui_settings, user_settings):
        super().__init__(parent, frame, font, data)

        self.gui_settings = gui_settings
        self.user_settings = user_settings
        frame.grid_columnconfigure(0, weight=1)
        self.appearance_frame = self.labeled_frame(self.frame,
                                                   label='Appearance', 
                                                   parent_row=0,
                                                   parent_column=0,
                                                   columns=2,
                                                   column_weight=[1,1])
        
        
        self.mode_select_label = ctk.CTkLabel(self.appearance_frame, text='Mode:', font=font)
        self.mode_select_label.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.switch_var =  ctk.StringVar(value=gui_settings['mode'])
        self.switch = ctk.CTkSwitch(self.appearance_frame, text=self.switch_var.get(), command=self.switch_event,
                                 variable=self.switch_var, onvalue="light", offvalue="dark", font=font)
        self.switch.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        self.theme_button = ctk.CTkButton(self.appearance_frame, text='Theme', command=self.update_theme, font=font)
        self.theme_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.theme_label = ctk.CTkLabel(self.appearance_frame, text=self.gui_settings['theme'], font=font)
        self.theme_label.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        # self.font_frame = ctk.CTkFrame(frame)
        self.font_frame = self.labeled_frame(self.frame,
                                             label='Font',
                                             parent_row=1,
                                             parent_column=0,
                                             columns=2,
                                             column_weight=[1,1],
                                             row0_weight=0)
        
        #self.font_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        #self.font_frame.grid_columnconfigure(1, weight=1)
        #self.font_frame.grid_columnconfigure(2, weight=1)

        self.font_family_label = ctk.CTkLabel(self.font_frame, text='Family:', font=font)
        self.font_family_label.grid(row=0, column=0, padx=10, pady=10, sticky='ne')
        self.font_family = ctk.CTkLabel(self.font_frame, text=self.gui_settings['font']['family'], font=font)
        self.font_family.grid(row=0, column=1, padx=10, pady=10, sticky='nw')

        self.font_size_label = ctk.CTkLabel(self.font_frame, text='Size:', font=font)
        self.font_size_label.grid(row=1, column=0, padx=10, pady=10, sticky='ne')
        self.font_size = ctk.CTkLabel(self.font_frame, text=str(self.gui_settings['font']['size']), font=font)
        self.font_size.grid(row=1, column=1, padx=10, pady=10, sticky='nw')

        #self.font_option_frame = ctk.CTkFrame(frame)
        #self.font_option_frame.grid_columnconfigure(0, weight=1)

        #self.font_option_frame.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        
        self.weight_var = ctk.StringVar(value=self.gui_settings['font']['weight'])
        self.weight_switch = ctk.CTkSwitch(self.font_frame,
                                            text='Bold', 
                                            variable=self.weight_var, 
                                            onvalue='bold', 
                                            offvalue= 'normal', 
                                            command=self.on_switch_weight, 
                                            font=font)
        self.weight_switch.grid(row=2, column=0, padx=10, pady=10, sticky='ne')

        self.italic_var = ctk.StringVar(value=self.gui_settings['font']['slant'])
        self.italic_switch = ctk.CTkSwitch(self.font_frame, 
                                           text='Italic', 
                                           variable=self.italic_var, 
                                           onvalue='italic', 
                                           offvalue= 'roman', 
                                           command=self.on_switch_italic, 
                                           font=font)
        self.italic_switch.grid(row=2, column=1, padx=10, pady=10, sticky='nw')

        self.underline_var = ctk.StringVar(value='yes' if self.gui_settings['font']['underline'] else 'no')
        self.underline_switch = ctk.CTkSwitch(self.font_frame, 
                                            text='Underline', 
                                            variable=self.underline_var, 
                                            onvalue='yes', 
                                            offvalue= 'no', 
                                            command=self.on_switch_underline, 
                                            font=font)
        self.underline_switch.grid(row=3, column=0, padx=10, pady=10, sticky='ne')

        self.overstrike_var = ctk.StringVar(value='yes' if self.gui_settings['font']['overstrike'] else 'no')
        self.overstrike_switch = ctk.CTkSwitch(self.font_frame, 
                                                text='Overstrike', 
                                                variable=self.overstrike_var,
                                                onvalue='yes', 
                                                offvalue= 'no',
                                                command=self.on_switch_overstrike, 
                                                font=font)
        self.overstrike_switch.grid(row=3, column=1, padx=10, pady=10, sticky='nw')

        self.font_button = ctk.CTkButton(self.font_frame, text='Configure Font', command=self.on_configure_font, font=font)
        self.font_button.grid(row=4, column=0, padx=10, pady=10, sticky='new', columnspan=2)

        self.control_frame = self.labeled_frame(self.frame, label='Controls', parent_row=2, parent_column=0, columns=1, column_weight=[1])

        self.ok_button = ctk.CTkButton(self.control_frame, text="Restart", command=self.on_apply, font=font)
        self.ok_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.disable_font_controls()

    def disable_font_controls(self):
        self.weight_switch.configure(state='disabled')
        self.italic_switch.configure(state='disabled')
        self.underline_switch.configure(state='disabled')
        self.overstrike_switch.configure(state='disabled')

    def enable_font_controls(self):
        self.weight_switch.configure(state='normal')
        self.italic_switch.configure(state='normal')
        self.underline_switch.configure(state='normal')
        self.overstrike_switch.configure(state='normal')

    def initialize_widgets(self):
        # Your widget initialization code here
        pass
    
    def on_visible(self) -> None:
        self.data.logger.debug(f"{self.__class__}.on_visible() called")

    def sb_button_list(self) -> List[str]:
        return []

    @property 
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        if not isinstance(value, CTkAppData):
            raise TypeError("Data type error, expecting CTkAppData")
        self._data = value
        
    def on_apply(self):
        self.result = True
        ctk.set_appearance_mode(mode_string=self.gui_settings['mode'])
        self.gui_settings['geometry'] = self.parent.geometry()
        CTkSettings.save_settings(self.gui_settings, filename=self.parent.gui_settings_file)
        self.parent.save_settings(self.parent.exec_settings, self.parent.exec_settings_file, self.parent.users_home)
        self.parent.save_settings_on_exit()
        self.restart_app()

    def restart_app(self):
        """Restart the current program."""
        p = self.parent.exec_settings.get('virtual_env', sys.executable)
        if not os.path.exists(p):
            p = sys.executable
        os.execl(p, p, self.parent.script_path)

    def on_configure_font(self):
        font = ctk.CTkFont(family = self.gui_settings['font']['family'],
                                        size=self.gui_settings['font']['size'],
                                        weight=self.gui_settings['font']['weight'],
                                        slant=self.gui_settings['font']['slant'],
                                        underline=self.gui_settings['font']['underline'],
                                        overstrike=self.gui_settings['font']['overstrike'])
        fp = CTkFontPicker(self.frame, title='Configure Font', current_font=font)
        if not fp.result:
            return
        self.enable_font_controls()
        fd = self.gui_settings['font']
        fd['family'] = fp.family
        fd['size'] = fp.size
        fd['weight'] = fp.weight
        fd['slant'] = fp.slant
        fd['underline'] = fp.underline
        fd['overstrike'] = fp.overstrike
        
        self.font = ctk.CTkFont(family = self.gui_settings['font']['family'],
                                        size=self.gui_settings['font']['size'],
                                        weight=self.gui_settings['font']['weight'],
                                        slant=self.gui_settings['font']['slant'],
                                        underline=self.gui_settings['font']['underline'],
                                        overstrike=self.gui_settings['font']['overstrike'])
        self.font_family.configure(text=fd['family'])
        self.font_size.configure(text=str(fd['size']))

        # self.weight_switch.configure(textvariable=fd['weight'])
        if fd['weight'].lower() == 'normal':
            self.weight_switch.deselect()
        else:
            self.weight_switch.select()

        # self.italic_switch.configure(textvariable=fd['slant'])
        if fd['slant'] == 'roman':
            self.italic_switch.deselect()
        else:
            self.italic_switch.select()

        # self.underline_switch.configure(textvariable='yes' if fd['underline'] else 'no')
        if fd['underline']:
            self.underline_switch.select()
        else:
            self.underline_switch.deselect()

        #self.overstrike_switch.configure(textvariable='yes' if fd['underline'] else 'no')
        if fd['overstrike']:
            self.overstrike_switch.select()
        else:
            self.overstrike_switch.deselect()

        self.disable_font_controls()
        

    def on_switch_weight(self): # read only
        return

    def on_switch_italic(self): # read only
        return

    def on_switch_underline(self): # read only
        return

    def on_switch_overstrike(self): # read only
        return

    def update_theme(self):

        dialog = CTkYesNo(self.parent, message="Do you want to select a new theme?", title="Confirmation", font=self.font)
        if dialog.result:
            theme_dir = Path(self.gui_settings['theme']).parent
            theme_name=ctk.filedialog.askopenfilename(initialdir=theme_dir, 
                                                      title="Select Theme File", 
                                                      filetypes=[("JSON files", "*.json")])
            self.gui_settings['theme'] = theme_name
            self.theme_label.configure(text=theme_name)
            # self.save_settings()
            CTkDialog(self.frame, 'Caveat', 'Theme will be used after restarting the app', font=self.font)

    def switch_event(self):
        mode = self.switch_var.get()
        ctk.set_appearance_mode(mode)
        self.gui_settings['mode'] = mode
        self.switch.configure(text=mode)
