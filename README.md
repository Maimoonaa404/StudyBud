 StudyBud – Community Discussion Platform
Overview

StudyBud is a Django-based web application that allows users to create discussion rooms, explore topics, and engage in conversations. The platform supports authentication, topic-based filtering, and dynamic search functionality.

This project demonstrates backend development fundamentals, database integration, and full CRUD implementation using Django.

Features:

User authentication (Login / Register / Logout)

Create, update, and delete discussion rooms

Topic-based filtering

Search functionality

Real-time room message display

User profile pages

Database-driven content management

 Tech Stack:

Backend: Python, Django

Database: SQLite 

Frontend: HTML, CSS

Version Control: Git

 Key Concepts Implemented:

Django ORM relationships

User authentication & authorization

Query filtering using icontains

CRUD operations

URL routing and view handling

Template inheritance

Database migrations

 Installation & Setup:

Create a virtual environment:

python -m venv venv


Activate the virtual environment:

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Run migrations:

python manage.py migrate


Start the development server:

python manage.py runserver

Future Improvements:

Deploy to cloud (AWS / Render / Railway)

Add REST API endpoints

Improve UI/UX

Add real-time messaging with WebSockets
