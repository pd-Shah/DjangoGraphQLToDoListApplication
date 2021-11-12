mv venv/ ../
rm ./db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
mv ../venv .
source venv/bin/activate &&
python manage.py makemigrations &&
python manage.py migrate &&
python manage.py createsuperuser &&
python drop_db.py