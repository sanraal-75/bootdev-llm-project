import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified python file with arguments supplied as keyword arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Keyword arguments supplied as a list",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path)) # normalise and join paths to get the absolute file path
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir: # the common path of the computed file path and the working directory should be the working directory.
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            # print(file_path.endswith("py"))
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", abs_file_path] #create a subprocess object
        if args != None:
            command.extend(args) #extend with optional arguments

        completed_process = subprocess.run(command,capture_output=True,timeout=30,text=True,cwd=abs_working_dir)
        
        output = []

        if completed_process.returncode != 0:
            output.append(f'Process exited with code {completed_process.returncode}')
        
        if completed_process.stdout == "" and completed_process.stderr == "":
            output.append("No output produced")
        
        if completed_process.stdout != "":
            output.append(f'STDOUT: {completed_process.stdout}')
            
        if completed_process.stderr != "":
            output.append(f'STDERR: {completed_process.stderr}')

        return "\n".join(output)

    except Exception as e:
        return f'Error: executing Python file: {e}'