
# Django Expense Tracker API 

A comprehensive RESTful API for tracking personal expenses and income, featuring advanced Django REST Framework capabilities including JWT authentication, filtering, searching, ordering, throttling, and multiple renderers/parsers.

## Features
- **Authentication & Authorization**
  - User registration and JWT login
  - User access control (regular users vs. superusers)
  - Secure token-based authentication

- **Expense/Income Management**
  - Personal expense/income tracking
  - Automatic tax calculation (flat or percentage)
  - Complete CRUD operations
  - Paginated API responses

- **Advanced API Features**
  - **Renderers**: JSON, Browsable API, Admin renderers
  - **Parsers**: JSON, Form, MultiPart parsers
  - **Throttling**: Rate limiting (100/hour for anonymous, 1000/hour for authenticated users)
  - **Filtering**: Filter by transaction type, tax type, dates
  - **Searching**: Full-text search across title and description
  - **Ordering**: Sort by amount, date, title

## Technologies
- **Backend**: Django 5.2.4, Django REST Framework 3.16.0
- **Authentication**: djangorestframework-simplejwt 5.5.0
- **Database**: SQLite (development)
- **Filtering**: django-filter
- **Language**: Python 3.12 

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
- `GET /api/expenses/` — List user's records (paginated, with filtering, searching, ordering)
- `POST /api/expenses/` — Create new record
- `GET /api/expenses/{id}/` — Get specific record
- `PUT /api/expenses/{id}/` — Update record
- `DELETE /api/expenses/{id}/` — Delete record

## Advanced API Features

### 🎨 Renderers
The API supports multiple response formats:

- **JSON Renderer** (`application/json`): Standard JSON responses
- **Browsable API Renderer** (`text/html`): Interactive web interface
- **Admin Renderer** (`text/html`): Admin-style formatted responses

**Usage:**
```http
GET /api/expenses/
Accept: application/json
```

### 📥 Parsers
The API accepts multiple input formats:

- **JSON Parser** (`application/json`): JSON request bodies
- **Form Parser** (`application/x-www-form-urlencoded`): HTML form data
- **MultiPart Parser** (`multipart/form-data`): File uploads and mixed data

**Usage:**
```http
POST /api/expenses/
Content-Type: application/json
{
  "title": "Coffee",
  "amount": "5.50",
  "transaction_type": "debit"
}
```

### 🚦 Throttling
Rate limiting to prevent abuse:

- **Anonymous users**: 100 requests per hour
- **Authenticated users**: 1000 requests per hour

**Response headers:**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

**Throttled response:**
```json
{
  "detail": "Request was throttled. Expected available in 3600 seconds."
}
```

### 🔍 Filtering
Filter expenses by specific criteria:

**Available filters:**
- `transaction_type`: Filter by credit/debit
- `tax_type`: Filter by flat/percentage
- `created_at`: Filter by creation date
- `updated_at`: Filter by update date

**Examples:**
```http
GET /api/expenses/?transaction_type=debit
GET /api/expenses/?tax_type=percentage
GET /api/expenses/?created_at__gte=2024-01-01&created_at__lte=2024-01-31
GET /api/expenses/?transaction_type=credit&tax_type=flat
```

### 🔎 Searching
Full-text search across expense data:

**Searchable fields:**
- `title`: Expense title
- `description`: Expense description

**Examples:**
```http
GET /api/expenses/?search=coffee
GET /api/expenses/?search=rent payment
GET /api/expenses/?search=monthly groceries
```

### 📊 Ordering
Sort expenses by various fields:

**Orderable fields:**
- `created_at`: Creation date
- `updated_at`: Last update date
- `amount`: Expense amount
- `title`: Expense title

**Examples:**
```http
GET /api/expenses/?ordering=amount          # Ascending
GET /api/expenses/?ordering=-amount         # Descending
GET /api/expenses/?ordering=-created_at     # Newest first
GET /api/expenses/?ordering=title          # Alphabetical
```

### 🔄 Combined Features
Use multiple features together:

```http
GET /api/expenses/?transaction_type=debit&search=coffee&ordering=-amount
```

This request will:
1. Filter for debit transactions
2. Search for "coffee" in title/description
3. Sort by amount (highest first)

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

### Unit Tests
Run all tests:
```
python manage.py test expenses
```

### API Testing with Postman

#### 1. Setup Postman Collection
1. Create a new collection: "Django Expense Tracker API"
2. Set collection variables:
   - `base_url`: `http://localhost:8000`
   - `jwt_token`: `YOUR_JWT_TOKEN_HERE`
3. Create environment with the same variables

#### 2. Authentication Testing
**Register User:**
```http
POST {{base_url}}/api/auth/register/
Content-Type: application/json
{
  "username": "testuser",
  "password": "testpass123"
}
```

**Login:**
```http
POST {{base_url}}/api/auth/login/
Content-Type: application/json
{
  "username": "testuser",
  "password": "testpass123"
}
```

#### 3. Testing Renderers
**JSON Renderer:**
```http
GET {{base_url}}/api/expenses/
Accept: application/json
Authorization: Bearer {{jwt_token}}
```

**Browsable API:**
```http
GET {{base_url}}/api/expenses/
Accept: text/html
Authorization: Bearer {{jwt_token}}
```

#### 4. Testing Parsers
**JSON Parser:**
```http
POST {{base_url}}/api/expenses/
Content-Type: application/json
Authorization: Bearer {{jwt_token}}
{
  "title": "Coffee",
  "description": "Morning coffee",
  "amount": "5.50",
  "transaction_type": "debit",
  "tax": "0.50",
  "tax_type": "flat"
}
```

**Form Parser:**
```http
POST {{base_url}}/api/expenses/
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer {{jwt_token}}
title=Coffee&description=Morning coffee&amount=5.50&transaction_type=debit&tax=0.50&tax_type=flat
```

#### 5. Testing Throttling
**Anonymous Throttling:**
```http
GET {{base_url}}/api/auth/register/
# Make 100+ requests quickly to test throttling
```

**Authenticated Throttling:**
```http
GET {{base_url}}/api/expenses/
Authorization: Bearer {{jwt_token}}
# Make 1000+ requests quickly to test throttling
```

#### 6. Testing Filtering
```http
GET {{base_url}}/api/expenses/?transaction_type=debit
Authorization: Bearer {{jwt_token}}

GET {{base_url}}/api/expenses/?tax_type=percentage
Authorization: Bearer {{jwt_token}}

GET {{base_url}}/api/expenses/?created_at__gte=2024-01-01
Authorization: Bearer {{jwt_token}}
```

#### 7. Testing Searching
```http
GET {{base_url}}/api/expenses/?search=coffee
Authorization: Bearer {{jwt_token}}

GET {{base_url}}/api/expenses/?search=rent payment
Authorization: Bearer {{jwt_token}}
```

#### 8. Testing Ordering
```http
GET {{base_url}}/api/expenses/?ordering=amount
Authorization: Bearer {{jwt_token}}

GET {{base_url}}/api/expenses/?ordering=-created_at
Authorization: Bearer {{jwt_token}}
```

#### 9. Combined Features Testing
```http
GET {{base_url}}/api/expenses/?transaction_type=debit&search=coffee&ordering=-amount
Authorization: Bearer {{jwt_token}}
```

### Performance Testing
- **Response Time**: Monitor response times
- **Load Testing**: Use Postman Collection Runner with 100+ iterations

## Troubleshooting

### Common Issues

#### 1. Throttling Not Working
**Error:** No throttling response
**Solution:**
- Verify throttling settings in settings.py
- Ensure you're hitting the rate limit (100/hour for anonymous, 1000/hour for authenticated)

#### 2. Filtering Not Working
**Error:** Filters not applied
**Solution:**
- Check filter field names match model fields
- Verify django-filter is installed
- Check filter_backends configuration in views.py

#### 3. Authentication Issues
**Error:** 401 Unauthorized
**Solution:**
- Verify JWT token is valid and not expired
- Check Authorization header format: `Bearer YOUR_TOKEN`
- Ensure token is properly set in Postman environment

### Performance Monitoring

#### API Response Times
- Monitor response times in Postman
- Verify throttling is working

## Dependencies

### Required Packages
```
asgiref==3.9.0
Django==5.2.4
djangorestframework==3.16.0
djangorestframework_simplejwt==5.5.0
PyJWT==2.9.0
sqlparse==0.5.3
tzdata==2025.2
django-filter==24.2
```

### System Requirements
- Python 3.12+
- SQLite (development)
- Virtual Environment (recommended)

## Notes
- **Security**: Regular users can only access their own records
- **Admin Access**: Superusers can access all records
- **Authentication**: All endpoints require JWT authentication except registration and login
- **Rate Limiting**: Anonymous users limited to 100 requests/hour, authenticated users to 1000 requests/hour
- **Filtering**: Supports filtering by transaction type, tax type, and date ranges
- **Searching**: Full-text search across title and description fields
- **Ordering**: Sort by amount, date, or title in ascending/descending order
