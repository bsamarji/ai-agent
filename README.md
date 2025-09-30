# AI Agent

## Description

I've created a basic ai agent that can help with writing or debugging code. The agent is powered by the google `gemini-2.0-flash-001` model. It has access to the following tools:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

## Setup

I used the uv package manager for project management, so you need to have the uv package manager installed and you can use the `uv sync` command to install the packages specified in the uv.lock file.

The agent is confined to the current working directory. This is currently hard coded to the ./calculator dir in the ./functions/call_function.py script. Be careful modifying the current working directory path, otherwise you could give the agent access to your entire file system!

### API Key

You need to create a .env file in the root of the project and get an API key from the [google AI studio](https://aistudio.google.com/).

Save your API key in the .env file as:

```
GEMINI_API_KEY="your_api_key_here"
```

## Usage

Once you're setup then you can ask the agent any question, but it is bound to the system prompt and the current working directory. Run a sample command like the one below:

```
uv run main.py "Run my calculator app to calculate 3 * 8 + 9"
```

Remember it is a basic agent and the google LLMs are not guaranteed to be 100% accurate so you may have to play around with your prompts or tweak the `system_prompt` in main.py to get better outcomes.
