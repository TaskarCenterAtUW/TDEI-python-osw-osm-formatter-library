# Use the official Python 3.10 image as the base image
FROM python:3.10

RUN apt-get update && apt-get  install -y \
        gdal-bin \
        libgdal-dev \
        python3-gdal

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Copy the input files into the container at /input
COPY input /app/input

# Copy the source code into the container at /app
COPY src /app/src

# Copy the tests directory into the container at /app/tests
COPY tests /app/tests

# Install GDAL package
RUN pip install GDAL==3.7.3

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Run unit tests
RUN python -m unittest discover -v tests/unit_tests

# Run unit tests with coverage
RUN coverage run --source=src -m unittest discover -v tests/unit_tests

# Display coverage report
RUN coverage report

# Run the Python script
CMD ["python", "src/example.py"]
