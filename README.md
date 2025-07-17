# Fitness Studio Booking API

A Django REST Framework–based API to manage fitness classes and user bookings.

---

## Tech Stack

- Python 3.9
- Django 3.2
- Django REST Framework 3.13.1
- SQLite (default)
- Swagger + ReDoc (for API docs)

---

##  Features

- View all upcoming fitness classes
- Book a class (only if slots are available)
- View bookings by email
- API documentation with Swagger and ReDoc

---

## Setup Instructions

### 1. Clone the project

```bash
git clone https://github.com/shradda-kini/Fitness-Studio.git
cd fitness_studio
```
### 2. Create and activate a virtual environment

python -m venv env
env\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Apply migrations and Load sample data

python manage.py migrate
python manage.py loaddata seed.json

### 5. Run the project

python manage.py runserver

### 6. Running Tests

python manage.py test


API Endpoint 
Base URL: http://localhost:8000/

### Sample Curl request for each of the API endpoints:
1. GET /classes 
curl http://localhost:8000/classes/

2. POST /book
curl -X POST http://localhost:8000/book/ \
  -H "Content-Type: application/json" \
  -d '{"class_id": 1, "client_name": "user1", "client_email": "user1@example.com"}'

3. GET /bookings
curl http://localhost:8000/bookings/?email=user1@example.com
