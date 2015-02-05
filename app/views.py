import urllib, cStringIO, json, random
import PIL
import requests
from flask import render_template, send_file, jsonify, session, request
from StringIO import StringIO
from app import app
from PIL import Image
from celery import Celery
from celery.result import AsyncResult

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    CELERY_TASK_RESULT_EXPIRES = 600
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

@celery.task(bind=True)
def gen_img(self, img_urls, width, height, length):
    new_im = Image.new('RGB', (width, height))
    for i in xrange(0, width, length):
        for j in xrange(0, height, length):
            print i
            print j
            img = random.choice(img_urls)
            img_urls.remove(img)
            r = requests.get(img)
            img_io = StringIO(r.content)

            image = Image.open(img_io)
            image.thumbnail((length, length))

            new_im.paste(image, (i, j))
            self.update_state(state='PROGRESS', meta={'currentj':j, 'currenti': i})

    out_img = StringIO()
    new_im.save(out_img, 'JPEG', quality=90)
    out_img.seek(0)
    return out_img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/genimg', methods=['POST'])
def genimg():
    width =  request.values.get('width', 0, type=int)
    height = request.values.get('height', 0, type=int)

    length = int(max(width,height) * 0.128) + 1
    length = min(length, 300) #max size 300*300

    session['length'] = length
    session['width'] = width
    session['height'] = height

    url = 'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user=fakelbst&api_key=4dff88a0423651b3570253b10b745b2c&format=json&limit=100&page=1'
    # TODO: last.fm server error, set timeout
    response = requests.get(url)
    data =  json.loads(response.text)

    albums = data['topalbums']['album']

    img_urls = []
    for a in albums:
        if a['image'][3]['#text'] != 'http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png':
            img_urls.append(a['image'][3]['#text'])

    task = gen_img.delay(img_urls, width, height, length)

    return jsonify({'task_id': task.task_id, 'success': True})

@app.route("/task_result/<task_id>")
def task_result_check(task_id):
    res = gen_img.AsyncResult(task_id)
    if res.state == 'PROGRESS':
        width = res.info.get('currenti', 0)
        height = res.info.get('currentj', 0)
        current = float(width)/session['width'] + float(height)/session['height'] * session['length']/session['width']
        return jsonify({'ready': False, 'current': '%.4f' % current})

    if res.ready() != False:
        return jsonify({'ready': True})
    else:
        return jsonify({'ready': False, 'current': 0})

@app.route('/img/<task_id>')
def return_imgobk(task_id):
    res = gen_img.AsyncResult(task_id)
    result = res.result
    return send_file(result, mimetype='image/jpg')

