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