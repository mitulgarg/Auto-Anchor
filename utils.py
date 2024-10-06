import os
import dspy
import platform
from pydantic import BaseModel, Field
from typing import Annotated, Any, Dict, Optional, Sequence, TypedDict, List, Tuple

def GetFilesInDirectory(directory):
    paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            paths.append(file_path)
    # print(paths)
    return paths



def DetectApplication(requirements_file, directory_structure):
    # Read the requirements.txt file
    with open(requirements_file, 'r') as file:
        requirements = file.read()

    # Get the Python version
    python_version = platform.python_version()

    # Determine the type of application based on dependencies
    type_of_application = None
    if 'streamlit' in requirements:
        type_of_application = 'Streamlit'
    elif 'langchain' in requirements:
        type_of_application = 'Langchain'
    
    # Look for a common entry point file (app.py or main.py) in the directory structure
    entrypoint_filename = 'app.py'  # Default guess
    for file in directory_structure:
        if file.endswith(('app.py', 'main.py')):
            entrypoint_filename = os.path.basename(file)
            break
    
    # # Set the working directory
    # work_directory = 'src'  # Default work directory
    # for file in directory_structure:
    #     if 'src/' in file:
    #         work_directory = 'src'
    #         break

    class Input(BaseModel):
        dir_struct: List[str] = Field(description="List of all the files in the directory.")
       

    class Output(BaseModel):
        work_directory: str = Field(description="The working directory of the application")


    class FindWorkingDirectory(dspy.Signature):
        f"""I need the working directory for this {type_of_application} application so that I can create a Dockerfile."""

        input: Input = dspy.InputField()
        output: Output = dspy.OutputField()

    predictor = dspy.TypedPredictor(FindWorkingDirectory)
    input = Input(
        dir_struct = directory_structure,
    )
    mapped_parameters = predictor(input=input)
    print(mapped_parameters.output.work_directory)
    


    # Output the final format
    return f'''Input(
    python_version = "{python_version}",
    type_of_application = '{type_of_application}',
    work_directory = '{mapped_parameters.output.work_directory}',
    entrypoint_filename = '{entrypoint_filename}'
    )'''

# output = DetectApplication('requirements2.txt', GetFilesInDirectory("."))

# print(output)
