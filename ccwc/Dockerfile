# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /ccwc

# Copy the ccwc.py script from the host into the container at /ccwc
COPY ccwc.py /ccwc/ccwc.py

# Copy ccwc.py's additional file
COPY test.txt /ccwc/test.txt

# Install required Python packages (chardet)
RUN pip install chardet

# Set the entry point to run the ccwc.py script when the container starts
ENTRYPOINT ["python", "./ccwc.py"]
