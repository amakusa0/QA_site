rm -r ./questions/migrations
rm -r ./accounts/migrations
rm db.sqlite3
python manage.py makemigrations questions
python manage.py makemigrations accounts
python manage.py migrate
