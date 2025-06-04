# Use the official Python 3.7 image as the base image
FROM python:3.7

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements files first to leverage Docker cache
COPY requirements.txt .
COPY libs-requirements.py .

# Install virtualenv
RUN pip install --no-cache-dir virtualenv

# Create a virtual environment
RUN virtualenv venv

# Activate the virtual environment and install dependencies
RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt
RUN ./venv/bin/python libs-requirements.py

# Copy the rest of the application code
COPY . .

# migrate db
RUN ./venv/bin/python web-app/manage.py migrate

# Expose the application port
EXPOSE 8000

# Command to run the application using the virtual environment
CMD ["./venv/bin/python", "web-app/manage.py", "runserver", "0.0.0.0:8000"]
