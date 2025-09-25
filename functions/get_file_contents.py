import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    joined_path = os.path.join(working_directory, file_path)

    # validate that the directory is inside our working directory,
    # to keep the LLM restricted to the working dir
    abs_working_dir_path = os.path.abspath(working_directory)
    abs_joined_path = os.path.abspath(joined_path)
    abs_common_path = os.path.commonpath([abs_joined_path, abs_working_dir_path])
    if abs_common_path != abs_working_dir_path:
        return f"Error: Cannot read '{file_path}'' as it is outside the permitted working directory"

    # validate that the file is actually a file
    if os.path.isfile(abs_joined_path) is False:
        return f"Error: File not found or is not a regular file: '{file_path}'"

    with open(abs_joined_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        file_content_string = file_content_string + f"[...File '{file_path}' truncated at 10000 characters]"
        return file_content_string