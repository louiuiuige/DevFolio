
first do this in terminal:
(cd "C:\Users\Administrator\Documents\folio\devfolio_django")
(change depending on your folder address, as long it ends with "\devfolio_django")

run this (one time and never again):
python -m venv .venv

do this :
if Windows (CMD) ".venv\Scripts\activate"
if Windows (PowerShell) ".venv\Scripts\Activate.ps1"

(you should now see this in your console "(.venv)")
like this -> "(.venv) C:\Users\you\my_django_project>"

then type this and hit enter:
"python manage.py runserver"

(you are now running the server, you will see the site when you enter this into
your browser "http://127.0.0.1:8000/")

to deactivate, just do "CTRL + C"
