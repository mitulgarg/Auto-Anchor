from checkreq import FindImport, FindreqLibraries, changereqfile
from utils import *
import dspy
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from typing import Annotated, Any, Dict, Optional, Sequence, TypedDict, List, Tuple
import platform
import os


def detect_application(requirements_file, directory_structure):
    with open(requirements_file, 'r') as file:
        requirements = file.read()

    python_version = platform.python_version()

    type_of_application = None
    if 'streamlit' in requirements:
        type_of_application = 'Streamlit'
    elif 'langchain' in requirements:
        type_of_application = 'Langchain'
    elif 'Flask' in requirements:
        type_of_application = 'Flask'
    

    entrypoint_filename = 'app.py'  
    for file in directory_structure:
        if file.endswith(('app.py', 'main.py')):
            entrypoint_filename = os.path.basename(file)
            break
    
    class Input(BaseModel):
        dir_struct: List[str] = Field(description="List of all the files in the directory.")

    class Output(BaseModel):
        work_directory: str = Field(description="The working directory of the application.")
        entrypoint_filename: str = Field(description="The filename that is the entrypoint for the application.")

    class FindWorkingDirectory(dspy.Signature):
        f"""I need the working directory for this {type_of_application} application and also the entrypoint filename for running it so that I can create a Dockerfile."""

        input: Input = dspy.InputField()
        output: Output = dspy.OutputField()

    predictor = dspy.TypedPredictor(FindWorkingDirectory)
    input = Input(
        dir_struct=directory_structure,
    )
    mapped_parameters = predictor(input=input)
    print(mapped_parameters.output.work_directory)
    print(mapped_parameters.output.entrypoint_filename)

    final_output = {
        'python_version': python_version,
        'type_of_application': type_of_application,
        'work_directory': mapped_parameters.output.work_directory,
        'entrypoint_filename': mapped_parameters.output.entrypoint_filename
    }

    return final_output


def main():

    class Input(BaseModel):
        python_version: str = Field(description="Python version to be used")
        type_of_application: str = Field(description="Type of python application")
        work_directory: str = Field(description="Working directory of the application")
        entrypoint_filename: str = Field(description="File name for starting the application endpoint")

    class Output(BaseModel):
        dockerfile: str = Field(description="The complete dockerfile code")

    class CreateDockerFile(dspy.Signature):
        """I need a Dockerfile for a basic Streamlit app. The app is written in Python."""

        input: Input = dspy.InputField()
        output: Output = dspy.OutputField()


    list_of_libs = []
    
    for dir in GetFilesInDirectory('src'):
        list_of_libs += FindImport(dir)
    
    for dir in GetFilesInDirectory('src'):
        changereqfile("requirements2.txt", 'requirements.txt', dir)
        print(FindreqLibraries("requirements.txt", dir))

    bedrock = dspy.Bedrock(region_name="us-east-1")

    model_kwargs = {
        "max_tokens": 4000,
        "temperature": 0.4,
    }

    lm = dspy.AWSAnthropic(bedrock, "anthropic.claude-3-5-sonnet-20240620-v1:0", **model_kwargs)
    dspy.configure(lm=lm)

    output = detect_application('requirements2.txt', GetFilesInDirectory("."))

    input = Input(
        python_version=output["python_version"],
        type_of_application=output["type_of_application"],
        work_directory=output["work_directory"],
        entrypoint_filename=output["entrypoint_filename"]
    )

    predictor = dspy.TypedPredictor(CreateDockerFile)
    mapped_parameters = predictor(input=input)
    
    print(mapped_parameters.output.dockerfile)
    with open("Dockerfile", "w") as file:
        file.write(mapped_parameters.output.dockerfile)

if __name__ == "__main__":
    main()
