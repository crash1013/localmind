import customtkinter as ctk # type: ignore
from localmind.widgets.CTkDialog import CTkDialog
from localmind.widgets.CTkYesNo import CTkYesNo
from localmind.widgets.CTkFontPicker import CTkFontPicker
from localmind.gui.CTkAppView import FontSpec

import json
import os
from pathlib import Path

from typing import Union, List, Dict, Optional, Any

class CTkSettings(ctk.CTkToplevel):

    @classmethod 
    def load_settings(cls, filename='settings.json') -> Dict[str, Any]:
        """
        Load settings from a JSON file. If the file does not exist, create it with default settings.

        Args:
            filename (str): The name of the settings file. Defaults to 'settings.json'.

        Returns:
            Dict[str, Any]: A dictionary containing the settings.

        The default settings include:
            - mode: 'dark'
            - theme: 'user_themes/GreyGhost.json'
            - geometry: None
            - font: 
                - family: 'Righteous'
                - size: 18
                - weight: 'normal' (or 'bold')
                - slant: 'roman' (or 'italic')
                - underline: False
                - overstrike: False

        If the file does not exist, it will be created with the default settings.
        If an error occurs while loading the settings, the default settings will be returned.
        """
        # Function implementation
        settings: Dict[str, Any] =  {
                    'mode': 'dark',
                    'theme': 'user_themes/GreyGhost.json',
                    'geometry': None,
                    'font':  {
                        'family': 'Righteous',
                        'size': 18,
                        'weight': 'normal', # or bold
                        'slant': 'roman',   # or italic
                        'underline': False,
                        'overstrike': False
                    }
                }
        try:
            if not os.path.exists(filename):
                cls.save_settings(settings=settings, filename=filename)
            else:
                with open(filename, 'r') as fp:
                    settings = json.load(fp)
        except Exception as error:
            print(f"save_settings error: {error}")
        return settings
    
    @classmethod
    def save_settings(cls, settings: Optional[Dict[str, Any]]=None, filename: str ='settings.json') -> None:
        """
        Save settings to a JSON file. Validates the settings dictionary before saving.

        Args:
            settings (Optional[Dict[str, Any]]): A dictionary containing the settings. Must include required keys.
            filename (str): The name of the settings file. Defaults to 'settings.json'.

        Raises:
            ValueError: If the settings object is None.
            KeyError: If required keys are missing in the settings dictionary.
            TypeError: If the settings object is not a dictionary.

        The required keys in the settings dictionary are:
            - mode
            - theme
            - font (which must include the following keys):
                - family
                - size
                - weight
                - slant
                - underline
                - overstrike

        The function ensures that all required keys are present in the settings dictionary.
        If validation passes, the settings are saved to the specified JSON file.
        """
        # Function implementation
        if settings is None:
            raise ValueError("Invalid empty settings object")
        def ensure_required_keys(d, required_keys):
            for key in required_keys:
                if key not in d:
                    raise KeyError(f"Missing required key in save_settings: {key}")
                  
        required = [ 'mode', 'theme', 'font' ]
        font_required = ['family', 'size', 'weight', 'slant', 'underline', 'overstrike' ]

        if not isinstance(settings, dict):
            raise TypeError("save_settings expected a dict as the settings object")
        ensure_required_keys(settings, required)
        ensure_required_keys(settings['font'], font_required)
        # were good to go lets save the settings
        with open(filename, 'w') as fp:
            json.dump(settings, fp, indent=4)


    def __init__(self, parent, settings:Optional[Dict[str, Any]]=None,  font:FontSpec | None = None):
        super().__init__(parent)
        if settings is None:
            CTkDialog(self, title="Error", message="Program error, settingsDialog initialization error", font=font)
            return
        if not isinstance(settings, dict):
            CTkDialog(self, title="Error", message='Program error, settings must be a dictionary', font=font)
            return
        self.parent = parent
        self.transient(parent)
        self.result = False
        self.font: FontSpec = font if font else ctk.CTkFont(size=18, weight='bold')
        self.backup_settings = settings.copy()
        self.settings = settings
        self.title('Settings')
        self.appearance_frame = ctk.CTkFrame(self)
        self.appearance_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.appearance_frame.grid_columnconfigure(1, weight=1)
        self.mode_select_label = ctk.CTkLabel(self.appearance_frame, text='Mode:', font=font)
        self.mode_select_label.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.switch_var =  ctk.StringVar(value=self.settings['mode'])
        self.switch = ctk.CTkSwitch(self.appearance_frame, text=self.switch_var.get(), command=self.switch_event,
                                 variable=self.switch_var, onvalue="light", offvalue="dark", font=font)
        self.switch.grid(row=0, column=1, padx=10, pady=10)

        self.theme_button = ctk.CTkButton(self.appearance_frame, text='Theme', command=self.update_theme, font=font)
        self.theme_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.theme_label = ctk.CTkLabel(self.appearance_frame, text=self.settings['theme'], font=font)
        self.theme_label.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        self.font_frame = ctk.CTkFrame(self)
        self.font_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.font_frame.grid_columnconfigure(1, weight=1)
        self.font_frame.grid_columnconfigure(2, weight=1)

        if isinstance(self.settings, dict):
            font_dict: dict[str, Any] = self.settings.get('font', {
                        'family': 'Courier',
                        'size': 18,
                        'weight': 'normal', # or bold
                        'slant': 'roman',   # or italic
                        'underline': False,
                        'overstrike': False
                    })
        else:
            raise ValueError("Invalid settings object: 'font'")

        self.font_family_label = ctk.CTkLabel(self.font_frame, text='Family:', font=font)
        self.font_family_label.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.font_family = ctk.CTkLabel(self.font_frame, text=font_dict['family'], font=font)
        self.font_family.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        self.font_size_label = ctk.CTkLabel(self.font_frame, text='Size:', font=font)
        self.font_size_label.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.font_size = ctk.CTkLabel(self.font_frame, text=font_dict['size'], font=font)
        self.font_size.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        self.font_option_frame = ctk.CTkFrame(self)
        self.font_option_frame.grid_columnconfigure(0, weight=1)

        self.font_option_frame.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        self.weight_var = ctk.StringVar(value=font_dict['weight'])
        self.weight_switch = ctk.CTkSwitch(self.font_option_frame, text='bold', 
                                                     variable=self.weight_var, onvalue='bold', offvalue= 'normal', command=self.on_switch_weight, font=font)
        self.weight_switch.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.italic_var = ctk.StringVar(value=font_dict['slant'])
        self.italic_switch = ctk.CTkSwitch(self.font_option_frame, text='Italic', 
                                                     variable=self.italic_var, onvalue='italic', offvalue= 'roman', command=self.on_switch_italic, font=font)
        self.italic_switch.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        self.underline_var = ctk.StringVar(value='yes' if font_dict['underline'] else 'no')
        self.underline_switch = ctk.CTkSwitch(self.font_option_frame, text='Underline', 
                                                        variable=self.underline_var, onvalue='yes', offvalue= 'no', command=self.on_switch_underline, font=font)
        self.underline_switch.grid(row=0, column=2, padx=10, pady=10, sticky='ew')

        self.overstrike_var = ctk.StringVar(value='yes' if font_dict['overstrike'] else 'no')
        self.overstrike_switch = ctk.CTkSwitch(self.font_option_frame, text='Overstrike', 
                                                         variable=self.overstrike_var, onvalue='yes', offvalue= 'no', command=self.on_switch_overstrike, font=font)
        self.overstrike_switch.grid(row=0, column=3, padx=10, pady=10, sticky='ew')


        self.font_configure_button_frame = ctk.CTkFrame(self)
        self.font_configure_button_frame.grid_columnconfigure(0, weight=1)
        self.font_configure_button_frame.grid(row=3, column=0, padx=10, pady=10, sticky='ew')
        self.font_button = ctk.CTkButton(self.font_configure_button_frame, text='Configure Font', command=self.on_configure_font, font=font)
        self.font_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=4, column=0, padx=10, pady=10, sticky='ew')
        self.control_frame.grid_columnconfigure([0, 1], weight=1)

        self.ok_button = ctk.CTkButton(self.control_frame, text="Ok", command=self.on_ok, font=font)
        self.ok_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.cancel_button = ctk.CTkButton(self.control_frame, text="Cancel", command=self.on_cancel, font=font)
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')


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
        self.font = self.backup_settings['font']
        self.destroy()

    def on_configure_font(self):
        font = ctk.CTkFont(family = self.settings['font']['family'],
                                        size=self.settings['font']['size'],
                                        weight=self.settings['font']['weight'],
                                        slant=self.settings['font']['slant'],
                                        underline=self.settings['font']['underline'],
                                        overstrike=self.settings['font']['overstrike'])
        fp = CTkFontPicker(self, title='Configure Font', current_font=font)
        fd = self.settings['font']
        fd['family'] = fp.family
        fd['size'] = fp.size
        fd['weight'] = fp.weight
        fd['slant'] = fp.slant
        fd['underline'] = fp.underline
        fd['overstrike'] = fp.overstrike
        
        self.font = ctk.CTkFont(family = self.settings['font']['family'],
                                        size=self.settings['font']['size'],
                                        weight=self.settings['font']['weight'],
                                        slant=self.settings['font']['slant'],
                                        underline=self.settings['font']['underline'],
                                        overstrike=self.settings['font']['overstrike'])
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


        

    def on_switch_weight(self): # read only
        return
        value=self.weight_switch.get()
        
        self.settings['font']['weight'] = value
        self.weight_switch.configure(textvariable=self.weight_var)

    def on_switch_italic(self):
        return
        value=self.italic_switch.get()
        
        self.settings['font']['slant'] = value
        self.italic_switch.configure(textvariable=self.italic_var)

    def on_switch_underline(self):
        return
        value=self.underline_switch.get()
        
        self.settings['font']['underline'] = True if value == 'yes' else False
        self.underline_switch.configure(textvariable=self.underline_var)

    def on_switch_overstrike(self):
        return
        value=self.overstrike_switch.get()
        
        self.settings['font']['overstrike'] = True if value == 'yes' else False
        self.overstrike_switch.configure(textvariable=self.overstrike_var)

    def update_theme(self):

        dialog = CTkYesNo(self, message="Do you want to select a new theme?", title="Confirmation", font = self.font if self.font else ctk.CTkFont(size=18, weight='bold'))
        if dialog.result:
            theme_name=ctk.filedialog.askopenfilename(initialdir=Path(self.settings['theme'].parent), title="Select Theme File", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
            self.settings['theme'] = theme_name
            self.theme_label.configure(text=theme_name)
            # self.save_settings()
            CTkDialog(self, 'Caveat', 'Theme will be used after restarting the app', font=self.font)


    def center_on_parent(self, parent):
        # Calculate position to center the dialog over the main application window
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        dialog_width = self.winfo_reqwidth()
        dialog_height = self.winfo_reqheight()

        position_x = parent_x + (parent_width / 2) - (dialog_width / 2)
        position_y = parent_y + (parent_height / 2) - (dialog_height / 2)

        # Set position
        self.geometry("+%d+%d" % (position_x, position_y))




    def switch_event(self):
        mode = self.switch_var.get()
        ctk.set_appearance_mode(mode)
        self.settings['mode'] = mode
        self.switch.configure(text=mode)
        self.parent.set_appearance_mode(mode)

