# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app
# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    protobuf-compiler \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /app

# Install dependencies including development ones
RUN pip install -r requirements.txt

COPY ./app/ /app

# Run the app. CMD can be overridden when starting the container
CMD uvicorn main:app --host 0.0.0.0 --port 8081 --reload