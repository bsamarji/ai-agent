import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

def main():
    # Get api key from env variable
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Compose cli argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="User prompt for the ai agent")
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()
    
    # Get the user prompt and store it in a message we can pass to the api
    user_prompt = args.prompt
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Send the user prompts to the ai through the api and store the api response
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages
    )
    
    # Print the ai's response
    print(response.text)

    if args.verbose:
        # Print the api usage metadata
        print(f"User prompt: {args.prompt}")
        usage_metadata = response.usage_metadata
        print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
        print(f"Response tokens: {usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
