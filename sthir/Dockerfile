# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /sthir

# Copy the project files into the container
COPY . /sthir

# Install dependencies for the project
RUN pip install .
RUN pip install -r requirements.txt

# Install pytest if not included in requirements.txt
RUN pip install pytest

# Run tests using pytest
RUN python -m pytest sthir/tests/

# Set the working directory to the root
WORKDIR /

# Copy the run_tests.sh script into the root of the container
COPY run_tests.sh ./

# Make the run_tests.sh script executable
RUN chmod +x /run_tests.sh

# Set the entry point for the container to Bash
# This allows you to run additional commands/scripts within the container
ENTRYPOINT ["/bin/bash", "-s"]
