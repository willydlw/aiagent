import os 
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    """
    Safely reads content from a file within the working directory, with a character limit.
    """
    try:
        # 1. Construct and normalize the full paths
        full_working_dir = os.path.abspath(working_directory)
        full_file_path = os.path.abspath(os.path.join(full_working_dir, file_path))

        # 2. Validate path is within the working directory
        if not full_file_path.startswith(full_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # 3. Validate path points to a regular file
        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # 4. Read the file with truncation logic
        with open(full_file_path, 'r', encoding='utf-8') as f:
            content = f.read(MAX_CHARS)

            # Check if file was larger than the limit
            if f.read(1):
                content += f'[...File "{full_file_path}" truncated at {MAX_CHARS} characters]'
            
            return content

    except FileNotFoundError:
        return f'Error: File not found: "{file_path}"'
    except IsADirectoryError:
        return f'Error: Path is a directory: "{file_path}"'
    except Exception as e:
        # Catch any other potential errors (permission, encoding, etc.)
        return f'Error: An unexpected error occurred: {e}'