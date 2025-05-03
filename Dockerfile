FROM ubuntu:latest
LABEL authors="Micah Potter"

ENTRYPOINT ["top", "-b"]
# Use an official Python runtime
FROM python:3.12-slim

# Set working directory
WORKDIR /daily_reading_bot

# Copy project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your bot
CMD ["python", "main.py"]