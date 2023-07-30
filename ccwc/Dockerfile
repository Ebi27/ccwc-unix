# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /ccwc

# Copy the ccwc.py script from the host into the container at /ccwc
COPY ccwc.py /ccwc/ccwc.py
COPY ccwc_test.py /ccwc/ccwc_test.py

# Copy additional files
COPY test.txt /ccwc/test.txt
COPY test_sample.txt /ccwc/test_sample.txt

# Install required Python packages (chardet)
RUN pip install chardet
RUN pip install pytest

# Set a default command for the container
CMD ["pytest", "ccwc_test.py"]
