# Task Management Application with Task Completion Report

## 🚗 Overview
This project is a **Task Management Application with Task Completion Report** built with **Django Rest Framework (DRF)**


## 📌 Features

### 🏷 User Authentication:
- User registration and login functionality using Django Rest Framework's authentication.

### 2. Roles and Permissions:
## SuperAdmin:
○ Can manage admin(create, delete, assign roles, and promote/demote
admin).
○ Can manage users (create, delete,update).
○ Can manage tasks and view all task completion reports.
○ Can access full Admin panel with all privileges.

## Admin:
○ Can create, assign, view, and manage tasks.
○ Can view task completion reports for tasks assigned to users.
○ Has limited access to the Admin panel: Can manage tasks but not
users.

## User:
○ Can view their assigned tasks, update their task status, and submit a
completion report (including worked hours).
○ Can only interact with their own tasks through the User API.



## 🚀 Getting Started

### 📌 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/PriyankaTaug/TaskManagement.git
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migration
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```
