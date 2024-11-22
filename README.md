# FastAPI Backend for Unified Vendor Data
This project is backend system for managing and unifying product data from multiple vendors. It provides an API to fetch, unify, and serve product information to a frontend (Flutter App). The system is build with **FastAPI**, **PostgreSQL**, and **Kafka**.

### Prerequisites
- Docker & Docker Compose installed on your machine.

### Steps to Run Locally

1. **Clone the Repository
   ```bash
   git clone https://github.com/MehmetGulll/vonder-project-backend
2. **Navigate to the Backend Directory
   ```bash
   cd backend
3. **Run the Docker Compose Command
   ```bash
   docker-compose up --build
4. **Access the API
    ```bash
    http://localhost:8000/docs
5. **If Kafka is Unhealthy
    ```bash
    In case Kafka appears as unhealthy in Docker Desktop, manually restart service:
    docker-compose restart backend