# Start from the official Go image
FROM golang:1.20

# Set environment variables for Go cache and XDG base directories
ENV GOCACHE=/tmp/go-cache
ENV GOPATH=/go
ENV GO111MODULE=on
ENV XDG_CACHE_HOME=/tmp/cache

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy go.mod and go.sum files to the container
COPY go.mod go.sum ./

# Download all dependencies
RUN go mod download

# Copy the source code into the container
COPY . .

# Run tests
RUN go test ./schema -v

# Set the working directory to the root
WORKDIR /

# Copy the run_tests.sh script into the container
COPY run_tests.sh ./
RUN chmod +x /run_tests.sh

# Default command to run bash
ENTRYPOINT ["/bin/bash", "-s"]
