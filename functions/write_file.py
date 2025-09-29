import os
from google.genai import types


def write_file(working_directory, file_path, content):
    joined_path = os.path.join(working_directory, file_path)

    # validate that the directory is inside our working directory,
    # to keep the LLM restricted to the working dir
    abs_working_dir_path = os.path.abspath(working_directory)
    abs_joined_path = os.path.abspath(joined_path)
    abs_common_path = os.path.commonpath([abs_joined_path, abs_working_dir_path])
    if abs_common_path != abs_working_dir_path:
        return f"Error: Cannot write to '{file_path}'' as it is outside the permitted working directory"

    # overwrite the contents of the file
    # if the file doesn't exist, the write mode will create it
    with open(abs_joined_path, "w") as f:
        f.write(content)
        return f"Successfully wrote to '{file_path}' ({len(content)} characters written)"
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write specified contents to a specified file. The file location is constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to be written to the file."
            ),
        },
    ),
)
