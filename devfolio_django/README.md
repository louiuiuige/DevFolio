# DevFolio Django

DevFolio is a student project showcase platform built with Django.

## Features

- Student registration and login
- Project submission, editing, and deletion
- Category and technology tagging
- Project search and filtering
- Ratings and reviews
- Student dashboard
- Admin management via Django admin

## How to run the system

1. Open PowerShell or Command Prompt.
2. Go to the project folder:
   - cd "C:\Users\Administrator\Documents\folio\devfolio_django"
3. Make sure Python is installed:
   - python --version
4. Create a virtual environment (one time, and never again):
   - python -m venv .venv
5. Activate the virtual environment:
   - Windows (CMD): .venv\Scripts\activate
   - Windows (PowerShell): .venv\Scripts\Activate.ps1
   - You should now see "(.venv)" in your console, like this: "(.venv) C:\Users\you\my_django_project>"
6. Install the dependencies (Django + Pillow):
   - pip install -r requirements.txt
7. Set up the database:
   - python manage.py migrate
8. Create a superuser (optional):
   - python manage.py createsuperuser
9. Seed the sample data:
   - python manage.py seed_data
10. Start the web app:
    - python manage.py runserver 0.0.0.0:8000
11. Open this in the browser:
    - http://127.0.0.1:8000
12. When you're done, deactivate the virtual environment:
    - CTRL + C to stop the server, then type `deactivate`

## Demo accounts

After running the seed command, use these accounts:

- Admin: admin / admin123
- Moderator: moderator / moderator123
- Student 1: student1 / student123
- Student 2: student2 / student123
- Student 3: student3 / student123

## Project status flow

- Draft
- Under Review
- Approved
- Rejected
- Archived

## Notes

- This project uses SQLite for local development.
- If you run the command outside the project folder, Django will show:
  - can't open file 'manage.py': No such file or directory
- Always run the commands inside `C:\Users\Administrator\Documents\folio\devfolio_django`.