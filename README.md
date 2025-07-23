
# Django Expense Tracker API 

A RESTful API for tracking personal expenses and income, with JWT authentication and user access control.

## Features
- User registration and JWT login
- Personal expense/income tracking
- Automatic tax calculation (flat or percentage)
- Paginated API responses
- Complete CRUD operations
- User access control (regular users vs. superusers)

## Technologies
- Django
- Django REST Framework
- djangorestframework-simplejwt
- SQLite (development)
- Python 

## Setup Instructions

1. **Clone the repository**
2. **Create and activate a virtual environment**
   ```
   pip install virtualenv
   virtualenv -p python3 venv
   # On Windows:
   venv\Scripts\activate
   ```
3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
4. **Apply migrations**
   ```
   python manage.py migrate
   ```
5. **Create a superuser (optional, for admin access)**
   ```
   python manage.py createsuperuser
   ```
6. **Run the development server**
   ```sh
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register/` — Register a new user
- `POST /api/auth/login/` — Obtain JWT tokens
- `POST /api/auth/refresh/` — Refresh JWT token

### Expense/Income
- `GET /api/expenses/` — List user's records (paginated)
- `POST /api/expenses/` — Create new record
- `GET /api/expenses/{id}/` — Get specific record
- `PUT /api/expenses/{id}/` — Update record
- `DELETE /api/expenses/{id}/` — Delete record

## Sample API Requests

### Register
```http
POST /api/auth/register/
{
  "username": "user1",
  "password": "pass1"
}
```

### Login
```http
POST /api/auth/login/
{
  "username": "user1",
  "password": "pass1"
}
Response:
{
  "refresh": "...",
  "access": "..."
}
```

### Create Expense/Income
```http
POST /api/expenses/
Authorization: Bearer <access_token>
{
  "title": "Salary Payment",
  "amount": 1000.00,
  "transaction_type": "credit",
  "tax": 15.00,
  "tax_type": "percentage"
}
Response:
{
  "id": 2,
  "title": "Salary Payment",
  "description": "Salary Payment",
  "amount": 1000.00,
  "transaction_type": "credit",
  "tax": 15.00,
  "tax_type": "percentage",
  "total": 1150.0000,
  "created_at": "July 5, 2025, 2:14 a.m.",
  "updated_at": "July 5, 2025, 2:14 a.m."
}
```

### List Expenses (Paginated)
```http
GET /api/expenses/
Authorization: Bearer <access_token>
Response:
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "title": "Salary Payment",
            "description": "salary",
            "amount": "1000.00",
            "transaction_type": "credit",
            "tax": "15.00",
            "tax_type": "percentage",
            "total": 1150.0,
            "created_at": "2025-07-05T02:14:47.880336Z",
            "updated_at": "2025-07-05T02:14:47.880336Z"
        }
    ]
}
```

## HTTP Status Codes
- 200 OK — Successful GET, PUT
- 201 Created — Successful POST
- 204 No Content — Successful DELETE
- 400 Bad Request — Invalid data
- 401 Unauthorized — Authentication required
- 403 Forbidden — Permission denied
- 404 Not Found — Resource not found

## Testing
Run all tests:
```
python manage.py test expenses
```

## Notes
- Regular users can only access their own records
- Superusers can access all records
- All endpoints require JWT authentication except registration and login
