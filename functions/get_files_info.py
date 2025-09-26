import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    joined_path = os.path.join(working_directory, directory)

    # validate that the directory is inside our working directory,
    # to keep the LLM restricted to the working dir
    abs_working_dir_path = os.path.abspath(working_directory)
    abs_joined_path = os.path.abspath(joined_path)
    abs_common_path = os.path.commonpath([abs_joined_path, abs_working_dir_path])
    if abs_common_path != abs_working_dir_path:
        return f"Error: Cannot list '{directory}'' as it is outside the permitted working directory"

    if os.path.isdir(abs_joined_path) is False:
        return f"Error: '{directory}'  is not a directory"

    # get metadata for all the items in the directory (name, size, is_dir)
    dir_item_names = os.listdir(abs_joined_path)
    dir_item_paths = [os.path.join(abs_joined_path, item) for item in dir_item_names]
    dir_item_sizes = [os.path.getsize(item) for item in dir_item_paths]
    dir_is_dir = [os.path.isdir(item) for item in dir_item_paths]
    contents_dict = {}

    for i in range(0, len(dir_item_names)):
        contents_dict[dir_item_names[i]] = {
            "size": dir_item_sizes[i],
            "is_dir": dir_is_dir[i],
        }

    # format the metadata into a string and store it in a list
    contents_list = []
    for name in contents_dict:
        contents_list.append(
            f"- {name}: file_size={contents_dict[name]['size']} bytes, is_dir={contents_dict[name]['is_dir']}"
        )

    # add all the metadata strings into one string
    dir_contents = "\n".join(contents_list)
    return dir_contents


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
