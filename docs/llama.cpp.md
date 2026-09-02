# Install and build llama.cpp

***

Illama.cpp can be built to support various CPU/GPU/XPU hardware platforms. The hardware used to develop LocalMind is an Intel Arc Pro B70 on Windows and an Intel Arc B580 on Fedora Linux. SYCL or Vulkan flavors of llama.cpp work with these GPU's. Local mind provides a way to use both backends for server and benchmarking.

***

A script file is used to update the local GitHib repository then build and install the llama.cpp software into a location that can be used by localmind.
The recommeneded location for these build scripts is <Users Home>\bin and it should be in the path for convenience.

**Linux**
/home/<user id>/bin/ or /home/<user id>/.local/bin

**Windows**
C:\Users\<user id>\bin\

## Requirements:

### Sofware Tools

* [Git](https://git-scm.com/install/windows)
* [CMake](https://cmake.org/download/)
* [Visual Studio (Community)](https://visualstudio.microsoft.com/vs/community/)
* [Intel oneAPI for SYCL build](https://www.intel.com/content/www/us/en/developer/tools/oneapi/oneapi-toolkit-download.html)
* [Vulkan SDK for Vulkan build](https://vulkan.lunarg.com/sdk/home)

### Software Notes

| Tool | Notes |
| :--- | :---- |
| C/C++ Compiler | You can use MSVC/LLVM/GCC/ICX for all CMAKE presets<br>The compiler is selected specifing CMAKE_C_COMPILER and CMAKE_CXX_COMPILER.<br>I recommend using the default compiler for the selected cmake preset. |

* When installing oneAPI be sure to install both "Intel oneAPI Toolkit" and "Intel Deep Learning Essentials".
* I recommend using the default installation settings for all packages.
 

### Hardware

* Any CPU/GPU/XPU supported by llama.cpp

## Example build scripts

There are a number of CMAKE presets available, Localmind was developed using the SYCL and Vulkan release versions.

Available configure presets:

  "x64-linux-gcc-debug"
  "x64-linux-gcc-release"
  "x64-linux-gcc-reldbg"
  "x64-linux-gcc+static-release"
  "arm64-windows-llvm-debug"
  "arm64-windows-llvm-release"
  "arm64-windows-llvm+static-release"
  "arm64-apple-clang-debug"
  "arm64-apple-clang-release"
  "arm64-apple-clang+static-release"
  "x64-windows-llvm-debug"
  "x64-windows-llvm-release"
  "x64-windows-llvm-reldbg"
  "x64-windows-llvm+static-release"
  "x64-windows-msvc-debug"
  "x64-windows-msvc-release"
  "x64-windows-msvc+static-release"
  "x64-windows-sycl-debug"
  "x64-windows-sycl-debug-f16"
  **"x64-windows-sycl-release"**
  "x64-windows-sycl-release-f16"
  "x64-windows-vulkan-debug"
  **"x64-windows-vulkan-release"**

You can use these batch/shell script files you must modify these directory names to match your installation choices.

| Script Variable | Description |
| :-------------- | :---------- |
| REPO_PATH | The path to the cloned llama.cpp repository |
| BUILD_DIR | The build directory within the cloned repository |
| INSTALL_PREFIX | The directory where you want llama.cpp to be installed |
| ONEAPI_VARS | The path to the script that sets the environment for Intel oneAPI |
| CMAKE_PRESET | The CMAKE preset |

The steps required to build llama.cpp in a command prompt after all prerequisite software has been installed.

1. Change the working directory to the location where you want to install the git repository.
2. Clone the repository: `git clone https://github.com/ggml-org/llama.cpp.git`
3. Change the directory to the repository. 
3. Execute the CMAKE commands as shown in the following scripts.
4. Configure localmind to use the newly built llama.cpp: 

You can select multiple llama.cpp installations in the LMSettings tab. Select them one at a time using the "Browse Executable Paths" button. Each time a path is selected the list of compiler executable lists is appended with the newly specified path.

![Select llama.cpp install path(s)](./images/llama-exe1.png)



### Vulkan Build for Windows, using the Microsoft Visual Studio Compiler

- Requires Vulkan SDK and Visual Studio

```BATCH
@echo off
setlocal EnableExtensions

set "REPO_PATH=E:\work\llama.cpp"
set "BUILD_DIR=build-x64-windows-vulkan-release"
set "INSTALL_PREFIX=C:\llama-vulkan-release"
set "CMAKE_PRESET=x64-windows-vulkan-release"
set "SCRIPT_DIR=%~dp0"

echo [INFO] Navigating to "%REPO_PATH%"
cd /D "%REPO_PATH%" || goto :error

if not exist "CMakeLists.txt" (
    echo [ERROR] Could not find llama.cpp source at "%REPO_PATH%"
    goto :error
)

set "VS_VARS=C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"

if exist "%VS_VARS%" (
    echo [INFO] Initializing Visual Studio MSVC environment...
    call "%VS_VARS%" || goto :error
) else (
    echo [ERROR] Could not find "%VS_VARS%"
    goto :error
)

echo [INFO] Pulling latest changes...
git pull --rebase || goto :error

set "PATH=C:\Program Files\Microsoft Visual Studio\18\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja;%PATH%"

echo [INFO] Configuring with "%CMAKE_PRESET%" preset...
cmake --preset "%CMAKE_PRESET%" || goto :error

echo [INFO] Building...
cmake --build "%BUILD_DIR%" --config Release -j || goto :error

echo [INFO] Deleting install directory
set TARGET_DIR="%INSTALL_PREFIX"
if exist %TARGET_DIR% (
    echo Deleting %TARGET_DIR%...
    rd /s /q %TARGET_DIR%
    echo Done.
) else (
    echo Directory does not exist. Skipping.
)

echo [INFO] Creating install directory...
if not exist "%INSTALL_PREFIX%" mkdir "%INSTALL_PREFIX%" || goto :error

echo [INFO] Installing to "%INSTALL_PREFIX%"...
cmake --install "%BUILD_DIR%" --prefix "%INSTALL_PREFIX%" --config Release || goto :error

echo.
echo [SUCCESS] Update complete.
echo Installed files should be in:
echo   %INSTALL_PREFIX%
pause
exit /b 0

:error
echo.
echo [FAILED] Build/update failed.
echo Current directory:
cd
echo.
pause
exit /b 1
```

### SYCL Build for Windows using Intel compilers.

- Requires Intel oneAPI

```BATCH
@echo off
setlocal EnableExtensions

set "REPO_PATH=E:\work\llama.cpp"
set "BUILD_DIR=build-x64-windows-sycl-release"
set "INSTALL_PREFIX=C:\llama-sycl-release"
set "ONEAPI_VARS=C:\Program Files (x86)\Intel\oneAPI\setvars.bat"
set "CMAKE_PRESET=x64-windows-sycl-release"

set "SCRIPT_DIR=%~dp0"

echo [INFO] Navigating to "%REPO_PATH%"
cd /D "%REPO_PATH%" || goto :error

if not exist "CMakeLists.txt" (
    echo [ERROR] Could not find llama.cpp source at "%REPO_PATH%"
    goto :error
)

if exist "%ONEAPI_VARS%" (
    echo [INFO] Initializing oneAPI...
    call "%ONEAPI_VARS%" intel64 || goto :error
) else (
    echo [ERROR] Could not find setvars.bat at "%ONEAPI_VARS%"
    goto :error
)

set "PATH=C:\Program Files\nodejs;%PATH%"

echo [INFO] Checking Intel runtime DLL path...
where svml_dispmd.dll >nul 2>&1 || (
    echo [ERROR] svml_dispmd.dll not found in PATH after setvars.
    goto :error
)

echo [INFO] Pulling latest changes...
git pull --rebase || goto :error

echo [INFO] Configuring with "%CMAKE_PRESET%" preset...
cmake --preset "%CMAKE_PRESET%" ^
	  -DCMAKE_C_COMPILER=icx -DCMAKE_CXX_COMPILER=icx || goto :error

echo [INFO] Building...
cmake --build "%BUILD_DIR%" --config Release -j || goto :error

echo [INFO] Creating install directory...
if not exist "%INSTALL_PREFIX%" mkdir "%INSTALL_PREFIX%" || goto :error

echo [INFO] Installing to "%INSTALL_PREFIX%"...
cmake --install "%BUILD_DIR%" --prefix "%INSTALL_PREFIX%" --config Release || goto :error

echo.
echo [SUCCESS] Update complete.
echo Installed files should be in:
echo   %INSTALL_PREFIX%
pause
exit /b 0

:error
echo.
echo [FAILED] Build/update failed.
echo Current directory:
cd
echo.
pause
exit /b 1

```

Linux SYCL build

When building for Linux I recommend installing oneAPI using the default package manager, apt or dnf. This allows the packages to be updated as your system updates are installed.

For Vulkan on Linux: [Getting Started with the Linux Tarball Vulkan SDK](https://vulkan.lunarg.com/doc/view/latest/linux/getting_started.html)  

The SYCL build script for Linux. 
A preset was not used. Be sure to change the compilers to gcc or llvm if not building for SYCL.


```BASH
#!/usr/bin/env bash
set -euo pipefail

REPO="$HOME/work/llama.cpp"
INSTALL_PREFIX="$HOME/.local"
BUILD_DIR="build-sycl"
LIB_DIR="$INSTALL_PREFIX/lib64"

cd "$REPO"

echo "[1/6] Updating repo..."
git fetch --all --prune
git pull --ff-only

echo "[2/6] Cleaning old build..."
rm -rf "$BUILD_DIR"

echo "[3/6] Loading Intel oneAPI..."
if [[ -f /opt/intel/oneapi/setvars.sh ]]; then
    # Avoid noisy repeat initialization when possible
    if [[ -z "${ONEAPI_ROOT:-}" ]]; then
        set +u
        source /opt/intel/oneapi/setvars.sh
        set -u
    else
        echo "oneAPI already initialized: $ONEAPI_ROOT"
    fi
else
    echo "ERROR: /opt/intel/oneapi/setvars.sh not found"
    exit 1
fi

echo "[4/6] Configuring CMake..."
cmake -B "$BUILD_DIR" \
    -DCMAKE_BUILD_TYPE=Release \
    -DGGML_SYCL=ON \
    -DCMAKE_C_COMPILER=icx \
    -DCMAKE_CXX_COMPILER=icpx \
    -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX"

echo "[5/6] Building..."
cmake --build "$BUILD_DIR" --config Release -j"$(nproc)"

echo "[6/6] Installing..."
cmake --install "$BUILD_DIR"

cd /home/crash/work/llama.cpp
find build* -type f \( \
  -name 'libllama*.so*' -o \
  -name 'libggml*.so*' -o \
  -name 'libmtmd*.so*' \
\) -exec cp -av {} "$LIB_DIR" \;

cd ~
sudo ldconfig "$LIB_DIR"


echo
echo "Installed binaries should be under:"
echo "  $INSTALL_PREFIX/bin"
echo
echo "Version check:"
"$INSTALL_PREFIX/bin/llama-server" --version || true

```











