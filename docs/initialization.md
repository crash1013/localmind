# Initialization

## JSON INI files

LocalMind uses a number of JSON files to store static initialization settings. The settings in these files are normally handled as you use the application. All the initialization files are stored in the .localmind folder in the uses home directory.
When running localmind on Linux the filenames are case sensitive.

Linux Home Directory: `/home/<user id>/.localmind`

**Windows Home Directory**: `C:/Users/<user id>/.localmind`

## gui_settings.json
This file stores the information used to configure the appearance of the application.


```JSON
{
    "mode": "light",
    "theme": "E:/work/localmind/user_themes/Phoenix.json",
    "geometry": "2560x1369+-3646+216",
    "font": {
        "family": "Cascadia Code",
        "size": 18,
        "weight": "bold",
        "slant": "roman",
        "underline": 0,
        "overstrike": 0
    }
}
```

## LocalMind_settings.json

This file stores the primary application settings that define the location of various components and how the database is implemented. Currently the database can be provided by SQLITE or MS SQL Server. SQL Server is enabled when the use_sqlsvr value is set to true, otherwise SQLite is used by default.

```JSON
{
    "title": "LocalMind",
    "virtual_env": "E:\\work\\localmind\\win.venv\\Scripts\\python.exe",
    "database_path": "C:\\Users\\crash\\.localmind\\LocalMind.sqlite",
    "instruction_file": "E:\\work\\localmind\\docs\\LocalMind.pdf",
    "use_sqlsvr": false,
    "logging_level": 20
}
```

| Setting | Description | Default |
| :------- | :------------ | :-------- |
| title      | Used where a title is required | LocalMind |
| virtual_env | Used to restart and apply settings | Windows:<br> `<installation directory>\.venv\Scripts\python.exe`<br>Linux:<br> <installation directory>/.venv/bin/python |
| database_path | The file path to the Sqlite database file. | LocalMind.sqlite |
| instruction_path | Identifies the path to the file presented in the Instruction View. | <install directory>/docs/LocalMind.pdf |
| use_sqlsvr | Flag to enable SQL Server functionality | False |
| logging_level | Sets the logging level for the LocalMind Logger | DEBUG |


### Python Logging Levels

| Level | Numeric Value | Primary Usage & Guidance |
| :--- | :---: | :--- |
| **DEBUG** | 10 | Detailed diagnostic information used by developers to troubleshoot issues during development or deep debugging. |
| **INFO** | 20 | Confirmation that things are working as expected (e.g., service started, user logged in, scheduled job completed). |
| **WARNING** | 30 | An indication that something unexpected happened or a problem may occur soon (e.g., 'disk space low'), but the software is still working as expected. |
| **ERROR** | 40 | A serious issue occurred; the software was unable to perform a specific function or operation (e.g., database query failed). |
| **CRITICAL** | 50 | A severe error indicating that the program itself may be unable to continue running (e.g., complete system crash, out of memory). |
| **NOTSET** | 0 | When set on a logger, it delegates log level filtering to its parent logger. When set on a handler, it processes all events. |

### Access to SQL Server
Access to the SQL server is controlled by settings stored in the users environment.

```python
self.server = os.environ.get('SQL_SERVER', "127.0.0.1")
self.port = int(os.environ.get('SQL_PORT', 1433))
self.user = os.environ.get('SQL_SVR_USER', "user")
self.password = os.environ.get('SQL_SVR_PASSWORD', "password")
self.driver = os.environ.get('SQL_SVR_DRIVER', "ODBC Driver 18 for SQL Server")
```


## lm_settings.json

These settings are used with llama-server.  They tell LocalMind where to find llama.cpp, the models it uses, and some important settings for llama.cpp. Although there is a models settings it is not currently used, the application dynamically discovers the models at runtime based on the model_path setting.

```JSON

{
    "llama_exe_path": "C:/llama-vulkan-release/bin",
    "llama_exe_paths": [
        "C:/llama-vulkan-release/bin",
        "C:/llama-sycl-release/bin"
    ],
    "model_path": "C:\\lms_models",
    "models": [
        "lmstudio-community/gemma-4-12B-it-GGUF/gemma-4-12B-it-Q4_K_M.gguf",
        "lmstudio-community/gemma-4-12B-it-QAT-GGUF/gemma-4-12B-it-QAT-Q4_0.gguf",
        "lmstudio-community/gemma-4-26B-A4B-it-GGUF/gemma-4-26B-A4B-it-Q4_K_M.gguf",
    ],
    "last_model": "lmstudio-community/gpt-oss-20b-GGUF/gpt-oss-20b-MXFP4.gguf",
    "api_key": "",
    "context_size": 16384,
    "host": "0.0.0.0",
    "port": 8081,
    "gpu_layers": "999"
}
```

| Setting | Description | Default |
| :------- | :------------ | :-------- |
| llama_exe_path | The path where the current llama executable is installed | CMAKE Installation Directory |
| llama_exe_paths | LocalMind Supports multiple llama.cpp installations | Multiple CMAKE installations |
| model_path | The root path to where the models are stored | |
| models | Currently not used. ||
| last_model | The path to the last model used | |
| api_key | Typically not needed for local models |  "" |
| context_size | The context size passed to llama-server | |
