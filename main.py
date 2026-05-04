import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

from functions.call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # system_prompt = """
    #     You are a helpful AI coding agent.

    #     When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    #     - List files and directories
    #     - Read file contents
    #     - Execute Python files with optional arguments
    #     - Write or overwrite files

    #     All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    # """

    system_prompt = """
        You are a helpful AI coding agent.

        When answering questions about code:
        1. ALWAYS explore the project first using get_files_info
        2. THEN read relevant files using get_file_content
        3. ONLY use run_python_file if the user explicitly asks to execute code

        Never guess file names.
        Never execute code unless necessary.

        All paths must be relative to the working directory.
    """

    client = genai.Client(api_key=api_key)
    # for m in client.models.list():
    #     print(m.name)

    if (len(sys.argv) < 2):
        print("I need prompt")
        sys.exit(2)

    verbose_flag = False
    if (len(sys.argv) == 3 and sys.argv[2] == "--verbose"):
        verbose_flag = True

    
    prompt = sys.argv[1]
    
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info, 
            schema_get_file_content, 
            schema_run_python_file, 
            schema_write_file
        ],
    )

    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )


    max_iterations = 20

    for _ in range(max_iterations):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=config
        )

        if response is None or response.usage_metadata is None:
            print("Response is malformed")
            return
        
        if verbose_flag:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # Add model's response candidates to conversation history
        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    print("Candidate is malformed")
                    continue
                messages.append(candidate.content)

        # Check if model requested function calls
        if response.function_calls:
            for function_call in response.function_calls:
                print(f" - Calling function: {function_call.name}")
                result = call_function(function_call, verbose=verbose_flag)
                # Append each function result to messages
                messages.append(result)
        else:
            # Model has a final response (no function calls requested)
            print("Final response:")
            print(response.text)
            return
    
    # If we've exhausted all iterations without a final response
    print("Error: Maximum iterations reached. The agent did not produce a final response.")
    sys.exit(1)

main()


# print(get_files_info("calculator", "pkg"))