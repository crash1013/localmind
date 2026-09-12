# Building llama.cpp for LocalMind

LocalMind can use llama.cpp builds with CPU, SYCL, or Vulkan backends.

The systems used during LocalMind development include:

| Platform | GPU | Backends |
| :--- | :--- | :--- |
| Windows | Intel Arc Pro B70 | SYCL, Vulkan |
| Fedora Linux | Intel Arc B580 | SYCL, Vulkan |

The examples in this document show how to clone, build, install, and configure llama.cpp for use with LocalMind. The supplied scripts are examples: paths, compiler versions, package names, and Linux prerequisites will need to be adapted for your system.

## Recommended locations

Keep the build scripts in a directory on your `PATH` so they are easy to run.

**Linux**

```text
/home/<user>/.local/bin
```

or:

```text
/home/<user>/bin
```

**Windows**

```text
C:\Users\<user>\bin
```

---

## Common requirements

### Software

- [llama.cpp](https://github.com/ggml-org/llama.cpp)
- [Git](https://git-scm.com/)
- [CMake](https://cmake.org/download/)
- [Visual Studio Community](https://visualstudio.microsoft.com/vs/community/) for the Windows MSVC build
- [Intel oneAPI Toolkit](https://www.intel.com/content/www/us/en/developer/tools/oneapi/oneapi-toolkit-download.html) for SYCL builds
- [Vulkan SDK](https://vulkan.lunarg.com/sdk/home) for Vulkan builds

When installing oneAPI, use the default installation settings unless you have a specific reason to change them. LocalMind development systems also include Intel Deep Learning Essentials.

### Hardware

Any CPU, GPU, or XPU supported by llama.cpp can be used. The examples here focus on Intel Arc GPUs.

---

## Clone llama.cpp

Choose a working directory and clone the repository.

### Windows

```cmd
set WORKDIR=E:\work
cd /d %WORKDIR%
git clone https://github.com/ggml-org/llama.cpp.git
```

### Linux

```bash
mkdir -p ~/work
cd ~/work
git clone https://github.com/ggml-org/llama.cpp.git
```

---

# Windows builds

The Windows examples use llama.cpp CMake presets.

To see the presets available in your current checkout:

```cmd
cmake --list-presets
```

The LocalMind development builds on Windows use:

- `x64-windows-vulkan-release`
- `x64-windows-sycl-release`

The scripts below update the local llama.cpp checkout, configure the requested backend, build it, and install the result into a stable location that LocalMind can reference.

## Common script variables

| Variable | Description |
| :--- | :--- |
| `REPO_PATH` | Path to the cloned llama.cpp repository |
| `BUILD_DIR` | Build directory within the repository |
| `INSTALL_PREFIX` | Destination for the installed llama.cpp build |
| `ONEAPI_VARS` | Intel oneAPI environment setup script |
| `CMAKE_PRESET` | CMake preset used for the build |

---

## Windows Vulkan build

**Requires:**

- Visual Studio
- Vulkan SDK
- CMake

Example build script:

```batch
@echo off
setlocal EnableExtensions

set "REPO_PATH=E:\work\llama.cpp"
set "BUILD_DIR=build-x64-windows-vulkan-release"
set "INSTALL_PREFIX=C:\llama-vulkan-release"
set "CMAKE_PRESET=x64-windows-vulkan-release"

set "VS_VARS=C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"


echo [INFO] Navigating to "%REPO_PATH%"
cd /D "%REPO_PATH%" || goto :error

if not exist "CMakeLists.txt" (
    echo [ERROR] Could not find llama.cpp source at "%REPO_PATH%"
    goto :error
)

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

echo [INFO] Deleting install directory...
if exist "%INSTALL_PREFIX%" (
    rd /s /q "%INSTALL_PREFIX%"
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

---

## Windows SYCL build

**Requires:**

- Intel oneAPI
- CMake

Example build script:

```batch
@echo off
setlocal EnableExtensions

set "REPO_PATH=E:\work\llama.cpp"
set "BUILD_DIR=build-x64-windows-sycl-release"
set "INSTALL_PREFIX=C:\llama-sycl-release"
set "ONEAPI_VARS=C:\Program Files (x86)\Intel\oneAPI\setvars.bat"
set "CMAKE_PRESET=x64-windows-sycl-release"


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
    -DCMAKE_C_COMPILER=icx ^
    -DCMAKE_CXX_COMPILER=icx || goto :error

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

---

# Linux builds

## Linux Vulkan Build

Linux builds require more attention to distribution-specific prerequisites than Windows builds. Ubuntu and Fedora are the primary Linux families used during LocalMind development and testing.

Install compiler and SDK packages using the distribution package manager where practical. This makes future updates easier to manage through normal system updates.


On systems with an Intel GPU, `sycl-ls` should list a GPU device through Level Zero and/or OpenCL.

### Linux Vulkan prerequisites

For the Vulkan SDK tarball installation, follow LunarG's current instructions:

[Getting Started with the Linux Tarball Vulkan SDK](https://vulkan.lunarg.com/doc/view/latest/linux/getting_started.html)

**Example Vulkan Build Script**

```
#!/usr/bin/env bash
set -euo pipefail

REPO="$HOME/work/llama.cpp"
INSTALL_PREFIX="$HOME/llama-vulkan-release"
BUILD_DIR="build"
VULKAN_DIR="$HOME/vulkan/1.4.357.1"

cd "$REPO"

echo "[1/6] Updating repo..."
git fetch --all --prune
git pull --ff-only

echo "[2/6] Cleaning old build..."
rm -rf "$BUILD_DIR"

echo "[3/6] Setting Vulkan Environment"

if [[ -f $VULKAN_DIR/setup-env.sh ]]; then
    # Avoid noisy repeat initialization when possible
    if [[ -z "${VULKAN_SDK:-}" ]]; then
        set +u
        source "$VULKAN_DIR/setup-env.sh"
        set -u
        if [[ -z "${VULKAN_SDK:-}" ]]; then
            echo "ERROR: Vulkan SDK environment initialization failed"
            exit 1
        fi
    fi
    echo "VULKAN environment: $VULKAN_SDK"
else
    echo "ERROR: $VULKAN_DIR/setup-env.sh not found"
    exit 1
fi

echo "[4/6] Configuring CMake..."

cmake -B "$BUILD_DIR" -DGGML_VULKAN=ON -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX"

echo "[5/6] Building..."

cmake --build "$BUILD_DIR" --config Release -j"$(nproc)"

echo "[6/6] Installing..."
cmake --install "$BUILD_DIR"

echo
echo "Installed binaries should be under:"
echo "  $INSTALL_PREFIX/bin"
echo
echo "Version check:"
LD_LIBRARY_PATH="$INSTALL_PREFIX/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
"$INSTALL_PREFIX/bin/llama-server" --version || true

```

---

## Linux SYCL build

### Linux SYCL prerequisites

For SYCL builds, install Intel oneAPI using the package manager for your distribution.

After installation, the oneAPI setup script is normally located at:

```text
/opt/intel/oneapi/setvars.sh
```

You can verify the installation with:

```bash
source /opt/intel/oneapi/setvars.sh
icx --version
icpx --version
sycl-ls
```


The Linux SYCL example does not use a CMake preset. It explicitly selects Intel's compilers and enables `GGML_SYCL`.

The install library directory differs between common Linux families:

- Debian/Ubuntu: `$INSTALL_PREFIX/lib`
- Fedora/RHEL: `$INSTALL_PREFIX/lib64`

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO="$HOME/work/llama.cpp"
INSTALL_PREFIX="$HOME/llama-sycl-release"
BUILD_DIR="build-sycl"

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

cd ~

echo
echo "Installed binaries should be under:"
echo "  $INSTALL_PREFIX/bin"
echo
echo "Version check:"

LD_LIBRARY_PATH="$INSTALL_PREFIX/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
"$INSTALL_PREFIX/bin/llama-server" --version || true

```

---

# Verify the installation

After installing a build, confirm that the expected executable is found and reports the intended compiler/backend build.

### Windows

```cmd
C:\llama-vulkan-release\bin\llama-server --version
C:\llama-sycl-release\bin\llama-server --version
```

### Linux

If `$INSTALL_PATH/bin` is not already on your `PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
sudo ldconfig "$INSTALL_PREFIX/lib64"
```

Then:

```bash
llama-server --version
```

For a SYCL build, `llama-bench` with GPU offload provides a practical verification that the GPU backend is actually being used.

---

# Configure LocalMind

After building llama.cpp, configure LocalMind to use the installed executable directories.

Open the **LMSettings** tab and use **Browse Executable Paths** to add one or more llama.cpp installations. Each selected path is appended to the list of available compiler executable locations.

Typical Windows locations are:

```text
C:\llama-vulkan-release\bin
C:\llama-sycl-release\bin
```

A typical Linux location is:

```text
~/llama_vulkan/release/bin
```

![Select llama.cpp install path(s)](./images/llama-exe1.png)

---

# Build workflow summary

Once the prerequisite toolchains are installed, the recurring workflow is straightforward:

1. Update the local llama.cpp repository.
2. Remove or refresh the backend-specific build directory.
3. Initialize the required compiler/SDK environment.
4. Configure CMake for the desired backend.
5. Build llama.cpp.
6. Install the result into a stable location.
7. Verify `llama-server --version` and, when appropriate, run `llama-bench`.
8. Add the installed executable path to LocalMind.

**It is not possible to have a loader configuration for multiple backends because the target libraries share the same name.**

The supplied scripts automate these steps and can be adapted as toolchain versions, hardware, and llama.cpp itself evolve.
