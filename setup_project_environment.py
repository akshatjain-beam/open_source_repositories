import os
import shutil

def initialize_project_files(nested_folder_name, language_choice):
    # Define the nested folder path
    nested_folder_path = os.path.join(os.getcwd(), nested_folder_name)

    # Create the nested folder if it doesn't exist
    os.makedirs(nested_folder_path, exist_ok=True)

    # Define the paths for the new files to be created
    run_tests_sh_path = os.path.join(nested_folder_path, 'run_tests.sh')
    gitignore_path = os.path.join(nested_folder_path, '.gitignore')
    dockerignore_path = os.path.join(nested_folder_path, '.dockerignore')
    dockerfile_path = os.path.join(nested_folder_path, 'Dockerfile')

    # Check if the base .gitignore and .dockerignore exist, and copy or create them in the nested folder
    base_gitignore_path = os.path.join(os.getcwd(), '.gitignore')
    base_dockerignore_path = os.path.join(os.getcwd(), '.dockerignore')

    # Function to append content to or create a file
    def append_or_create_file(base_path, target_path):
        if os.path.exists(base_path):
            with open(base_path, 'r') as base_file:
                base_content = base_file.read()
            with open(target_path, 'a') as target_file:
                target_file.write("\n" + base_content)
        else:
            open(target_path, 'w').close()

    append_or_create_file(base_gitignore_path, gitignore_path)
    append_or_create_file(base_dockerignore_path, dockerignore_path)

    # Content for run_tests.sh (common for both languages)
    run_tests_sh_content = f"""\
#!/bin/bash

set -euo pipefail

cd /{nested_folder_name}
# Todo: Add the test command to run the tests. Copy the run test command from Dockerfile
"""

    # Content for Dockerfile based on the selected language
    if language_choice.lower() == 'python':
        dockerfile_content = f"""\
# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /{nested_folder_name}

# Copy the project files into the container
COPY . /{nested_folder_name}

# Install Poetry and pytest globally
RUN pip install poetry pytest

# Install all dependencies using Poetry
RUN poetry install 

# Run tests using pytest
RUN python -m pytest 

# Set the working directory to the root
WORKDIR /

# Copy the run_tests.sh script into the root of the container
COPY run_tests.sh ./

# Make the run_tests.sh script executable
RUN chmod +x /run_tests.sh

# Set the entry point for the container to Bash
ENTRYPOINT ["/bin/bash", "-s"]
"""
    elif language_choice.lower() == 'go':
        dockerfile_content = f"""\
# Start from the official Go image
FROM golang:1.20

# Set the Current Working Directory inside the container
WORKDIR /{nested_folder_name}

# Copy go.mod and go.sum files to the container
COPY go.mod go.sum ./

# Download all dependencies
RUN go mod download

# Copy the source code into the container
COPY . .

# Run tests
# Todo: add the name of the folder to run -> ./<folder-name or folder-path>
RUN go test

# Set the working directory to the root
WORKDIR /

# DO NOT CHANGE ANY BELOW CODE
WORKDIR /
COPY run_tests.sh ./
RUN chmod +x /run_tests.sh
ENTRYPOINT ["/bin/bash", "-s"]
"""
    else:
        print("Invalid language choice. Please choose either 'python' or 'go'.")
        return

    # Create run_tests.sh
    with open(run_tests_sh_path, 'w') as file:
        file.write(run_tests_sh_content)
    os.chmod(run_tests_sh_path, 0o755)

    # Create Dockerfile
    with open(dockerfile_path, 'w') as file:
        file.write(dockerfile_content)

    print(f"Created additional project files in: {nested_folder_path}")

# Example usage
nested_folder_name = input("Enter the name of the nested folder: ")
language_choice = input("Choose the language (python/go): ")
initialize_project_files(nested_folder_name, language_choice)
