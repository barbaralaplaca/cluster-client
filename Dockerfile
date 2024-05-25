# Use the specified Python version.
FROM python:3.12-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
