# Use Python base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Flask API
EXPOSE 8110

# Run the Flask app
CMD ["python", "run.py"]
