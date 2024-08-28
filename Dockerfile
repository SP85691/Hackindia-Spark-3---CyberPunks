# Use the official Python 3.11 image based on Alpine Linux
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Copy the .env file to the working directory
COPY .env .env

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app using uvicorn
CMD ["uvicorn", "App.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]