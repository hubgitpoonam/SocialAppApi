# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /socialapp

# Copy the dependencies file to the working directory
COPY . socialapp/

RUN pip install --upgrade pip


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Expose the port Django runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
