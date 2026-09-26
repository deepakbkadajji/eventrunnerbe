release: python manage.py migrate
web: gunicorn eventrunnerbe.wsgi --log-file - --access-logfile - --error-logfile -