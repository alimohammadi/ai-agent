import os

def get_files_info(working_directory, directory="."):
    try:
        # absolute working directory
        working_dir_abs = os.path.abspath(working_directory)

        # normalized target path
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        # ✅ security check (IMPORTANT)
        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_dir]
        ) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # ✅ check if directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # ✅ build response
        final_response = ""
        contents = os.listdir(target_dir)

        for content in contents:
            content_path = os.path.join(target_dir, content)

            is_dir = os.path.isdir(content_path)
            size = os.path.getsize(content_path)

            final_response += f"- {content}: file_size={size} bytes, is_dir={is_dir}\n"

        return final_response

    except Exception as e:
        return f"Error: {str(e)}"