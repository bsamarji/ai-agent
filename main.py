import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from functions.get_files_info import schema_get_files_info


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
            schema_get_files_info
        ]
    )

    # Send the user prompts to the ai through the api and store the api response
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

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
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
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
