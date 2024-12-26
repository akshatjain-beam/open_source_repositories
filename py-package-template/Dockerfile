# Use Python 3.7 as the base image
FROM python:3.7-slim

# Set the working directory in the container
WORKDIR /alexioannides-py-package-template

# Copy the project files into the container
COPY . /alexioannides-py-package-template

# Install the project in editable mode
# RUN pip install -e .

# Install pipenv and pytest globally
RUN pip3 install pipenv pytest numpy

# Install all dependencies using pipenv
RUN pipenv install --dev

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