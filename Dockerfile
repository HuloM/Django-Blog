# Pull base image
FROM python:3.10.2-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app/src

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .