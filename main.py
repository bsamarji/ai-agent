import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

def main():
    # Get api key from env variable
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Check if the user provided a prompt
    if len(sys.argv) < 2:
        print("Error... no prompt was provided as a cli argument.")
        sys.exit(1)
    
    # Get the user prompt and store it in a message we can pass to the api
    user_prompt = sys.argv[1]
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
    # Print the api usage metadata
    usage_metadata = response.usage_metadata
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
    print(f"Response tokens: {usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
