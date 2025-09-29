import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from functions.get_files_info import schema_get_files_info
from functions.get_file_contents import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


def main():
    # Get api key from env variable
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Compose cli argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="User prompt for the ai agent")
    parser.add_argument(
        "--verbose", help="increase output verbosity", action="store_true"
    )
    args = parser.parse_args()

    # Get the user prompt and store it in a message we can pass to the api
    user_prompt = args.prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    # Declare the available functions to the LLM
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    # Send the user prompts to the ai through the api and store the api response
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
        )
    )

    # Print the ai's response
    function_call_part = response.function_calls[0]
    if len(response.function_calls) > 0:
        function_result = call_function(function_call_part=function_call_part)
        if not function_result.parts[0].function_response.response:
            raise Exception(f"FATAL ERROR: the function '{function_call_part.name}' did not return a response.")
        elif args.verbose:
            print(f"-> {function_result.parts[0].function_response.response}")
    else:
        print(response.text)

    if args.verbose:
        # Print the api usage metadata
        print(f"User prompt: {args.prompt}")
        usage_metadata = response.usage_metadata
        print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
        print(f"Response tokens: {usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
