@echo off
setlocal

SET "BACKEND_PATH=C:\llama-vulkan-release\bin"
SET "LOCALMIND_PATH=E:\work\localmind"
SET "VIRTUAL_ENVIRONMENT=.venv\Scripts\activate.bat"

PATH=%PATH%;%BACKEND_PATH%
REM Activate Intel oneAPI only if it has not already been activated
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