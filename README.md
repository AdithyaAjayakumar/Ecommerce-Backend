Ecommerce Backend (Django REST Framework)

A modular backend service for a simple ecommerce platform.
It supports user management, product browsing, cart operations, and order processing.

Core Features
-User registration & login using JWT
-Product listing with categories
-Cart add/remove/update
-Order creation & tracking
-Simple payment flow (marked as COD / paid)
-Admin-level product & order controls

Project Structure
-The backend is organized into smaller Django apps:
-users – authentication, JWT, profiles
-productstore – products, categories
-cart – cart items per user
-order – order placement, status
-address – delivery addresses

Ecommerce – main Django project with settings & URLs

Running the Project (Local)
-Create a virtual environment
-Install Django & DRF
-pip install django djangorestframework
-Apply migrations
-python manage.py migrate
-Start the server
-python manage.py runserver

API Style

All routes follow REST principles and return clean JSON responses.
Authentication is token-based (JWT).
