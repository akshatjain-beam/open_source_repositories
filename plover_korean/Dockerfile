# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /plover_korean

# Copy the project files into the container
COPY . /plover_korean

# Install pytest globally
RUN pip install pytest

# Install all dependencies using pip
RUN pip install .

# Run tests using pytest
RUN python -m pytest test/

# Set the working directory to the root
WORKDIR /

# Copy the run_tests.sh script into the root of the container
COPY run_tests.sh ./

# Make the run_tests.sh script executable
RUN chmod +x /run_tests.sh

# Set the entry point for the container to Bash
# This allows you to run additional commands/scripts within the container
ENTRYPOINT ["/bin/bash", "-s"]
