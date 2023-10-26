# Use an official Python runtime as the parent image
FROM python:3.11.5-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd gcc libpq-dev

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . /app/

# run 
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]