import os

from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the content to a file specified by the file_path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # print(target_file)
    if os.path.exists(target_file) and not os.path.isfile(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    with open(target_file, 'w') as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'