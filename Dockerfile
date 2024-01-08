# Use the official Python 3.6 image as a base image
FROM python:3.6

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the port that Flask will run on
EXPOSE 5000

# Define the command to run your application
CMD ["python", "raizentech_test/weather_app.py"]
