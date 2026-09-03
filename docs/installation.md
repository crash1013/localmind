# LocalMind Installation

## Installation

Clone the LocalMind repository:

```bash
git clone https://github.com/crash1013/localmind.git
cd localmind
```

### Create the virtual environment

Create a python virtual emvironment for localmind:

Linux:

``` Bash

python3 -m venv .venv
source .venv/bin/activate

``` 

PowerShell:

``` PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install LocalMind and its dependencies

``` Bash
pip install -e .

```

There may be missing components in some Linux Distributions.

For example if tkinter cannot be imported:

If you need to update your python modules you should delete the environment `rm -rf .venv` and [rebuild it](#Create the virtual environment)

Debian/Ubuntu 

``` Bash
sudo apt update
sudo apt install python3-tk
```

For Fedora

``` Bash
sudo dnf install python3-tkinter
```

## Start LocalMind

Before launching LocalMind, initialize the compiler/runtime environment that matches the llama.cpp backend you intend to use.

### SYCL / Intel oneAPI

On Linux:

```bash
source /opt/intel/oneapi/setvars.sh
python src/localmind/gui/workbench.py

```

On Windows:

``` bat
call "C:\Program Files (x86)\Intel\oneAPI\setvars.sh
python src\gui\workbench.py
```

### Vulkan

On Windows

``` bat
call "C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"

python src\localmind\gui\workbench.py

```

On Linux

``` bash
source "$HOME/vulkan/<version>/setup-env.sh"
python src/localmind/gui/workbench.py

```

This is the localmind.bat located in the localmind project root.

It prepares the Windows runtime environment required by LocalMind and then launches the application.

Intel oneAPI's `setvars.bat` initializes both the Intel oneAPI environment and the required Microsoft Visual C++ environment. Because of this, a separate call to the Visual Studio `vcvars64.bat` script is not required when using this launcher.

The launcher supports LocalMind configurations that use both SYCL and Vulkan llama.cpp builds.

``` bat
@echo off
setlocal

SET "LOCALMIND_PATH=E:\work\localmind"
SET "VIRTUAL_ENVIRONMENT=.venv\Scripts\activate.bat"

REM Activate Intel oneAPI only if it has not already been activated
REM This sets the MSVC environment as well as the oneAPI environment.

if not defined SETVARS_COMPLETED (
    call "C:\Program Files (x86)\Intel\oneAPI\setvars.bat"
)

REM Switch to E: drive and LocalMind project folder

cd /d "%LOCALMIND_PATH%"

REM Activate Python virtual environment
call "%VIRTUAL_ENVIRONMENT%"

REM Launch LocalMind
python "src\localmind\gui\workbench.py"

endlocal
```

For FedoraLinux using the SYCL backend on Intel GPU's

If 

``` bash
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# source /opt/intel/oneapi/setvars.sh
ONEAPI_VARS="/opt/intel/oneapi/setvars.sh"

if [[ ! -f "${ONEAPI_VARS}" ]]; then
    echo "[ERROR] Intel oneAPI environment script not found:"
    echo "        ${ONEAPI_VARS}"
    exit 1
fi

if [[ -z "${ONEAPI_ROOT:-}" ]]; then
    echo "[INFO] Loading Intel oneAPI environment..."
    set +u
    # shellcheck disable=SC1091
    source "${ONEAPI_VARS}"
    set -u
else
    echo "[INFO] Intel oneAPI environment already loaded: ${ONEAPI_ROOT}"
fi

export LD_LIBRARY_PATH="$HOME/.local/lib64:${LD_LIBRARY_PATH:-}"
export ONEAPI_DEVICE_SELECTOR=level_zero:gpu

exec .venv/bin/python src/localmind/gui/workbench.py

```

