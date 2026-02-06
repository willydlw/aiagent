import os

from google.genai import types


def write_file(working_directory, file_path, content):
    """
    Writes content to a file within a restricted directory.
    Creates necessary directories if they don't exist.
    """
    try:
        # Normalize and find absolute paths to prevent directory traversal attacks
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        # Check if the file_path is outside the working_directory
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Check if the file_path is outside the working_directory
        #if not abs_file_path.startswith(abs_working_dir):
        #    return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Check if the target_path points to an existing directory
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # Ensure that all parent directories of the file_path exist
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        
        # Open the file in write mode ("w") and overwrite its contents
        with open(abs_file_path, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error writing to file {e}'



schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text content to a specified file within the working directory (overwriting if the file exists)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)