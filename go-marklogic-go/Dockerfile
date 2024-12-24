# Start from the official Go image
FROM golang:1.20

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy go.mod and go.sum files to the container
COPY go.mod go.sum ./

# Download all dependencies
RUN go mod download

# Copy the source code into the container
COPY . .

# Run tests
# Todo: add the name of the folder to run -> ./<folder-name or folder-path>
RUN go test -v ./test/text

# DO NOT CHANGE ANY BELOW CODE
WORKDIR /
COPY run_tests.sh ./
RUN chmod +x /run_tests.sh
ENTRYPOINT ["/bin/bash", "-s"]
