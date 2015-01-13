import urllib, cStringIO
import PIL
import requests
from flask import render_template, send_file
from StringIO import StringIO
from app import app
from PIL import Image

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

