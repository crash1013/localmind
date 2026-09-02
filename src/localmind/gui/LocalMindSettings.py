# LocalMindSettings.py

import json
import shutil
import sys
from logging import Logger
from localmind.utils.initLogger import init_logger
from pathlib import Path
from pydantic import BaseModel, ConfigDict, ValidationError, Field, field_validator
from typing import Optional


config_data = {
    "llama_exe_paths": [ "C:/llama-vulkan-release/bin/", "C:/llanna-sycl-release/bin/"],
    "llama_exe_path": "C:/llama-vulkan-release/bin/",
    "model_path": "/home/crash/models",
    "models": [
        "gemma-4-E2B-it-Q8_0.gguf", 
        "gemma-4-E4B-it-Q4_K_M.gguf",
        "gemma-4-E4B-it-Q6_K.gguf",
        "gemma-4-E4B_q4_0-it.gguf",
        "gemma-4-E2B_q4_0-it.gguf",
        "granite-4.1-8b-Q4_K_M.gguf",
        "granite-4.1-8b-Q6_K.gguf"
    ],
    "last_model": "gemma-4-E4B_q4_0-it.gguf",
    "api_key": "",
    "context_size": 4096,
    "host": "127.0.0.1",
    "port": "8081",
    "gpu_layers": "999"
}

class LMSettings(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    # Active override. If None, LocalMind uses PATH.
    llama_exe_path: Optional[str] = None

    # Recently used / known executable paths.
    llama_exe_paths: list[str] = Field(default_factory=list)

    model_path: str
    models: list[str]
    last_model: str
    api_key: Optional[str] = None
    context_size: int
    host: str
    port: int = Field(ge=1, le=65535)
    gpu_layers: str

    @field_validator("llama_exe_path", mode="before")
    @classmethod
    def normalize_llama_exe_path(cls, value: object) -> object:
        if value == "":
            return None
        return value

    @field_validator("llama_exe_paths", mode="before")
    @classmethod
    def normalize_llama_exe_paths(cls, value: object) -> object:
        if value is None:
            return []
        return value 

def platform_exe_name(name: str) -> str:
    if sys.platform.startswith("win") and not name.endswith(".exe"):
        return f"{name}.exe"
    return name


def resolve_llama_executable(settings: LMSettings, exe_name: str) -> str:
    exe_name = platform_exe_name(exe_name)

    if settings.llama_exe_path:
        base = Path(settings.llama_exe_path)

        # If user selected the exact executable
        if base.is_file():
            return str(base)

        # If user selected the llama.cpp bin directory
        candidate = base / exe_name
        if candidate.exists():
            return str(candidate)

        raise FileNotFoundError(f"Could not find {exe_name} in {base}")

    # No explicit setting: fall back to PATH
    found = shutil.which(exe_name)
    if found:
        return found

    raise FileNotFoundError(
        f"{exe_name} was not found. Set llama_exe_path or add it to PATH."
    )
    
class LocalMindSettings:

    def __init__(self, app_name: str = "localmind", logger: Optional[Logger] = None) -> None:
        self._users_home: Path = Path.home() / f".{app_name}"
        self._settings_path: Path = self._users_home / "lm_settings.json"
        self._database_path: Path = self._users_home / f"{app_name}.db"

        if logger is None:
            self.logger = init_logger(filename="LocalMindSettings.log", log_dir=self.users_home)
        else:
            self.logger = logger
        
        self.init_settings()
        
        
        try:
            self.settings: LMSettings = self.load_settings(str(self._settings_path))
            self.logger.debug(f"LMSettings successfully loaded from file: \n{self.settings}")
        except FileNotFoundError:
            self.logger.warning(f"Settings file not found at {self._settings_path}")
        except ValidationError as e:
            error_details = e.errors()

            self.logger.error("Settings file validation failed. Details:")

            for error in error_details:
                self.logger.error(f"  - Field '{e}'")
                
        except Exception as e:
            self.logger.error("LMSettings load error: {e}")

    def init_settings(self) -> bool:
        """ Initialize settings with default values from config_data. 
            This is used when no settings file is found or when the settings file is invalid. 
            Returns True if initialization is successful, False otherwise."""
        
        result: bool = False
        if not Path.exists(self._settings_path):
            self._settings_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._settings_path, "w", encoding="utf-8") as fp:
                json.dump({
                    "llama_exe_path": "",
                    "llama_exe_paths": [
                        "",
                    ],
                    "model_path": "",
                    "models": [ "",
                    ],
                    "last_model": "",
                    "api_key": "",
                    "context_size": 4096,
                    "host": "0.0.0.0",
                    "port": 8081,
                    "gpu_layers": "999"
                }, fp)
        try:
            self.settings = LMSettings.model_validate(config_data)
            result = True
        except ValidationError as e:
            self.logger.error(f"Default settings initialization error: {e}")
        return result
        
    def load_settings(self, filename: str | Path) -> LMSettings:
        """
        Load application settings from a JSON file.

        Args:
            filename: Path to the JSON configuration file.

        Returns:
            Validated LMSettings instance.
        """

        with open(filename, "r", encoding="utf-8") as fp:
            data = json.load(fp)

        return LMSettings.model_validate(data)
    
    def save_settings(self, filename: str | Path) -> bool:
        """
        Save application settings to a JSON file.

        Args:
            filename: Path to the JSON configuration file.

        Returns:
            True if save is successful, False otherwise.
        """
        result: bool = False
        try:
            with open(filename, "w", encoding="utf-8") as fp:
                json.dump(self.settings.model_dump(), fp, indent=4)
            result = True
        except Exception as e:
            self.logger.error(f"Error saving settings to {filename}: {e}")
        return result
    
    
    @property
    def users_home(self) -> Path:
        """
            return the users home directory for this application ~/.localmind 
        """
        return self._users_home
    
    @users_home.setter
    def users_home(self, new_home: str | Path) -> None:
        """
            Set the users home to the directory named new_home if new_home is a
            directory and it exists.
        """
        p : Path = Path(new_home)
        if p.exists() and p.is_dir():
            self._users_home = p
        else:
            self.logger.error(f"Specified user home directory does not exist or is not a directory: {str(p)}")

    @property 
    def database_path(self) -> Path:
        return self._database_path

    @database_path.setter
    def database_path(self, new_path: str | Path) -> None:  
        p: Path = Path(new_path)
        if p.exists() and p.is_file():
            self._database_path = p
        else:
            self.logger.error(f"Database file does not exist: {str(new_path)}")

    @property
    def settings_path(self) -> Path:
        return self._settings_path
    
    @settings_path.setter
    def settings_path(self, new_path: str | Path) -> None:
        p : Path = Path(new_path)

        if p.exists() and p.is_file():
            self._settings_path = p
        else:
            self.logger.error(f"Settings file does not exist: {str(new_path)}")

