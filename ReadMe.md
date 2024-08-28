# FastAPI Wallet Management System

This FastAPI project is designed to manage user authentication and payout transactions, providing a robust backend system integrated with MongoDB. It includes endpoints for user login, signup, and payout management, alongside MongoDB Express for convenient database management via a web interface.

## Description

The application offers a set of RESTful endpoints that allow for managing and querying payout transactions, user authentication, and registration processes, structured around secure practices and straightforward usability.

## Getting Started

### Prerequisites

Ensure you have Docker and Docker Compose installed on your system to handle the application containers seamlessly. This project is developed using Python 3.8+, FastAPI, and MongoDB.

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PooyanGnb/FastApiWalletManagememt
   cd yourrepository
   ```

2. **Build and Run Docker Containers**
   Use Docker Compose to build the application and its associated services.
   ```bash
   docker-compose up --build
   ```

### Accessing the Application

After starting the containers, the application will be available at:
- **FastAPI Application:** `http://127.0.0.1:808`
- **MongoDB Express Dashboard:** `http://127.0.0.1:8082`

## Endpoints

The application provides the following endpoints:

- **Login (`POST /login`):** Authenticates users and returns a JWT for session management.
- **Signup (`POST /signup`):** Registers a new user and provides a JWT upon successful registration.
- **Payout (`GET /payout`):** Allows querying and managing payout data with secured access.

### Using the Endpoints

Here is a brief overview of how to interact with the endpoints:

- **Login (POST):**


| parameters | type | required |
|----|----|----|
| email | str | Required
| password | str | Required 


  ```bash
  curl -X 'POST' \
    'http://127.0.0.1:8080/login' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "email": "user@example.com",
    "password": "password"
  }'
  ```

### Example 200 OK Response

  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC...",
    "token_type": "bearer"
  }
  ```

***

- **Signup (POST):**

|parameters|type|required|
|----|----|----|
| email | string | Required
| password | str | Required 
| user_type | str | Required

   ```bash
  curl -X 'POST' \
    'http://127.0.0.1:8080/signup' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "email": "newuser@example.com",
    "password": "newpassword",
    "user_type": "admin"
  }'
  ```


### Example 200 OK Response

  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC...",
    "token_type": "bearer"
  }
  ```
***
- **Payout (GET):**


 To access this endpoint, you must include a `Authorization` header with a Bearer token as follows: 
 ```plaintext
  Authorization: Bearer <Your_JWT_Token>
  ```


| Parameter | Type | Description | Required | 
|----|-----|----|----|
| statuses | string | Filter payouts by statuses | Optional | 
| page | int | Specify the page of results to view | Optional |
| start_date | date | Start date for payout filtering | Optional | 
|end_date | date | End date for payout filtering | Optional | 
| user_type | string | Filter by type of user | Optional | 
| payment_start_date| date | Start date for payment filtering | Optional | | payment_end_date | date | End date for payment filtering | Optional |

  ```bash
  curl -X 'GET' \
    'http://127.0.0.1:8080/payout?start_date=2024-01-01&end_date=2024-07-31' \
    -H 'accept: application/json'
  ```

  ### Example 200 OK Response

  ```json
  {
    "page": 1,
    "pageSize": 3,
    "totalPages": 1,
    "totalDocs": 1,
    "results": [
      {
        "id": "123",
        "amount": 100.50,
        "status": "pending",
        "date": "2024-06-01"
      }
    ],
  }
  ```


## Security Recommendations

To ensure the security of your deployment, it is crucial to customize the environment variables and credentials used by the application. Follow the guidelines below to enhance your project's security:

### Change JWT Secret

The JWT secret is used to sign the JSON Web Tokens used in authentication. It is essential that this key is unique and kept secret. Change the JWT secret from its default value to a secure, randomly generated string.

1. Open your `.env` file.
2. Change the value of `JWT_SECRET` to a new, randomly generated string. You can generate a secure string using tools like OpenSSL:

   ```bash
   openssl rand -base64 64
   ```

3. Save the `.env` file.

### Update MongoDB Credentials

The MongoDB credentials used in the application should also be unique and not rely on defaults.

1. **Update `.env` File**:
   - Open your `.env` file.
   - Change `MONGO_USERNAME` and `MONGO_PASSWORD` to your preferred username and a strong password.

2. **Update `docker-compose.yml`**:
   - Open the `docker-compose.yml` file.
   - Find the MongoDB service definition and update the environment variables for the root username and password to match those you set in the `.env` file.

   ```yaml
   services:
     mongo-db:
       environment:
         MONGO_INITDB_ROOT_USERNAME: newusername
         MONGO_INITDB_ROOT_PASSWORD: newpassword
   ```

	- Also don't forget to change the credentials for mongo express too.

	```yaml
   services:
     mongo-express:
       environment:
         ME_CONFIG_MONGODB_ADMINUSERNAME: newusername
         ME_CONFIG_MONGODB_ADMINPASSWORD: newpassword
   ```

3. Restart your Docker containers to apply these changes:

   ```bash
   docker compose down
   docker compose up 
   ```
   or
   ```bash
   docker compose restart
   ```

### Regularly Update Dependencies

Keep all project dependencies up to date to benefit from the latest security patches. Regularly check and update the libraries used by your project.


## MongoDB Express

Access MongoDB Express at `http://127.0.0.1:8082` to manage and view the database directly through your browser.

## Help

If you encounter any issues, refer to the FastAPI [documentation](https://fastapi.tiangolo.com/) for guidance or open an issue in the GitHub repository.

## Authors

Pooyan Ghanbari - [linkedin](https://www.linkedin.com/in/pooyan-ghanbari/) 

## Version History

- **0.1**
  - Initial Release: Basic authentication and payout management.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB Express](https://github.com/mongo-express/mongo-express)