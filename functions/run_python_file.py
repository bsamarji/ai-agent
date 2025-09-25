import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    joined_path = os.path.join(working_directory, file_path)

    # validate that the directory is inside our working directory,
    # to keep the LLM restricted to the working dir
    abs_working_dir_path = os.path.abspath(working_directory)
    abs_joined_path = os.path.abspath(joined_path)
    abs_common_path = os.path.commonpath([abs_joined_path, abs_working_dir_path])
    if abs_common_path != abs_working_dir_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # validate that the file exists
    if os.path.exists(abs_joined_path) is False:
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(args=["python", abs_joined_path] + args, cwd=abs_working_dir_path, timeout=30, capture_output=True, text=True)
        if completed_process.returncode != 0:
            return f"STDOUT:\n{completed_process.stdout}STDERR:\n{completed_process.stderr}Process exited with code {completed_process.returncode}"
        elif completed_process.stdout is None:
            return "No output produced."
        else:
            return f"STDOUT:\n{completed_process.stdout}STDERR:\n{completed_process.stderr}"
    except Exception as e:
        print(f"Error: executing Python file: {e}")
