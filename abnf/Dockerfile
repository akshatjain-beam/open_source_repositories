# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /abnf

# Copy the project files into the container
COPY . /abnf

# Install  pytest globally
RUN pip install pytest

# Install all dependencies using Poetry
RUN pip install requirements.txt 

# Run tests using pytest
RUN python -m pytest tests/

# Set the working directory to the root
WORKDIR /

# Copy the run_tests.sh script into the root of the container
COPY run_tests.sh ./

# Make the run_tests.sh script executable
RUN chmod +x /run_tests.sh

# Set the entry point for the container to Bash
# This allows you to run additional commands/scripts within the container
ENTRYPOINT ["/bin/bash", "-s"]
