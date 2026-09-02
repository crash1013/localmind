
# 
# CTkAppData.py
#
import logging
import threading
from typing import List, Tuple
from enum import IntEnum
from logging import Logger

from localmind.utils.PySqliteExt import SqliteExt

# from CTkApp import CTkApp
from localmind.utils.initLogger import init_logger

from typing import Optional, Union, List, Dict, Any

from pathlib import Path
import localmind
import customtkinter as ctk # type: ignore

#from CTkAppView import CTkAppView
"""
    CTkAppData is used to provide for shared data access 
    CTkApp data records
"""


class CTkAppData:

    class AccessModes(IntEnum):
        USER = 0
        SUPERVISOR = 1
        ADMIN = 2

    """ The class members contain references to the settings, manual and process containers """

    def __init__(self, app_name: Optional[str]) -> None:
        self._lock : threading.RLock = threading.RLock()
        self._app_name = app_name
        self._home_dir : Optional[str] = None
        # we need a pair of these for each tab in the tab view
        self._settings_tab = None
        self._settings = None


        self._instructions_tab = None
        self._instructions = None
        self._last_instruction_file: Path | None = None

        self._database_manager_tab = None
        self._database_manager = None

        self._lm_settings_tab = None
        self._lm_settings = None

        self._lm_server_tab = None
        self._lm_server = None
        self._server_settings: dict[str, Any] = {}

        # benchmark tab 
        self._benchmark_tab = None
        self._benchmark = None
        self._benchmark_settings = None

        # analysis tab
        self._analysis_tab = None
        self._analysis = None

        self._last_model_path: Optional[Path] = None

        self._last_instructon_file: Optional[Path] = None
        
        self._sidebar = None
        self._database_path : Optional[str] = None # either a connection str or a file path
        self._use_sqlsvr : bool = False # use sqlite3 by default
        self._logger : Optional[Logger] = None
        self._logging_level: int = logging.INFO # default to INFO level


        self.active_view = None # : Optional[CTkAppView] = None
        self.active_view_name : Optional[str] = None

        self._access_mode = self.AccessModes.USER

        self._package_root: str | None = None
        self._sb_buttons: List[Dict[str, Union[Tuple[int,int], str, ctk.CTkButton]]] = []   

    def validate_button_list(self, buttons: List[Dict[str, Union[Tuple[int,int], str, ctk.CTkButton]]]) -> bool:
        """ Returns true is the validation is successful """
        if not isinstance(buttons, list):
            self.logger.error("Button list must be a list.")
        
        for i, item in enumerate(buttons):
            if not isinstance(item, dict):
                self.logger.error(f"Element at index {i} must be a dictionary, but got {type(item).__name__}")
                return False
            
            # Validate the values within the dictionary
            for key, value in item.items():
                is_tuple_of_ints = isinstance(value, tuple) and len(value) == 2 and all(isinstance(x, int) for x in value)
                is_string = isinstance(value, str)
                is_button = isinstance(value, ctk.CTkButton)
                if not (is_tuple_of_ints or is_string or is_button):
                    self.logger.error(f"Button list validation failed, Value for key '{key}' at index {i} must be a tuple of two integers or a string or a button. Got {type(value).__name__}")
                    return False
                        
        # print("Validation successful!")
        return True

    def get_button(self, name: str) -> ctk.CTkButton | None:
        for i, item in enumerate(self._sb_buttons):
            if isinstance(item, dict) and 'name' in item and 'button' in item and item['name'] == name and isinstance(item['button'], ctk.CTkButton):
                return item['button']
        return None
            

    @property 
    def sb_buttons(self)-> List[Dict[str, Union[Tuple[int,int], str, ctk.CTkButton]]]:
        return self._sb_buttons
    
    @sb_buttons.setter
    def sb_buttons(self, button_list: List[Dict[str, Union[Tuple[int,int], str, ctk.CTkButton]]]) -> None:
        if self.validate_button_list(button_list):
            self._sb_buttons = button_list

    @property
    def last_model_path(self) -> Path:
        if self._last_model_path is not None:
            return self._last_model_path
        else:
            return Path("./")
        
    @last_model_path.setter
    def last_model_path(self, path: Path):
        if path.exists() and path.is_dir():
            with self._lock:
                self._last_model_path = path
        else:
            self.logger.error(f"Invalid path passed to last_model_path: {path}")

    @property
    def last_instruction_file(self) -> Path | None:
        return self._last_instruction_file
        
    @last_instruction_file.setter
    def last_instruction_file(self, new_file_path: str | Path) -> None:
        fp = Path(new_file_path)
        # 1. Check if it exists
        if not fp.exists():
            self.logger.error(f"Error: File not found at path: {new_file_path}")
            # raise FileNotFoundError(f"Error: File not found at path: {new_file_path}")

        # 2. Check if it is a file (and not a directory)
        elif not fp.is_file():
            self.logger.error(f"Error: Path is not a file: {new_file_path}")
            # raise NotADirectoryError(f"Error: Path is not a file: {new_file_path}")

        # 3. Check if the extension is '.md'
        elif fp.suffix.lower() != '.md':
            self.logger.error(f"Error: File must be a markdown file. Found extension: {fp.suffix}")
            # raise ValueError(f"Error: File must be a markdown file. Found extension: {fp.suffix}")
            
        # If all checks pass, the assignment proceeds normally
        else:
            self.logger.debug(f"Updated last instruction file to '{new_file_path}'")
            self._last_instruction_file = fp 
            

    @property
    def package_root(self) -> str:
        if self._package_root is None or len(self._package_root) == 0:
            self._package_root = str(Path(localmind.__file__).resolve().parents[2])
        return self._package_root
    
    @package_root.setter
    def package_root(self, new_path: str) -> None:
        with self._lock:
            if Path(new_path).exists():
                self._package_root = new_path

    @property
    def logger(self) -> Logger:
        if self._logger is None:
            self._logger = init_logger(filename=self._app_name if self._app_name is not None else "LocalMind", level=self.logging_level, log_dir=self._home_dir if self._home_dir is not None else ".\\")
        return self._logger
        
    @logger.setter
    def logger(self, logger: Logger) -> None: 
        if isinstance(logger, Logger):
            with self._lock:
                self._logger = logger
                self._logger.setLevel(self.logging_level)

    @property
    def logging_level(self) -> int:
        return self._logging_level

    @logging_level.setter
    def logging_level(self, level: int) -> None:
        if isinstance(level, int) and level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]:
            with self._lock:
                self._logging_level = level
                if self._logger is not None:
                    self._logger.setLevel(level)
        else:
            self.logger.error(f"Invalid logging level: {level}. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL.")

    @property 
    def database_path(self) -> str:
        if self._database_path is not None:
            return self._database_path
        else:
            return ""
    
    @database_path.setter
    def database_path(self, path: str) -> None:
        with self._lock:
            self._database_path = path

    @property
    def use_sqlsvr(self) -> bool:
        return self._use_sqlsvr 

    @use_sqlsvr.setter
    def use_sqlsvr(self, value: bool) -> None:
        if not isinstance(value, bool):
            return
        with self._lock:
            self._use_sqlsvr = value
    # @property
    # def sidebar(self):
    #     with self._lock:
    #         return self._sidebar
    
    # @sidebar.setter
    # def sidebar(self, sb):
    #     with self._lock:
    #         self._sidebar = sb
    
    @property
    def settings_tab(self):
        return self._settings_tab
    
    @settings_tab.setter
    def settings_tab(self, tab):
        with self._lock:
            self._settings_tab = tab
    
    @property
    def lm_settings_tab(self):
        return self._lm_settings_tab
    
    @lm_settings_tab.setter
    def lm_settings_tab(self, tab):
        with self._lock:
            self._lm_settings_tab = tab
    @property
    def lm_server_tab(self):
        return self._lm_server_tab
    
    @lm_server_tab.setter
    def lm_server_tab(self, tab):
        with self._lock:
            self._lm_server_tab = tab

    @property
    def benchmark_tab(self):
        return self._benchmark_tab
    
    @benchmark_tab.setter
    def benchmark_tab(self, tab):
        with self._lock:
            self._benchmark_tab = tab

    @property
    def benchmark(self):
        return self._benchmark
    
    @benchmark.setter
    def benchmark(self, tab):
        with self._lock:
            self._benchmark = tab

    @property 
    def benchmark_settings(self):
        return self._benchmark_settings
    
    @benchmark_settings.setter
    def benchmark_settings(self, settings) -> None:
        with self._lock:
            self._benchmark_settings = settings

    @property
    def lm_settings(self):
        return self._lm_settings
    
    @lm_settings.setter
    def lm_settings(self, settings):
        with self._lock:
            self._lm_settings = settings

    @property
    def lm_server(self):
        return self._lm_server
    
    @lm_server.setter
    def lm_server(self, server):
        with self._lock:
            self._lm_server = server

    @property
    def server_settings(self) -> dict[str, Any]:
        return self._server_settings
    
    @server_settings.setter
    def server_settings(self, settings: dict[str, Any]) -> None:
        if not isinstance(settings, dict):
            self.logger.error(f"Error: server_settings must be a dictionary. Got {type(settings).__name__}")
            return
        with self._lock:
            self._server_settings = settings

    @property
    def database_manager_tab(self):
        return self._database_manager_tab
    
    @database_manager_tab.setter
    def database_manager_tab(self, tab):
        with self._lock:
            self._database_manager_tab = tab

    @property
    def database_manager(self):
        return self._database_manager
    
    @database_manager.setter
    def database_manager(self, tab):
        with self._lock:
            self._database_manager = tab

    @property
    def analysis_tab(self):
        return self._analysis_tab
    
    @analysis_tab.setter
    def analysis_tab(self, tab):
        with self._lock:
            if not isinstance(tab, ctk.CTkFrame):
                self.logger.error(f"Error: analysis_tab must be a CTkFrame. Got {type(tab).__name__}")
                return  
            self._analysis_tab = tab

    @property
    def analysis(self):
        return self._analysis
    
    @analysis.setter
    def analysis(self, a):
        with self._lock:
            self._analysis = a

    @property
    def settings(self):
        return self._settings
    
    @settings.setter
    def settings(self, s):
        with self._lock:
            self._settings = s
    
    @property
    def instructions_tab(self):
        return self._instructions_tab
    
    @instructions_tab.setter
    def instructions_tab(self, n):
        with self._lock:
            self._instructions_tab = n

    @property
    def instructions(self):
        return self._instructions
    
    @instructions.setter
    def instructions(self, n):
        with self._lock:
            self._instructions = n
    
    @property
    def home(self):
        return self._home_dir
    
    @home.setter
    def home(self, path):
        with self._lock:
            self._home_dir = path

    @property
    def access_mode(self):
        return self._access_mode
    
    @access_mode.setter
    def access_mode(self, mode):
        if mode >= self.AccessModes.USER and mode <= self.AccessModes.ADMIN:
            with self._lock:
                self._access_mode = mode
