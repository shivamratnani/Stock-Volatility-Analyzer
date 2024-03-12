FROM ubuntu:latest
LABEL authors="shiv"

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir streamlit yfinance requests matplotlib pandas numpy

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Keep the container running
CMD ["tail", "-f", "/dev/null"]