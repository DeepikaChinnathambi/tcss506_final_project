# my-docker-compose-project

## Project Overview
This project is a Dockerized Python application that runs a Flask web service. It is designed to be deployed on an Amazon Web Services (AWS) EC2 instance.

## Files Included
- **Dockerfile**: Contains instructions to build the Docker image for the application.
- **docker-compose.yml**: Defines the services, networks, and volumes for the Docker application.
- **requirements.txt**: Lists the Python dependencies required for the application.
- **README.md**: Documentation for the project.

## Setup Instructions
1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd my-docker-compose-project
   ```

2. **Build the Docker image**:
   ```
   docker-compose build
   ```

3. **Run the application**:
   ```
   docker-compose up
   ```

4. **Access the application**:
   Open your web browser and navigate to `http://<EC2-instance-public-ip>:5000`.

## Usage
This application is a Flask web service that listens on port 5000. You can modify the application code in the project directory and rebuild the Docker image to see changes.

## Notes
- Ensure that your AWS EC2 instance has the necessary security group rules to allow inbound traffic on port 5000.
- You may need to install Docker and Docker Compose on your EC2 instance if they are not already installed.