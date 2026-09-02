# main_ui.py
from __future__ import annotations
import customtkinter as ctk # type: ignore

import os
from pathlib import Path
import sys
import json
from PIL import Image
import webbrowser

import numpy as np
import pandas as pd
from enum import IntEnum
from datetime import datetime
from datetime import date
import datetime as dt
import time

import localmind
from localmind.utils.PySqliteExt import SqliteExt
from localmind.gui.CTkAppView import CTkAppView
from localmind.gui.CTkAppData import CTkAppData
from localmind.gui.CTkAppSettings import CTkAppSettings
from localmind.gui.CTkAppWorkInstructions import CTkAppWorkInstructions
from localmind.gui.CTkDatabaseManager import CTkDatabaseManager
from localmind.gui.CTkServerView import CTkServerView
from localmind.gui.CTkBenchmarkView import CTkBenchmarkView
from localmind.gui.CTkAnalysisView import CTkAnalysisView
from localmind.gui.CTkSettings import CTkSettings
from localmind.gui.CTkLMSettings import CTkLMSettings
# from tkcalendar import DateEntry # type: ignore
from localmind.widgets.CTkYesNo import CTkYesNo
from localmind.utils.get_interpreter_path import get_interpreter_path
from localmind.utils.kill_llama_servers import kill_llama_servers, get_llama_server_procs

from typing import Union, List, Tuple, Dict, Optional
import logging


class LocalMind(ctk.CTk):
    _tab_names = ["Instructions", 'Settings', "DatabaseManager", "LMSettings", "LMServer", "Benchmark", "Analysis"]
    _tab_data = [ 'instruction_tab', 'settings_tab', 'database_manager_tab', 'lm_settings_tab', 'lm_server_tab', 'benchmark_tab', 'analysis_tab']
    class tabIndexes(IntEnum):
        WORK_INST_TAB = 0
        SETTINGS_TAB = 1
        DATABASE_MANAGER_TAB = 2
        LM_SETTINGS_TAB = 3
        LM_SERVER_TAB = 4
        BENCHMARK_TAB = 5
        ANALYSIS_TAB = 6
        END_TAB = 7

    def __init__(self, access_mode: CTkAppData.AccessModes = CTkAppData.AccessModes.ADMIN) -> None:
        super().__init__()
        self.ctkapp_data: CTkAppData = CTkAppData(app_name=self.__class__.__name__)
        self.ctkapp_data.access_mode = access_mode
        self.initialize_settings()
        self.check_database()
        self.initialize_ctk()
        self.initialize_widgets()
        time.sleep(2)
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Treat window close as 'No'
        # self.wait_visibility()
        self.update_count: int = 0
        self.update_timer: str = self.after(5000, self.do_update)

    def do_update(self) -> None:
        """ One second update timer, calls do_update in the current active tab """
        self.update_count += 1
        if hasattr(self.active_view, "do_update"):
            self.active_view.do_update()
        self.update_timer = self.after(1000, self.do_update)

    def initialize_ctk(self) -> None:
        ctk.set_default_color_theme(str(self.theme_file_path))
        if self.gui_settings is None or not isinstance(self.gui_settings, dict):
            raise ValueError("Settings not properly initialized")
        ctk.set_appearance_mode(mode_string=self.gui_settings['mode'])
        font_dict=self.gui_settings['font']
        self.custom_font = ctk.CTkFont(family=font_dict['family'], 
                                                 size=font_dict['size'],
                                                 weight=font_dict['weight'],
                                                 slant=font_dict['slant'],
                                                 underline=font_dict['underline'],
                                                 overstrike=font_dict['overstrike'])
        if 'title' in self.exec_settings.keys():
            self.title(self.exec_settings['title'])
        else:
            self.title(self.__class__.__name__)
        time.sleep(1)


    def initialize_widgets(self) -> None:
        """ Initialize the GUI """
        if 'geometry' in self.gui_settings.keys():
            self.geometry(self.gui_settings['geometry'])
        else:
            self.geometry(f"{1400}x{680}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self) #, width=600, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, padx=5, pady=(20, 10), rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(14, weight=1)


        self.image_path_light = "assets/favicon.png"
        self.image_path_dark = "assets/favicon-dark.png"
        self.logo_image = ctk.CTkImage(light_image=Image.open(self.image_path_light), dark_image=Image.open(self.image_path_dark), size=(64, 64))
        #self.image_label = ctk.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
        self.logo_button = ctk.CTkButton(self.sidebar_frame, 
                                         fg_color=self.sidebar_frame.cget('fg_color'),
                                         hover_color=self.sidebar_frame.cget('fg_color'),
                                         image=self.logo_image, 
                                         corner_radius=0, 
                                         border_width=0, 
                                         command=self.on_logo_button, 
                                         text="")
        #self.image_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.logo_button.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text=self.exec_settings['title'], font=ctk.CTkFont(family=self.custom_font.cget('family'), size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=20)

        # uncomment this section to add a date entry widget to the sidebar
        # you will need to create the callback function date_entry_virt_event to handle the event when the date is selected
        #self.date_label = ctk.CTkLabel(self.sidebar_frame, text="Date", font=self.custom_font)
        #self.date_label.grid(row=1, column=0, padx=10, pady=10)
        #today = date.today()
        #self.date_entry = DateEntry(self.sidebar_frame,
        #                            year=today.year, month=today.month, day=today.day, 
        #                            date_pattern='y-mm-dd',
        #                            font=(self.custom_font.cget('family'), self.custom_font.cget('size')))
        #self.date_entry.grid(row=2, column=0, padx=10, pady=10)

        #self.date_entry.bind('<<DateEntrySelected>>', self.date_entry_virt_event)

        
        # create the sidebar buttons and store them in a list of dictionaries for easy access
        self.sb_buttons: List[Dict[str, Union[Tuple[int,int], str, ctk.CTkButton]]] = []

        self.sb_new_button = ctk.CTkButton(self.sidebar_frame, text='New', command=self.on_sidebar_new, font=self.custom_font)
        self.sb_new_button.grid(row=3, column=0, padx=10, pady=10, sticky='ew')
        self.sb_buttons.append({'name': 'new', 'location': (3, 0), 'button': self.sb_new_button})
        
        self.sb_edit_button = ctk.CTkButton(self.sidebar_frame, text='Edit', command=self.on_sidebar_edit, font=self.custom_font)
        self.sb_edit_button.grid(row=4, column=0, padx=10, pady=10, sticky='ew')
        self.sb_buttons.append({'name': 'edit', 'location': (4, 0), 'button': self.sb_edit_button})
        
        self.sb_add_button = ctk.CTkButton(self.sidebar_frame, text='Add', command=self.on_sidebar_add, font=self.custom_font)
        self.sb_add_button.grid(row=5, column=0, padx=10, pady=10, sticky='ew')
        self.sb_buttons.append({'name': 'add', 'location': (5, 0), 'button': self.sb_add_button})
        
        self.sb_update_button = ctk.CTkButton(self.sidebar_frame, text='Update', command=self.on_sidebar_update, font=self.custom_font)
        self.sb_update_button.grid(row=6, column=0, padx=10, pady=10, sticky='ew')
        self.sb_buttons.append({'name': 'update', 'location': (6, 0), 'button': self.sb_update_button})

        self.sb_remove_button = ctk.CTkButton(self.sidebar_frame, text='Remove', command=self.on_sidebar_remove, font=self.custom_font)
        self.sb_remove_button.grid(row=7, column=0, padx=10, pady=10, sticky='ew')
        self.sb_buttons.append({'name': 'remove', 'location': (7, 0), 'button': self.sb_remove_button})

        self.sb_search_button = ctk.CTkButton(self.sidebar_frame, text='Search', command=self.on_sidebar_search, font=self.custom_font)
        self.sb_search_button.grid(row=8, column=0, padx=10, pady=10, sticky='ew')
        self.sb_buttons.append({'name': 'search', 'location': (8, 0), 'button': self.sb_search_button})

        self.sb_export_button = ctk.CTkButton(self.sidebar_frame, text='Export', command=self.on_sidebar_export, font=self.custom_font)
        self.sb_export_button.grid(row=9, column=0, padx=10, pady=10, sticky='ew')
        self.sb_buttons.append({'name': 'export', 'location': (9, 0), 'button': self.sb_export_button})

        self.sb_import_button = ctk.CTkButton(self.sidebar_frame, text='Import', command=self.on_sidebar_import, font=self.custom_font)
        self.sb_import_button.grid(row=10, column=0, padx=10, pady=10, sticky='ew')
        self.sb_buttons.append({'name': 'import', 'location': (10, 0), 'button': self.sb_import_button})
      
        self.sb_next_button = ctk.CTkButton(self.sidebar_frame, text='Next', command=self.on_sidebar_next, font=self.custom_font)
        self.sb_next_button.grid(row=11, column=0, padx=10, pady=10, sticky='ew')
        self.sb_buttons.append({'name': 'next', 'location': (11, 0), 'button': self.sb_next_button})

        self.sb_prior_button = ctk.CTkButton(self.sidebar_frame, text='Prior', command=self.on_sidebar_prior, font=self.custom_font)
        self.sb_prior_button.grid(row=12, column=0, padx=10, pady=10, sticky='ew')
        self.sb_buttons.append({'name': 'prior', 'location': (12, 0), 'button': self.sb_prior_button})

        self.sb_first_button = ctk.CTkButton(self.sidebar_frame, text='First', command=self.on_sidebar_first, font=self.custom_font)
        self.sb_first_button.grid(row=13, column=0, padx=10, pady=10, sticky='ew')
        self.sb_buttons.append({'name': 'first', 'location': (13, 0), 'button': self.sb_first_button})

        self.sb_last_button = ctk.CTkButton(self.sidebar_frame, text='Last', command=self.on_sidebar_last, font=self.custom_font)
        self.sb_last_button.grid(row=14, column=0, padx=10, pady=10, sticky='ew')
        self.sb_buttons.append({'name': 'last', 'location': (14, 0), 'button': self.sb_last_button})


        self.close_button = ctk.CTkButton(self.sidebar_frame, text='Close', command=self.on_close, font=self.custom_font)
        self.close_button.grid(row=15, column=0, padx=10, pady=10, sticky='ew')
        self.sb_buttons.append({'name': 'close', 'location': (15, 0), 'button': self.close_button})

        # append the button list to the ctkapp_data for access by other modules
        self.ctkapp_data.sb_buttons = self.sb_buttons


        # create the Tabview structure 
        self.tab_view = ctk.CTkTabview(master=self, command=self.on_tab_switch)
        self.tab_view.grid(row=0, column=1, padx=5, pady=(0,10), sticky='nsew')
        self.tab_view.grid_columnconfigure(0, weight=1)
        
        # add the tab names to the tab view and set the font to what the user has selected
        # configure the CkFrame for each tab to have a weight of 1 in the grid so that it expands to fill the space

        for i, tab_name in enumerate(self._tab_names):
            self.tab_view.add(tab_name)
            tab = self.tab_view.tab(tab_name)
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(1, weight=1)
            # use the font for the tab button that we choose, not the default
            self.tab_view._segmented_button._buttons_dict[tab_name].configure(font=self.custom_font)
            setattr(self.ctkapp_data, self._tab_data[i], tab)

                
        # create the tab view ui instances
        # these must have these minimal arguments: tab_window(parent, tab, font, data, kwarg)
        # parent = CtkApp (self)
        # tab =  tab_view.tab(tab_name)
        # font = CTkFont
        # data = CTkAppData

        settings = CTkAppSettings(self, self.tab_view.tab('Settings'), font=self.custom_font, data=self.ctkapp_data, gui_settings=self.gui_settings,user_settings=self.user_settings)
        self.ctkapp_data.settings = settings
        instructions = CTkAppWorkInstructions(self, self.tab_view.tab('Instructions'), font=self.custom_font, data=self.ctkapp_data)
        self.ctkapp_data.instructions = instructions
        database_manager = CTkDatabaseManager(self, self.tab_view.tab('DatabaseManager'), font=self.custom_font, data=self.ctkapp_data)
        self.ctkapp_data.database_manager = database_manager
        lmsettings = CTkLMSettings(self, self.tab_view.tab('LMSettings'), font=self.custom_font, data=self.ctkapp_data)
        self.ctkapp_data.lm_settings = lmsettings
        lmserver = CTkServerView(self, self.tab_view.tab('LMServer'), font=self.custom_font, data=self.ctkapp_data)
        self.ctkapp_data.lm_server = lmserver
        benchmark = CTkBenchmarkView(self, self.tab_view.tab('Benchmark'), font=self.custom_font, data=self.ctkapp_data)
        self.ctkapp_data.benchmark = benchmark
        analysis = CTkAnalysisView(self, self.tab_view.tab('Analysis'), font=self.custom_font, data=self.ctkapp_data)
        self.ctkapp_data.analysis = analysis

        self._views = [
            self.ctkapp_data.instructions,
            self.ctkapp_data.settings,
            self.ctkapp_data.database_manager,
            self.ctkapp_data.lm_settings,
            self.ctkapp_data.lm_server,
            self.ctkapp_data.benchmark,
            self.ctkapp_data.analysis     
        ]

        # set the default tab to the first one and set the active view to the first tab
        self.tab_view.set(self._tab_names[0])
        self.active_view: CTkAppView = self.ctkapp_data.settings
        self.on_tab_switch()
           
    def get_users_home(self, app_name: str) -> Path:
        users_home: Path = Path.home() / f".{app_name}" 
        self.ctkapp_data.logger.info(f"User home directory: {users_home}")
        return users_home

    def initialize_settings(self) -> None:
        """ Initialize the settings for the application """
        app_name = self.__class__.__name__

        self.users_home = Path(self.get_users_home(app_name))
        self.script_path = Path(__file__).resolve()
        self.script_dir = self.script_path.parent
        self.ctkapp_data.logger.info(f"Script directory: {self.script_dir}")

        self.users_home.mkdir(parents=True,exist_ok=True)

        old_path = Path.cwd()
        os.chdir(self.users_home)

        self.gui_settings_file = str(self.users_home / "gui_settings.json")
        self.ctkapp_data.logger.info(f"GUI settings file: {self.gui_settings_file}")

        self.exec_settings_file = str(self.users_home / f"{app_name}_settings.json")
        self.ctkapp_data.logger.info(f"Exec settings file: {self.exec_settings_file}")

        self.init_user_settings()
        self.ctkapp_data.home = self.users_home

        self.gui_settings = CTkSettings.load_settings(filename=self.gui_settings_file)

        self.theme_file_path = Path(self.gui_settings['theme'])
        self.theme_file = self.theme_file_path.name        
        
        if not self.theme_file_path.is_file():
            self.ctkapp_data.logger.error(
                f"Can't find theme file: {self.gui_settings['theme']} defaulting to blue"
            )
            self.theme_file = "blue"
            self.gui_settings["theme"] = self.theme_file

        # load executive settings
        self.ctkapp_data.logger.debug(f"Loading exec settings from '{self.exec_settings_file}'")

        self.exec_settings = self.load_settings(filename=self.exec_settings_file)

        keys = self.exec_settings.keys()

        # Set shared settings in ctkapp_data for access by other views and modules
        if "logging_level" in keys:
            self.ctkapp_data.logging_level = self.exec_settings.setdefault("logging_level", logging.INFO)
            
        if "use_sqlsvr" in keys:
            self.ctkapp_data.use_sqlsvr = self.exec_settings.setdefault("use_sqlsvr", False)

        if "instruction_file" in keys:
            self.ctkapp_data.last_instruction_file = self.exec_settings.setdefault("instruction_file", str(Path(self.users_home) / "instructions.md"))
            self.ctkapp_data.logger.debug(f"Set last instruction file: {self.ctkapp_data.last_instruction_file}")

        os.chdir(old_path)

        self.ctkapp_data.logger.info(f"Settings initialized.")

    def init_user_settings(self):
        self.user_settings = {
            "UserID": "user"
        }
        return 0

    def load_settings(self, filename: str):
        if filename == self.exec_settings_file and not os.path.exists(filename):
            path_to_python = get_interpreter_path()
            # write the default instructions file if it does not exist
            instruction_file_path = Path(self.ctkapp_data.package_root) / "docs/localmind.md"
            if not instruction_file_path.exists():
                #default_instructions = Path(self.script_dir) / "instructions.md"
                if instruction_file_path.exists():
                    with open(instruction_file_path, 'r') as src, open(instruction_file_path, 'w') as dst:
                        dst.write(src.read())
                else:
                    self.ctkapp_data.logger.warning(f"Default instructions file not found at {instruction_file_path}, creating empty instructions file.")
                    with open(instruction_file_path, 'w') as dst:
                        dst.write("# Instructions\n\n**Please open the localmind documentation file!**\n\n(It is <localmind install directory>\\docs\\localmind.md)")
            s = {
                "title": self.title(),
                "virtual_env": path_to_python,
                "database_path":self.ctkapp_data.database_path,
                "instruction_file": str(instruction_file_path),
                "use_sqlsvr": False
            }
            with open(filename, 'w') as fp:
                json.dump(s, fp, indent=4)
        else:
            with open(filename, 'r') as fp:
                s = json.load(fp)

        return s
    
    def save_settings(self, settings, filename, filepath=None):
        """ save_settings by default saves the executive settings in the same path as the executive code """
        if filepath==None:
            filepath=self.script_dir
        p = os.path.join(filepath, filename)
        with open(p, 'w') as fp:
            json.dump(settings, fp, indent=4)

    def tab_show_sb_buttons(self, show_buttons: list[str] | None = None) -> None:
        """Show sidebar buttons in the requested order."""

        if show_buttons is None:
            show_buttons = []

        # Hide all configurable buttons first
        for item in self.sb_buttons:
            button = item["button"]
            if button is not None and isinstance(button, ctk.CTkButton) and item["name"] != "close":
                button.grid_forget()

        # Show requested buttons consecutively
        for row, name in enumerate(show_buttons, start=3):
            button = self.ctkapp_data.get_button(name)

            if button is not None:
                button.grid(
                    row=row,
                    column=0,
                    padx=10,
                    pady=10,
                    sticky="ew",
                )

        self.update_idletasks()

    def on_logo_button(self):
        if self.ctkapp_data.lm_settings is None or not hasattr(self.ctkapp_data.lm_settings, "settings") or not hasattr(self.ctkapp_data.lm_settings.settings, "settings"):
            self.ctkapp_data.logger.error("LMSettings not properly initialized, cannot open server URL")
            return
        host = self.ctkapp_data.lm_settings.settings.settings.host
        port = self.ctkapp_data.lm_settings.settings.settings.port
        if host in ("0.0.0.0", "::", ""):
            host = "127.0.0.1"
        url = f"http://{host}:{port}/"
        self.ctkapp_data.logger.debug(f"Opening LocalMind server URL: {url}")
        
        try:
            webbrowser.open(url, new=2, autoraise=True)
        except Exception as exc:
            self.ctkapp_data.logger.exception(f"Failed to open browser for URL: {url}")

    def on_tab_switch(self):
        """
            called when the current tab is switched to a new tab.
            we set the active view and then update the sidebar buttons to accomodate the needs of
            the new view.
        """
        if hasattr(self.active_view, 'on_close_tab'):
            self.active_view.on_close_tab()
            
        tv_name = self.tab_view.get()
        self.ctkapp_data.logger.debug(f"tab: '{tv_name}' is active")
        self.last_tab = tv_name
        self.active_view = { name: view for name, view in zip(self._tab_names, self._views) }[tv_name]
        # self.active_view = self.active_view

        if hasattr(self.active_view, 'sb_button_list'):
            buttons = self.active_view.sb_button_list()
            self.tab_show_sb_buttons(buttons)
            if hasattr(self.active_view, 'on_visible'):
                self.active_view.on_visible()
        self.ctkapp_data.active_view_name = tv_name


    def on_sidebar_first(self) -> None:
        """ 
            Activate the on_sidebar_start function in the active view
        """
        if hasattr(self.active_view, "on_sidebar_first"):
            self.active_view.on_sidebar_first()

    def on_sidebar_last(self) -> None:
        """ 
            Activate the on_sidebar_end function in the active view
        """
        if hasattr(self.active_view, "on_sidebar_last"):
            self.active_view.on_sidebar_last()

    def on_sidebar_next(self) -> None:
        """ 
            Activate the on_sidebar_next function in the active view
        """
        if hasattr(self.active_view, "on_sidebar_next"):
            self.active_view.on_sidebar_next()

    def on_sidebar_prior(self) -> None:
        """ 
            Activate the on_sidebar_prior function in the active view
        """
        if hasattr(self.active_view, "on_sidebar_prior"):
            self.active_view.on_sidebar_prior()

    def on_sidebar_new(self) -> None:
        """ 
            Activate the on_sidebar_new function in the active view
        """
        if hasattr(self.active_view, "on_sidebar_new"):
            self.active_view.on_sidebar_new()

    def on_sidebar_edit(self) -> None:
        """ 
            Activate the on_sidebar_edit function in the active view
        """
        if hasattr(self.active_view, "on_sidebar_edit"):
            self.active_view.on_sidebar_edit()

    def on_sidebar_add(self) -> None:
        """ 
            Activate the on_sidebar_add function in the active view
        """
        if hasattr(self.active_view, "on_sidebar_add"):
            self.active_view.on_sidebar_add()

    def on_sidebar_update(self) -> None:
        """ 
            Activate the on_sidebar_update function in the active view
        """
        if hasattr(self.active_view, "on_sidebar_update"):
            self.active_view.on_sidebar_update()

    def on_sidebar_remove(self) -> None:
        """ 
            Activate the on_sidebar_remove function in the active view
        """
        if hasattr(self.active_view, "on_sidebar_remove"):
            self.active_view.on_sidebar_remove()

    def on_sidebar_search(self) -> None:
        """ 
            Activate the on_sidebar_search function in the active view
        """
        if hasattr(self.active_view, "on_sidebar_search"):
            self.active_view.on_sidebar_search()

    def on_sidebar_export(self) -> None:
        """ 
            Activate the on_sidebar_search function in the active view
        """
        if hasattr(self.active_view, "on_sidebar_export"):
            self.active_view.on_sidebar_export()

    def on_sidebar_import(self) -> None:
        """ 
            Activate the on_sidebar_search function in the active view
        """
        if hasattr(self.active_view, "on_sidebar_import"):
            self.active_view.on_sidebar_import()

    def save_user_settings(self) -> None:
        pass

    def save_settings_on_exit(self) -> None:
        self.gui_settings['geometry'] = self.geometry()

        # save the gui_settings to the gui_settings_file
        CTkSettings.save_settings(self.gui_settings, filename=self.gui_settings_file)

        # update from persistent shared exec_settings in ctkapp_data 
        self.exec_settings["use_sqlsvr"] = self.ctkapp_data.use_sqlsvr
        self.exec_settings["logging_level"] = self.ctkapp_data.logging_level
        self.exec_settings["database_path"] = self.ctkapp_data.database_path
        self.exec_settings["instruction_file"] = str(self.ctkapp_data.last_instruction_file)
        self.save_settings(self.exec_settings, self.exec_settings_file, self.script_dir)
        self.save_user_settings() # not used with current implementation, but could be used in the future to save user-specific settings
        self.ctkapp_data.logger.debug(f"lm_settings type: {type(self.ctkapp_data.lm_settings)}")
        if isinstance(self.ctkapp_data.lm_settings, CTkLMSettings) and hasattr(self.ctkapp_data.lm_settings._settings, "save_settings"):
            self.ctkapp_data.logger.debug(f"Saving lm_settings as: {str(self.ctkapp_data.lm_settings._settings.settings_path)}")
            self.ctkapp_data.lm_settings._settings.save_settings(str(self.ctkapp_data.lm_settings._settings.settings_path))

    def on_close(self) -> None:
        self.save_settings_on_exit()
        # check for running servers and ask to kill them before exiting
        procs = get_llama_server_procs()
        if procs:
            if CTkYesNo(self, "Running LLaMA Servers", message="There are running LLaMA servers. Do you want to kill them before exiting?", font=self.custom_font).result:
                kill_llama_servers(logger=self.ctkapp_data.logger)
        self.destroy()

    def init_database(self) -> None:
        """ If you are using the database and it does not exist or is missing tables: 
            
            1) Create it if it does not exist.

            2) Create the needed tables"""
        
        return

    def check_database(self) -> bool:
        """ 
            check_database is a function that runs once when CTkApp.__init__ is executed.
            This is also used to apply the path to the database to all modules that need
            access.
        """
        result = True
        if self.ctkapp_data.database_path is None or self.ctkapp_data.database_path == "":
            database_path = self.exec_settings['database_path']
            
            self.ctkapp_data.database_path = database_path
        
        return result
    
  

if __name__=="__main__":
    try:
        app = LocalMind()
        app.mainloop()
    except Exception as e:
        print("Exception occurred:", e)
        import traceback
        traceback.print_exc()
