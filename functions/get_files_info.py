import os

from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        # 1. Get absolute path of the working directory 
        abs_working_dir = os.path.abspath(working_directory)

        # 2. Construct and normalize the full path to the target directory 
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))

        # 3. Validate that the target_dir is inside the working_dir_abs
        #    Does target directory fall within the absolute working director path
        #    Will be True or False
        valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # 4. Check if the target is actually a directory 
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        # 5. Iterate over the items in the target directory. For each of them 
        #    record the name, file size, and whether it's a directory itself.
        #    Use this data to build and return a string representing the contents
        #    of the target directory.
        files_info = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename) 
            is_dir = os.path.isdir(filepath)

            try:
                file_size = os.path.getsize(filepath)
            except OSError:
                file_size = 0

            files_info.append(f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}")

        if not files_info:
            return "Directory is empty"
        
        return "\n".join(files_info)
    
    except  Exception as e:
        return f"Error listing files {e}"


    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)