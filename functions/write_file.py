import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)

    abs_file_path = os.path.normpath(
        os.path.join(working_dir_abs, file_path)
    )

    if os.path.commonpath([working_dir_abs, abs_file_path]) != working_dir_abs:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # If it is directory
    if os.path.isdir(abs_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        # Create folder 
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        # Write to file
        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: Failed to write to file: {file_path}, {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites an existing file or writes to a new file if it doesn't exist  (and creates required parent dires safely), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the files as a string",
            )
        },
    ),
)