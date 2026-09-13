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
4. Set up the database:
   - python manage.py migrate
5. Create a superuser (optional):
   - python manage.py createsuperuser
6. Seed the sample data:
   - python manage.py seed_data
7. Start the web app:
   - python manage.py runserver 0.0.0.0:8000
8. Open this in the browser:
   - http://127.0.0.1:8000

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