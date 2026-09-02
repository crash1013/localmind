
# get_interpreter_path.py

"""
    From within a virtual environment get the path to the interpreter. Regardless of Windows or Linux
"""
import sys
import os

def get_interpreter_path():
    """
    Determines the path to the Python interpreter within a virtual environment,
    handling differences between Windows and Linux.
    """
    venv_path = os.environ.get('VIRTUAL_ENV')
    if not venv_path:
        print("Warning: No virtual environment detected.")
        return sys.executable  # Fallback to the current interpreter

    if sys.platform.startswith('win'):
        interpreter_path = os.path.join(venv_path, 'Scripts', 'python.exe')
    else:  # Assume Linux or other Unix-like
        interpreter_path = os.path.join(venv_path, 'bin', 'python')

    return interpreter_path

if __name__ == "__main__":
    interpreter = get_interpreter_path()
    print(f"The Python interpreter path in this environment is: {interpreter}")