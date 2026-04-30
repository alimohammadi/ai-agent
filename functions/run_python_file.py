import os
import subprocess
from google.genai import types

def run_python_file(working_directory: str, file_path: str, args=None):
    working_dir_abs = os.path.abspath(working_directory)

    abs_file_path = os.path.normpath(
        os.path.join(working_dir_abs, file_path)
    )

    # Security check
    if os.path.commonpath([working_dir_abs, abs_file_path]) != working_dir_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # Check existence
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    # If directory
    if os.path.isdir(abs_file_path):
        return f'Error: Cannot execute "{file_path}" as it is a directory'

    # Check python file
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    try:
        cmd = ["python3", abs_file_path]

        if args:
            cmd.extend(args)

        result = subprocess.run(
            cmd,
            cwd=working_dir_abs,
            timeout=30,
            capture_output=True,
            text=True
        )

        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

        if result.returncode != 0:
            output += f"\nProcess exited with code {result.returncode}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified directory with optional arguments, returning the combined standard output and error",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of string arguments to pass to the Python file",
            )
        },
    ),
)