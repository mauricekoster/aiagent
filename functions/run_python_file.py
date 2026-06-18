import os
import subprocess

from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the python script specified by the file_path relative to the working directory. Arguments can be passed to the script as well.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments passed the the python script.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="An argument"
                )
            ),
        },
        required=['file_path'],
        
    ),
    
)


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # print(target_file)
    if not os.path.exists(target_file) or not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_file]
    if args:
        command.extend(args)

    completed_process = subprocess.run(command, cwd=working_dir_abs, check=True, text=True, capture_output=True, timeout=30)

    result = ""
    if completed_process.returncode != 0:
        result += f"Process exited with code {completed_process.returncode}"

    if not completed_process.stdout and not completed_process.stderr:
        result += "No output produced"

    if completed_process.stdout:
        result += "STDOUT:" + completed_process.stdout
    if completed_process.stderr:
        result += "STDERR:" + completed_process.stderr

    return result
