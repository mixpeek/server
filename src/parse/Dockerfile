# Use an official Ubuntu base image
FROM ubuntu:20.04

# Set the working directory in the container
WORKDIR /usr/src/app

# Define the Tika version to use
ARG TIKA_VERSION=2.9.1

# Install Python 3.10, OpenJDK 11, curl, and supervisor
RUN apt-get update && \
    apt-get install -y software-properties-common curl && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3-pip openjdk-11-jdk python3.10-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    # Update alternatives to use Python 3.10 as the default python3
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 && \
    update-alternatives --set python3 /usr/bin/python3.10

# Install pip for Python 3.10
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

# Install supervisor
RUN pip3 install supervisor

# Now pip3 and python3 will point to the Python 3.10 versions
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Download the Apache Tika server jar
RUN curl -O https://downloads.apache.org/tika/${TIKA_VERSION}/tika-server-standard-${TIKA_VERSION}.jar

# Copy your FastAPI application and other necessary files
COPY . /usr/src/app

# Create the logs directory
RUN mkdir -p /usr/src/app/logs

# Create a supervisord.conf file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose port for Uvicorn and potentially for Tika server if needed
EXPOSE 8001

# Use CMD to run supervisord, which will start both the Tika server and Uvicorn
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
