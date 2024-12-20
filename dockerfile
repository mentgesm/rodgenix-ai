# Use Python as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY ./app /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the Flask port
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]

