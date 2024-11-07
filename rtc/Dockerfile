# FROM golang:1

# LABEL maintainer="Sebastián Chamena <sebachamena@gmail.com>"

# ARG env=development
 
# ENV ENV $env
# ENV WORKDIR /rtc

# WORKDIR ${WORKDIR}

# COPY go.* ./

# RUN go mod download

# COPY . .

# RUN go build .

# CMD if [ ${ENV} = development ]; \
# 	then \
#     go get github.com/pilu/fresh && \
# 	fresh; \
# 	fi

# EXPOSE 8888

# Start from the official Go image
FROM golang:1.20

# Set the Current Working Directory inside the container
WORKDIR /rtc

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

# DO NOT CHANGE ANY BELOW CODEWORKDIR /
COPY run_tests.sh ./
RUN chmod +x /run_tests.sh
ENTRYPOINT ["/bin/bash", "-s"]