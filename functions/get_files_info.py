import os

def get_files_info(working_directory, directory="."): # calculator
    
    try:
        absolute_path = os.path.abspath(working_directory) # ~/bootdev-llm-project/calculator
        target_path = os.path.normpath(os.path.join(absolute_path, directory))
        valid_target_dir = os.path.commonpath([absolute_path, target_path]) == absolute_path

        if not valid_target_dir:
            return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

        if not os.path.isdir(target_path):
            return(f'Error: "{directory}" is not a directory')

        directory_files = os.listdir(target_path)

        output = ""
        for entry in directory_files:
            output += (f"{entry}: file_size={os.path.getsize("/".join([target_path,entry]))}, is_dir={os.path.isdir("/".join([target_path,entry]))}\n")

        return output

    except Exception as e:
        return(f"Error: {e}")