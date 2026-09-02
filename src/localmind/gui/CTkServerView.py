# CTkServerView.py

import customtkinter as ctk # type: ignore
from pathlib import Path
from enum import IntEnum
from typing import Union, Tuple, List, Any
import subprocess
import threading
import copy 

from localmind.widgets.CTkYesNo import CTkYesNo
from localmind.gui.CTkAppData import CTkAppData
from localmind.gui.CTkAppView import CTkAppView
from localmind.widgets.LlamaBenchSettingsDialog import LlamaBenchSettingsDialog
from localmind.utils.llama_server_help_spec import HELP_SPEC
from localmind.utils.kill_llama_servers import kill_llama_servers, get_llama_server_procs
from localmind.gui.LocalMindSettings import LocalMindSettings, resolve_llama_executable

class CTkServerView(CTkAppView):
    class status(IntEnum):
        STOP = 0
        RUN = 1
        ERROR = 2

    def __init__(self, parent: ctk.CTk, frame: ctk.CTkFrame, font: Union[ctk.CTkFont, Tuple[str, int, str]], data: CTkAppData) -> None:
        super().__init__(parent, frame, font, data)
        self._settings: LocalMindSettings = LocalMindSettings(app_name=self.data._app_name if self.data._app_name is not None else "LocalMind",
                                                              logger=self.data.logger)
        self._server_settings: dict[str, Any] = copy.deepcopy(HELP_SPEC)
        self.server_options: dict[str, Any] = {}
        self.initialize_widgets()
        self.process: subprocess.Popen[str] | None = None
        self.server_status = self.status.STOP
        self.last_server_command: list[str] | None = None

    def sb_button_list(self) -> List[str]: # no buttones yet
        self.data.logger.debug(f"{self.__class__.__name__}: sb_button_list returned  [ 'first', 'last' 'edit', 'new'].")
        return [ 'first', 'last', 'edit', 'new']

    def on_visible(self) -> None:
        """ change the text of the buttons we use to reflect the current view"""
        self.set_button_names({
            "first": "Start",
            "last": "Stop",
            "edit": "Parameters",
            "new": "Clear"
        })
        if self.run_button is not None and self.stop_button is not None:
            if self.process is not None and self.process.poll() is None:
                self.run_button.configure(state="disabled")
                self.stop_button.configure(state="normal")
            else:
                self.run_button.configure(state="normal")
                self.stop_button.configure(state="disabled")

    def on_close_tab(self) -> None:
        """ Called when the tab is closed. Override in derived classes for custom behavior. """
        self.data.logger.debug(f"{self.__class__}.on_tab_closed() called")

    def initialize_widgets(self) -> None:
        # set the start and stop buttons
        self.run_button: ctk.CTkButton | None = self.data.get_button('first')
        self.stop_button: ctk.CTkButton | None = self.data.get_button('last')
        # relabel the first and last sidebar buttons to Start and Stop and enable them
        self.clear_button: ctk.CTkButton | None = self.data.get_button('new')
        self.edit_button: ctk.CTkButton | None = self.data.get_button('edit')

        if self.run_button is not None:
            self.data.logger.debug(f"{self.__class__.__name__}: run_button found.")
            self.run_button.configure(state="normal")
        if self.stop_button is not None:
            self.data.logger.debug(f"{self.__class__.__name__}: stop_button found.") 
            self.stop_button.configure(state="disabled")    
        if self.run_button is not None:
            self.run_button.configure(text='Start')
        if self.stop_button is not None:
            self.stop_button.configure(text='Stop')
        if self.clear_button is not None:
            self.data.logger.debug(f"{self.__class__.__name__}: clear_button found.")
            self.clear_button.configure(text='Clear')
        if self.edit_button is not None:
            self.data.logger.debug(f"{self.__class__.__name__}: edit_button found.")
            self.edit_button.configure(text='Parameters')
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)

        self.message_label_frame = ctk.CTkFrame(self.frame, bg_color='transparent')
        self.message_label_frame.grid(row=0, column=0, padx=5, pady=(5,5), sticky='new')
        self.message_label_frame.grid_columnconfigure(0, weight=1)
        self.message_label_frame.grid_rowconfigure(0, weight=1)
        self.message_label = ctk.CTkLabel(self.message_label_frame, text="Server Output", font=self.font)
        self.message_label.grid(row=0, column=0, padx=5, pady=(5,5), sticky='ew')

        self.console_frame = ctk.CTkFrame(self.frame, bg_color='transparent')
        self.console_frame.grid(row=1, column=0, padx=5, pady=(5, 0), sticky='nsew')
        self.console_frame.grid_columnconfigure(0, weight=1)
        self.console_frame.grid_rowconfigure(0, weight=1)

        self.console = ctk.CTkTextbox(self.console_frame, wrap="word", font=self.font)
        self.console.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.update_server_options()
        self.show_server_options(self.server_options)

    def append_console(self, text: str) -> None:
        self.console.insert("end", text)
        self.console.see("end")

    def set_server_running(self, running: bool) -> None:
        if self.run_button is not None:
            self.run_button.configure(state="disabled" if running else "normal")
        if self.stop_button is not None:
            self.stop_button.configure(state="normal" if running else "disabled")

    def build_server_command(
        self,
        llama_server_path: str,
        options: dict[str, Any]
    ) -> list[str]:
        if options is None:
            return [llama_server_path]
        cmd = [llama_server_path]

        for option, value in options.items():
            if isinstance(value, bool):
                if value:
                    cmd.append(option)
            else:
                cmd.extend([option, str(value)])
        self.last_server_command = cmd
        return cmd

    def show_server_options(self, options: dict[str, Any]) -> None:
        for option, value in options.items():
            self.console.insert("end", f"{option}: {value}\n")

    def update_server_options(self) -> None:
        self._settings.settings = self._settings.load_settings(str(self._settings._settings_path))
        self.server_options['--model'] = str(Path(self._settings.settings.model_path) /  Path(self._settings.settings.last_model))
        self.server_options['--ctx-size'] = self._settings.settings.context_size
        self.server_options['--host'] = self._settings.settings.host
        self.server_options['--port'] = self._settings.settings.port
        self.server_options['--gpu-layers'] = self._settings.settings.gpu_layers
        if self._settings.settings.api_key:
            self.server_options['--api-key'] = self._settings.settings.api_key
        self.data.server_settings = self.server_options

    def update_server_settings(self) -> None:
        #self._settings.settings.model_path = self.server_options.get('--model', self._settings.settings.model_path)
        model_path = Path(self._settings.settings.model_path).expanduser().resolve()
        model_file_path = Path(self.server_options['--model']).expanduser().resolve()
        self._settings.settings.last_model = str(model_file_path.relative_to(model_path))
        self._settings.settings.context_size = self.server_options.get('--ctx-size', self._settings.settings.context_size)
        self._settings.settings.host = self.server_options.get('--host', self._settings.settings.host)
        self._settings.settings.port = self.server_options.get('--port', self._settings.settings.port)
        self._settings.settings.gpu_layers = self.server_options.get('--gpu-layers', self._settings.settings.gpu_layers)
        self._settings.save_settings(str(self._settings._settings_path))
        self.data.server_settings = self.server_options

    def on_sidebar_first(self) -> None:
        "Start the server"
        self._settings = LocalMindSettings(app_name=self.data._app_name if self.data._app_name is not None else "LocalMind",
                                                              logger=self.data.logger)
        if self.process is not None and self.process.poll() is None:
            self.append_console("Server is already running.\n")
            return
        running_servers = get_llama_server_procs()
        if running_servers:
            yes_no = CTkYesNo(self.parent, title="Terminate Running Servers", message=f"Found running llama-server(s): {', '.join(str(p.pid) for p in running_servers)}. Do you want to terminate them?", font=self.font)
            if yes_no.result is False:
                self.append_console("User chose not to terminate running llama-server processes. Aborting server start.\n")
                return 
            self.append_console(f"Found {len(running_servers)} running llama-server processes. Attempting to terminate them...\n")
            pids = kill_llama_servers(logger=self.data.logger)
            if pids:
                self.append_console(f"Terminated llama-server processes: {pids}\n")
            else:
                self.append_console("No running llama-server processes found.\n")
        
        self.update_server_options()
        cmd = self.build_server_command(str(resolve_llama_executable(self._settings.settings, "llama-server")), self.server_options)
        start_message = f"Starting server:\n{' '.join(cmd)}\n\n"
        self.append_console(start_message)
        self.data.logger.info(start_message)

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        self.data.logger.debug(f"Popen started llama-server and returned: {type(self.process)}")
        
        if self.process.poll(): # the process started and stopped
            self.data.logger.debug("The process is 'stopped'")
            self.set_server_running(running=False)
        else:
            self.data.logger.debug("The server is running")
            self.set_server_running(running=True)
            thread = threading.Thread(target=self.read_server_output, daemon=True)
            thread.start()

    def read_server_output(self) -> None:
        if self.process is None or self.process.stdout is None:
            return

        for line in self.process.stdout:
            self.frame.after(0, self.append_console, line)

        return_code = self.process.poll()
        self.frame.after(0, self.append_console, f"\nServer exited with code {return_code}\n")


    def on_sidebar_last(self) -> None:
        "Stop the server"
        self.set_server_running(running=False)
        if self.process is None or self.process.poll() is not None:
            self.append_console("Server is not running.\n")
            return

        self.append_console("Stopping server...\n")
        self.process.terminate()

    def on_sidebar_edit(self) -> None:
        self.update_server_options()
        bsdlg = LlamaBenchSettingsDialog(self.parent, 
                                              self._server_settings, 
                                              font=self.font, 
                                              title="Server Settings", 
                                              current_options=self.server_options)
        if bsdlg.result is not None:
            self.server_options = bsdlg.result
            self.update_server_settings()
            self._settings.save_settings(str(self._settings._settings_path))
            self.show_server_options(self.server_options)

        if self.server_options is None:
            return

    def clear_server_output(self) -> None:
        self.console.delete("1.0", "end")
        self.append_console("Server output cleared.\n")

    def on_sidebar_new(self) -> None:
        """This sidebar buttons provides the clear function """
        self.clear_server_output()

