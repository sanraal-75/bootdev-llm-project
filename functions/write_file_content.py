import os

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path)) # normalise and join paths to get the absolute file path
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir: # the common path of the computed file path and the working directory should be the working directory.
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(abs_file_path),exist_ok=True) # create any missing directories from file_path

        with open(abs_file_path,"w") as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error writing file "{file_path}": {e}'