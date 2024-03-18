# Python image to use.
FROM python:3.11-alpine

# Set the working directory to /app
WORKDIR /app

# copy the requirements file used for dependencies
COPY requirements.txt .

RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Run app.py when the container launches
CMD streamlit run --server.port=8080 /app/src/app/app.py