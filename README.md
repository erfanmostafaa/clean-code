Project Title: FastAPI Payout Service

### Overview:
This project is a FastAPI-based web service that provides endpoints for managing payouts. It includes functionality for authentication, querying payouts, and handling pagination.

### Features:
- User authentication using JWT tokens.
- Endpoint for retrieving payout information with pagination support.
- Integration with MongoDB for data storage.
- Unit tests to ensure the reliability of endpoints.

### Project Structure:

/project
|-- /services
|   |-- auth_service.py
|   |-- db_service.py
|-- /utils
|   |-- pagination.py
|-- main.py
|-- test_main.py
|-- requirements.txt
|-- .env
|-- README.md


- `/services`: Contains modules for handling authentication and database operations.
- `/utils`: Contains utility functions, especially for pagination.
- `main.py`: Entry point of the application, containing FastAPI endpoints.
- `test_main.py`: Unit tests for the endpoints implemented in main.py.
- `requirements.txt`: List of required Python packages.
- `.env`: Configuration file for environment variables.
- `README.md`: Documentation file providing an overview of the project, setup instructions, and usage details.

### Setup Instructions:
1. Clone the repository: git clone <repository-url>
2. Navigate to the project directory: cd project
3. Create and activate a virtual environment (optional but recommended).
4. Install dependencies: pip install -r requirements.txt
5. Set up environment variables in .env file.
6. Run the application: uvicorn main:app --reload

### Usage:
1. Authentication:
   - Obtain a JWT token by authenticating with the /login endpoint.
   - Include the token in the Authorization header for subsequent requests.

2. Retrieve Payouts:
   - Send GET requests to the /payout endpoint.
   - Provide query parameters for filtering and pagination:
     - statuses: Comma-separated list of payout statuses.
     - start_date and end_date: Date range for payouts creation.
     - payment_start_date and payment_end_date: Date range for payouts payment.
     - page: Page number for pagination.

### Endpoint Details:
- `/login`:
  - Method: POST
  - Request Body: JSON with username and password.
  - Response: JWT token upon successful authentication.

- `/payout`:
  - Method: GET
  - Query Parameters:
    - statuses (optional): Comma-separated list of payout statuses.
    - start_date and end_date (optional): Date range for payouts creation.
    - payment_start_date and payment_end_date (optional): Date range for payouts payment.
    - page (optional): Page number for pagination.
  - Response: Paginated list of payouts based on provided filters.

### Testing:
- Unit tests are provided in test_main.py.
- Run tests using pytest command in the project directory.

### Dependencies:
- FastAPI
- PyJWT
- PyMongo
- pytest

### Environment Variables:
- JWT_SECRET: Secret key for JWT token generation.
- JWT_ALGORITHM: Algorithm used for JWT token encoding.
- JWT_EXPIRATION_MINUTES: Expiration time for JWT token.
- MongoDB related environment variables.

### Conclusion:
This project demonstrates the implementation of a FastAPI-based payout service with authentication, database integration, and testing. It provides a scalable and efficient solution for managing payouts in a web application environment.

For any further information or inquiries, please contact the project maintainer.

Author: [Your Name]
Contact: [Your Email]
Date: [Date]