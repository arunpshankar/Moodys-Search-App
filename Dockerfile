# Use Python 3.9 Alpine as the base image
FROM python:3.9-slim as builder

# Your Dockerfile content


# Set the working directory to /app
WORKDIR /app


# Upgrade pip and install dependencies in a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --upgrade pip

# Copy the requirements file used for dependencies
COPY requirements.txt .

# Install Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Use multi-stage build to create a slim final image
FROM python:3.9-slim

# Create virtual environment in the final image
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Set the working directory to /app
WORKDIR /app

# Copy the rest of the working directory contents into the container at /app
COPY ./app .

# List contents of the directory to ensure app.py is present
RUN ls -la /app/src/app/

# Set PYTHONPATH to include /app/src so Python can import modules from it
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

# Run app.py when the container launches
CMD ["streamlit", "run", "--server.port=8080", "/app/src/app/app.py"]