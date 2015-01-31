artwork-wallpaper
=================

Get an awsome wallpaper from your last.fm library

Development
-----
    npm install
    pip install -r requirements.txt

    redis-server
    celery -A app.views.celery worker --loglevel=info
    python server.py
