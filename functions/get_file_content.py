import os

from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    # absolute working directory
    working_dir_abs = os.path.abspath(working_directory)

    # normalized target path
    abs_file_path = os.path.normpath(
        os.path.join(working_dir_abs, file_path)
    )

    # ✅ check if directory
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    # ✅ security check (IMPORTANT)
    valid_target_dir = os.path.commonpath(
        [working_dir_abs, abs_file_path]
    ) == working_dir_abs

    if not valid_target_dir: 
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    file_content_string = ""
    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if len(file_content_string) >= MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string
    
    except Exception as e:
        return f"Exception reading file: {e}"

