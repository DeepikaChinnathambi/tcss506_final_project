# Use Python 3.11 slim as the base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project
COPY . /app

# Expose the port
EXPOSE 5000

# Run the app via app
ENV FLASK_APP=run

# USE THIS WHEN IN DEVELOPMENT MODE
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# UNCOMMENT THIS WHEN RUNNING IN PRODUCTION MODE
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--no-debugger", "--no-reload"]
