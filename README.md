# Video-to-Sound Microservices

## Overview
The Video-to-Sound project is a microservices-based application designed to extract audio from video files and perform various sound manipulations. This project is structured using a microservices architecture to ensure scalability, maintainability, and the separation of concerns.

## Architecture
The system consists of the following microservices and supporting services:
- **Auth Service**: Handles authentication and authorization.
- **Converter**: Responsible for extracting audio from video files.
- **Gateway**: Acts as the entry point for the front-end, routing requests to appropriate services.
- **Notification Service**: Manages sending notifications to users.
- **MongoDB and MySQL**: Serve as data storage solutions.
- **RabbitMQ**: Message broker for handling communication between services.

Each service is containerized, making it easy to deploy the system using Docker or Kubernetes.

## File Structure
- `auth_service/`: Authentication service.
- `converter/`: Audio extraction and conversion service.
- `gateway/`: API Gateway.
- `mongo-db/`: MongoDB configurations.
- `mysql-db/`: MySQL database configurations.
- `notification/`: Notification handling service.
- `rabbit/`: RabbitMQ message broker.
- `zuck.mp4`: Sample video file for testing.

## Getting Started
To get started with the Video-to-Sound microservices, follow these steps:
1. Ensure Docker and Docker Compose are installed on your system.
2. Clone the repository to your local machine.
3. Navigate to the project directory and run `docker-compose up` to start the services.
4. Access the gateway via `localhost:8000` to interact with the system.

For detailed instructions on setting up each service, refer to the README.md files within each service directory.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

