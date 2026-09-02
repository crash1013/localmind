import customtkinter as ctk # type: ignore

from localmind.widgets.CTkYesNo import CTkYesNo
from tkinter import filedialog

from localmind.gui.CTkAppData import CTkAppData
from localmind.gui.CTkAppView import CTkAppView
from pathlib import Path
from logging import Logger

from typing import Union, Tuple, List, Dict, Optional
from localmind.gui.LocalMindSettings import LocalMindSettings

from pydantic import ValidationError

from logging import Logger
from ipaddress import ip_address
import socket



class CTkLMSettings(CTkAppView):
    def __init__(self, parent: ctk.CTk, frame: ctk.CTkFrame, font: Union[ctk.CTkFont, Tuple[str, int, str]], data: CTkAppData):
        super().__init__(parent, frame, font, data)
        self._settings: LocalMindSettings = LocalMindSettings(app_name=self.data._app_name if self.data._app_name is not None else "LocalMind", logger=self.data.logger)
        self.initialize_widgets()
        self.settings_changed: bool = False
        
    def on_close_tab(self) -> None:
        """ Called when the tab is closed. Override in derived classes for custom behavior. """
        self.data.logger.debug(f"{self.__class__}.on_tab_closed() called")
        if self.settings_changed:
            dialog = CTkYesNo(self.parent, title="Unsaved Changes", message="Save updated settings?", font=self.font)
            if dialog.result:
                self.on_save_settings()
                self.settings_changed = False

    @property
    def settings(self) -> LocalMindSettings:
        return self._settings
    
    @settings.setter
    def settings(self, new_settings: LocalMindSettings):
        self._settings = new_settings
        self.settings_changed = True

    def initialize_widgets(self) -> None:
        self.frame.grid_columnconfigure(0, weight=1)

        self.model_frame = self.labeled_frame(self.frame, 
                                              label="Model Selection", 
                                              parent_row=0, 
                                              parent_column=0, 
                                              columns = 2,
                                              column_weight=[0, 1])
        
        self.model_path_label = ctk.CTkLabel(self.model_frame, text="Model Path:", font=self.font)
        self.model_path_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.model_path_var = ctk.StringVar(value=self.settings.settings.model_path)
        self.model_path_var.trace_add("write", self.on_model_path_changed)

        self.model_path_entry = ctk.CTkEntry(self.model_frame, font=self.font, textvariable=self.model_path_var)
        self.model_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        # setup the model combobox
        self.model_label = ctk.CTkLabel(self.model_frame, text="Model:", font=self.font)
        self.model_label.grid(row=1, column=0, padx=10, pady=10, sticky = "w")

        self.model_var = ctk.StringVar(value=self.settings.settings.last_model)
        self.model_combo = ctk.CTkComboBox(self.model_frame, command=self.on_model_changed, font=self.font, variable=self.model_var, values=list(self.find_gguf_models(Path(self.model_path_var.get())).keys()))
        self.model_combo.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        #----------------------------------------------------------------------
        self.model_config_frame = self.labeled_frame(self.frame, 
                                                           label="Model Configuration", 
                                                           parent_row=1, 
                                                           parent_column=0, 
                                                           columns=2, 
                                                           column_weight=[0,1],
                                                           row0_weight=0)
        self.model_context_size_label = ctk.CTkLabel(self.model_config_frame, text="Context:", font=self.font)
        self.model_context_size_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        self.model_context_size_var = ctk.StringVar(value=str(self._settings.settings.context_size))
        self.model_context_size_var.trace_add("write", self.update_context_size)
        self.model_context_size_entry = ctk.CTkEntry(self.model_config_frame, font=self.font, textvariable=self.model_context_size_var)
        self.model_context_size_entry.grid(row=0, column=1, padx=10, pady=10, sticky='new')

        self.gpu_layers_label = ctk.CTkLabel(self.model_config_frame, text = "GPU Layers:", font=self.font)
        self.gpu_layers_label.grid(row=1, column=0, padx=10, pady=10, sticky='nw')
        self.gpu_layers_var = ctk.StringVar(value=self._settings.settings.gpu_layers)
        self.gpu_layers_var.trace_add('write', self.on_gpu_layers_changed)
        self.gpu_layers_entry = ctk.CTkEntry(self.model_config_frame, font=self.font, textvariable=self.gpu_layers_var )
        self.gpu_layers_entry.grid(row=1, column=1, padx=10, pady=10, sticky='new')

        #----------------------------------------------------------------------  
        self.server_settings_frame = self.labeled_frame(self.frame, 
                                                        label="Server Configuration",
                                                         parent_row = 2,
                                                         parent_column=0,
                                                         columns=2,
                                                         column_weight=[0, 1]
                                                        )
        self.llama_exe_paths_label = ctk.CTkLabel(self.server_settings_frame, text="Llama Executable Path:", font=self.font)
        self.llama_exe_paths_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.llama_exe_paths_var = ctk.StringVar(value=self._settings.settings.llama_exe_path if self._settings.settings.llama_exe_path else "")
        self.llama_exe_paths_var.trace_add("write", self.on_llama_exe_path_changed)
        self.llama_exe_paths_combo = ctk.CTkComboBox(self.server_settings_frame, font=self.font, variable=self.llama_exe_paths_var, values=self._settings.settings.llama_exe_paths)
        self.llama_exe_paths_combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.server_host_label = ctk.CTkLabel(self.server_settings_frame, text=self.get_host_label(), font=self.font)
        self.server_host_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.server_host_var = ctk.StringVar(value=self._settings.settings.host)

        self.server_host_entry = ctk.CTkEntry(self.server_settings_frame, font=self.font, textvariable=self.server_host_var)
        self.server_host_entry.bind("<FocusOut>", self.on_host_changed)
        self.server_host_entry.bind("<Return>", self.on_host_changed)
        self.server_host_entry.bind("<FocusIn>", self.on_host_focus_in)

        self.server_host_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.server_port_label = ctk.CTkLabel(self.server_settings_frame, text="Port:", font=self.font)
        self.server_port_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.port_var = ctk.StringVar(value=str(self._settings.settings.port))
        self.port_var.trace_add("write", self.on_port_changed)

        self.server_port_entry = ctk.CTkEntry(self.server_settings_frame, font=self.font, textvariable=self.port_var)
        self.server_port_entry.grid(row=3, column=1, padx=10, pady=10, sticky='ew')

        self.server_api_key_label = ctk.CTkLabel(self.server_settings_frame, font=self.font, text="api key:")
        self.server_api_key_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        self.api_key_var = ctk.StringVar(value=str(self._settings.settings.api_key))
        self.api_key_var.trace_add("write", self.on_api_key_changed)

        self.api_key_entry = ctk.CTkEntry(self.server_settings_frame, font=self.font, textvariable=self.api_key_var)
        self.api_key_entry.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

        self.control_frame = self.labeled_frame(self.frame, 
                                                label="Controls",
                                                parent_row = 4,
                                                parent_column=0,
                                                columns=3,
                                                column_weight=[1, 1, 1]
                                                )
        self.browse_model_path_button = ctk.CTkButton(self.control_frame, 
                                                     text="Browse Model Path", 
                                                     font=self.font, 
                                                     command=self.on_browse_model_path)
        self.browse_model_path_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.browse_exe_paths_button = ctk.CTkButton(self.control_frame,
                                                     text="Browse Executable Paths",
                                                     font=self.font,
                                                     command=self.on_browse_exe_paths)
        self.browse_exe_paths_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        self.save_button = ctk.CTkButton(self.control_frame,
                                         text="Save Settings",
                                         font=self.font,
                                         command=self.on_save_settings)
        self.save_button.grid(row=0, column=2, padx=10, pady=10, sticky='ew')

    def sb_button_list(self) -> List[str]:
        """ return the list of supported button names """
        return []

    def on_visible(self) -> None:
        """ change the text of the buttons we use to reflect the current view"""
        pass

    def on_llama_exe_path_changed(self, *args) -> None:
        new_value = self.llama_exe_paths_var.get()
        self._settings.settings.llama_exe_path = new_value
        self.settings_changed = True

    def on_browse_exe_paths(self, *args) -> None:
        """
        Opens the OS directory selection dialog and updates the UI with the selected path.
        """
        # The core function: asking the user for a directory path
        folder_selected = filedialog.askdirectory(initialdir=Path(self._settings.settings.llama_exe_path) if self._settings.settings.llama_exe_path else None,
                                                    title="Select Llama Executable Directory",
                                                    mustexist=True)

        
        if folder_selected:
            self.data.logger.debug(f"User selected executable directory: {folder_selected}")
            # Update the GUI label to show the path
            if folder_selected not in self._settings.settings.llama_exe_paths:
                self._settings.settings.llama_exe_paths.append(folder_selected)
                self.llama_exe_paths_combo.configure(values=self._settings.settings.llama_exe_paths)
                self.settings_changed = True
        else:
            self.data.logger.debug("User cancelled the browse executable path operation.")    
            
    def on_browse_model_path(self, *args) -> None:
        """
        Opens the OS directory selection dialog and updates the UI with the selected path.
        """
        # The core function: asking the user for a directory path
        folder_selected = filedialog.askdirectory()
        
        if folder_selected:
            self.data.logger.debug(f"User selected model directory: {folder_selected}")
            # Update the GUI label to show the path
            self.model_path_var.set(folder_selected)
            self.settings_changed = True
        else:
            self.data.logger.debug("User cancelled the browse model path operation.")

    def on_save_settings(self, *args) -> None:
        result = self._settings.save_settings(self._settings.settings_path)
        self.settings_changed = False
        self.data.logger.debug(f"Saving lm settings: \n{self._settings.settings} \nto {self._settings.settings_path}")
        if result:
            self.data.logger.debug("LMSettings updated successfully")
        else:
            self.data.logger.warning("Error saving LMSettings")

        

    def on_api_key_changed(self, *args) -> None:
        pass

    def on_port_changed(self, *args) -> None:
        try:
            port: int = int(self.port_var.get())
            self._settings.settings.port = port
            self.settings_changed = True
        except ValidationError as e:
            self.data.logger.error(f"Pydantic validation failed: {e}")
        except ValueError as e:
            self.data.logger.error(f"Invalid port, not a number: {e}")


    def get_host_label(self, valid: Optional[bool] = None) -> str:
        prefix = '?' if valid is None else "✓" if valid else "✗"
        return prefix + " Host:"

    def is_valid_ip(self, value: str) -> bool:
        try:
            ip_address(value)
            return True
        except ValueError:
            return False
    
    def is_valid_hostname(self, hostname: str) -> bool:
        try:
            socket.getaddrinfo(hostname, None)
            return True
        except socket.gaierror:
            return False    
        
    def on_host_focus_in(self, *args) -> None:
        self.server_host_label.configure(require_redraw=True, text=self.get_host_label())

    def on_host_changed(self, *args) -> None:
        new_value = self.server_host_var.get().strip()

        self.settings_changed = True

        if not new_value:
            self.server_host_label.configure(require_redraw=True, text=self.get_host_label())
            return
        bool_valid_host = False
        if self.is_valid_ip(new_value):
            self.server_host_label.configure(require_redraw=True, text=self.get_host_label(valid=(bool_valid_host := True)))
        elif len(new_value) < 3:
            self.server_host_label.configure(require_redraw=True, text=self.get_host_label())
        elif self.is_valid_hostname(new_value):
            self.server_host_label.configure(require_redraw=True, text=self.get_host_label(valid=(bool_valid_host := True)))
        else:
            self.server_host_label.configure(require_redraw=True, text=self.get_host_label(valid=False))
        if bool_valid_host:
            self._settings.settings.host = new_value

    def on_gpu_layers_changed(self, *args) -> None:
        self.settings_changed = True
        new_value: str = self.gpu_layers_var.get()
        if new_value.isdigit():
            self._settings.settings.gpu_layers = new_value

    def update_model_combo(self) -> None:
        self.settings_changed = True
        self.model_combo.configure(require_redraw=True, values=self.find_gguf_models(Path(self.model_path_var.get())))
        self._settings.settings.models = list(self.model_combo.cget('values'))

    def update_context_size(self, *args) -> None:
        self.settings_changed = True
        new_size = self.model_context_size_var.get()
        self._settings.settings.context_size = int(new_size)


    def on_model_changed(self, model: str) -> None:
        self.settings_changed = True
        self._settings.settings.last_model = model

    def on_model_path_changed(self, *args) -> None:
        path = Path(self.model_path_var.get())
        if path.exists():
            self.settings_changed = True
            self._settings.settings.model_path = str(path)
            self.update_model_combo()

    def find_gguf_models(self, model_root: Path | str) -> Dict[str, Path]:
        """
        Recursively find .gguf files under model_root.

        Returns:
            dict mapping display name -> full model path
        """
        if isinstance(model_root, str):
            model_root = Path(model_root) # ensure the path is a Path
        if not model_root.exists() or not model_root.is_dir():
            if isinstance(self.data.logger, Logger):
                self.data.logger.debug(f"model_root: '{str(model_root)}' does not exist or is not a directory")
            return {}

        model_files: list[Path] = sorted(
            model_root.rglob("*.gguf"),
            key=lambda p: str(p.relative_to(model_root)).lower()
        )

        models: Dict[str, Path] = {}

        for path in model_files:
            display_name = str(path.relative_to(model_root))

            # Use forward slashes in UI, even on Windows
            display_name = display_name.replace("\\", "/")

            models[display_name] = path

        return models
