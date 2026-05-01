from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types

# directory = function_call.args.get("directory", ".")
directory = "./calculator"

def call_function(function_call, verbose=False):
    function_name = function_call.name or ""
    if function_name == "":
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ],
        )
    
    if verbose:
        print(f"Calling function: {function_name}({function_call.args})")
    else:
        print(f" - Calling function: {function_name}")
        
    result = ""
    args = dict(function_call.args) if function_call.args else {}

    if function_name == "get_files_info":
        result = get_files_info(directory, **args)
    elif function_name == "get_file_content":
        result = get_file_content(directory, **args)
    elif function_name == "run_python_file":
        result = run_python_file(directory, **args)
    elif function_name == "write_file":
        result = write_file(directory, **args)
        
    if result == "":
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"},
                )
            ],
        )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call.name,
                response={"result": result},
            )
        ],
    )
         