import urllib, cStringIO, json, random
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

@app.route('/test2')
def test2():
    url = 'http://userserve-ak.last.fm/serve/300x300/96864147.png'
    url2 = 'http://userserve-ak.last.fm/serve/300x300/62328943.png'

    response = requests.get(url)
    response2 = requests.get(url2)

    new_im = Image.new('RGB', (400,400))

    img_io = StringIO(response.content)
    img_io2 = StringIO(response2.content)

    i = Image.open(img_io)
    i2 = Image.open(img_io2)

    i.thumbnail((100,100))
    i2.thumbnail((100,100))

    new_im.paste(i, (0,0))
    new_im.paste(i2, (100,0))

    out_img = StringIO()
    new_im.save(out_img, 'PNG')

    out_img.seek(0)

    return send_file(out_img, mimetype='image/png')

@app.route('/genimg')
def genimg():
    width = 1366
    height = 768
    url = 'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user=fakelbst&period=6month&api_key=4dff88a0423651b3570253b10b745b2c&format=json&limit=50&page=1'
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

