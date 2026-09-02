# initLogger

import logging
from pathlib import Path
import sys
from logging.handlers import RotatingFileHandler
from typing import Union, Optional

def init_logger(filename: Union[str, Path], 
                level: int=logging.DEBUG, 
                log_dir: Optional[Union[str, Path]] = None,
                format: str = '%(asctime)s  %(name)s  %(levelname)s: %(message)s',
                max_bytes: int = 1000000,
                backup_count: int = 10,
                silent: bool = False,
                enable_console_handler: bool = True,
                enable_file_handler: bool = True) -> logging.Logger:
    """
    Initializes and returns a logger with both file and console handlers. Each handler, file and console, can be enabled or disabled independently.
    The identity of the logger comes from 'filename',
    The location of the resulting log file is controlled by 'log_dir' when 'log_dir' is provided otherwise the log file is created in the same directory as 'filename'.

    Logic:
    1. If log_dir is provided: The log file is placed in log_dir using filename's stem.
       (Any directory info inside filename is ignored).
    2. If log_dir is None: The log file is placed in the same directory as filename.    

    This function creates a logger using the provided filename to determine the logger's name and the file name for logging.
    If the filename contains an extension, the logger's name will be the filename without the extension.
    If the filename does not contain an extension, the logger's name will be the filename, and a '.log' extension will be appended to the file name.

    The logger is configured with:
    - A rotating file handler that writes logs to a file, with a default maximum file size of 1MB and up to 10 backup files.
    - A console handler that outputs logs to the console (sys.stdout).
    Both handlers use the same log format.

    Parameters:
    - filename (str): The base name for the log file. If it does not contain an extension, '.log' will be appended.
    - level (int, optional): The logging level threshold. Default is logging.DEBUG.
    - log_dir (str or Path, optional): The directory where the log file will be stored. If None, the log file will be created in the same directory as the filename.
    - format (str, optional): The log message format. Default is '%(asctime)s  %(name)s  %(levelname)s: %(message)s'.
    - maxBytes (int, optional): The maximum size of the log file in bytes before it is rotated. Default is 1,000,000 bytes.
    - backupCount (int, optional): The number of backup log files to keep. Default is 10.
    - silent (bool, optional): If True, suppresses log messages during initialization. Default is False.
    - enable_console_handler (bool, optional): If True, enables the console handler. Default is True.
    - enable_file_handler (bool, optional): If True, enables the file handler. Default is True.

    Returns:
    - logging.Logger: The configured logger instance.

    Raises:
    - Exception: If there is an error initializing the logger, an exception is raised and printed.

    Example:
    >>> logger = init_logger('app_log')
    >>> logger.info('This is an info message')
    """
    valid_levels = {logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL}
    if level not in valid_levels:
        raise ValueError(f"Invalid logging level: {level}. Must be one of {valid_levels}")
    # ensure at least one handler is enabled
    if not enable_console_handler and not enable_file_handler:
        enable_console_handler = True

    # 1. Convert filename to Path object immediately and determine logger name and log file path
    log_path = Path(filename).expanduser()
    # 1. Determine the logger's name (stem of the filename)
    logname = log_path.stem

    if log_dir is not None:
        log_dir_path = Path(log_dir).expanduser()
    else:       
        log_dir_path = log_path.parent
    
    
    # 2. Determine the actual file name for logging (ensuring it ends in .log)
    # We use the original filename (without extension) and append .log
    # If input is 'app.log', log_file_base is 'app'
    log_file_path = log_dir_path / (logname + '.log')

    try:
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        if not silent:
            print(f"Failed to create log directory {log_file_path.parent}: {e}")
            print(f"Logger initialization failed for {logname}")
        raise

    logger = logging.getLogger(logname)

    # Check if the logger already has handlers to avoid duplicate logs
    if not logger.hasHandlers():
        try:
            # File handler (using the determined log_file_path)
            log_formatter = logging.Formatter(format)
            if enable_file_handler:
                if not isinstance(max_bytes, int) or not isinstance(backup_count, int):
                    raise ValueError("max_bytes and backup_count must be integers.")
                if max_bytes <= 0 or backup_count < 0:
                    raise ValueError("max_bytes must be positive and backup_count must be non-negative.")
                log_handler = RotatingFileHandler(str(log_file_path), maxBytes=max_bytes, backupCount=backup_count)
                log_handler.setFormatter(log_formatter)
                logger.addHandler(log_handler)

            # Stream handler (console)
            if enable_console_handler:
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(log_formatter)
                logger.addHandler(console_handler)

            logger.propagate = False  # Prevent log messages from being propagated to the root logger
            logger.setLevel(level)

            if not silent:
                logger.debug(f"{logname} logger starting up. Logging to {log_file_path}")
        except Exception as e:
            if not silent:
                print(f"Failed to initialize logger {logname}: {e}")
            raise
            
    if not silent:
        logger.info(f"{logname} logger initialized successfully")
        
    return logger

if __name__=="__main__":
    # Test Case 1: No extension input
    logger1 = init_logger(filename = "test_log_file")
    logger1.error("Test 1: Error message.")

    print("-" * 20)

    # Test Case 2: Invalid extension input, should still create a .log file
    logger2 = init_logger(filename = "api_log.txt")
    logger2.info("Test 2: Info message from API log.")