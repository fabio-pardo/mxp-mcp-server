FROM python:3.12-slim

WORKDIR /app

# Install UV package manager
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen

# Copy application code
COPY src/ ./src/
COPY .env* ./

# Expose port
EXPOSE 8000

# Default to REST API server (can be overridden)
CMD ["uv", "run", "python", "src/rest_api/server.py"]
