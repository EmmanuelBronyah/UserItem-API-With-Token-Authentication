# UserItem API

The UserItem API is a RESTful web service that allows users to manage items with token authentication. 
It provides endpoints for user management, item creation, and retrieval.

## Features

- User registration and authentication.
- Token-based authentication for secure API access.
- CRUD operations for managing items.
- Hosted at https://useritem-api-with-token-authentication.onrender.com

## Technologies Used

- FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.7+.
- SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- JWT: JSON Web Tokens for secure user authentication.

## Getting Started

### Prerequisites

- Python 3.7+
- PostgreSQL Database

### Installation

1. Clone the repository:

```shell
git clone https://github.com/EmmanuelBronyah/UserItem-API-With-Token-Authentication.git
```
2. **Navigate to the project directory.**
   
```shell
cd userItemAPI-with-token-authentication
```
3. Install dependencies.
   
```shell
pip install -r requirements.txt
```
5. Set up the database.
   
```shell
# Ensure PostgreSQL is running
# Update database URL
alembic upgrade head
```
6. **Run the program.**
   
```shell
python main.py
```

## Usage
1. Run the FASTAPI application.
   
```shell
uvicorn main:app --reload
```
2. Access the API documentation:
Open your browser and go to http://127.0.0.1:8000/docs to explore and test the API using Swagger.

3. Token Authentication:
Obtain a token by sending a POST request to /token with valid user credentials.
Use the obtained token in the Authorization header for subsequent requests.

## API Endpoints
- POST /token: Obtain a JWT token for authentication.
- POST /create-user: Register a new user.
- GET /get-user/{user_id}: Retrieve user details by ID.
- GET /get-users: Retrieve a list of users.
- POST /create-item: Create a new item.
- GET /get-item/{item_id}: Retrieve item details by ID.
- GET /get-items: Retrieve a list of items.

## License
This project is licensed under the MIT License.

## Acknowledgements
- Built by Bronyah Emmanuel.
