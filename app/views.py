import urllib, cStringIO, json, random
import PIL
import requests
from flask import render_template, send_file, jsonify
from StringIO import StringIO
from app import app
from PIL import Image
from celery import Celery

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task()
def add_together(a, b):
    return a + b

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    url = 'http://userserve-ak.last.fm/serve/300x300/96864147.png'
    response = requests.get(url)
    img_io = StringIO(response.content)
    i = Image.open(img_io)
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

@app.route('/genimg')
def genimg():
    width = 1366
    height = 768
    url = 'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user=fakelbst&api_key=4dff88a0423651b3570253b10b745b2c&format=json&limit=50&page=1'
    response = requests.get(url)
    data =  json.loads(response.text)
    print data

    albums = data['topalbums']['album']

    img_urls = []
    for a in albums:
        img_urls.append(a['image'][2]['#text'])

    new_im = Image.new('RGB', (width, height))

    for i in xrange(0, width, 100):
        for j in xrange(0, height, 100):
            print i
            print j
            img = random.choice(img_urls)
            r = requests.get(img)
            img_io = StringIO(r.content)

            image = Image.open(img_io)
            image.thumbnail((100,100))

            new_im.paste(image, (i, j))

    out_img = StringIO()
    new_im.save(out_img, 'PNG')
    out_img.seek(0)

    return send_file(out_img, mimetype='image/png')

@app.route('/test_celery')
def test_celery():
    result = add_together.delay(23, 42)
    print(result.get())
    return jsonify({})

