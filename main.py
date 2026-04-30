import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
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
        function_declarations=[schema_get_files_info],
    )

    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
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

    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:     
        print(response.text)

main()


# print(get_files_info("calculator", "pkg"))