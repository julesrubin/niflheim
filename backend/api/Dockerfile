# Use the official Python 3.13 slim image as a base
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy only the dependency files to leverage Docker cache
COPY pyproject.toml uv.lock* /app/

# Install dependencies using uv
RUN uv pip install --no-cache --system -r /app/pyproject.toml

# Copy the rest of the application source code
COPY src/ /app/src

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]