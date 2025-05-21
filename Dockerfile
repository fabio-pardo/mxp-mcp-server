FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make server.py executable
RUN chmod +x server.py

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "server.py"]
