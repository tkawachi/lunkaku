# -*- coding: utf-8 -*-

import sys; sys.path.insert(0, './distlib.zip')
from google.appengine.ext.webapp.util import run_wsgi_app
import werkzeug
from flask import Flask, json
app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world'

@app.route('/list')
def list():
    """ダミーデータを返すようにしてます"""
    dummy_result = [
        {
            'twitter_name': 'as_a_mix',
            'lat': 123.456,
            'lon': 12.3456,
            'content': u"コンテンツ",
            'image': u"http://www.chiki2-tan2.com/img/page2/shinranchi.jpg",
        },
        {
            'twitter_name': 'kawachi',
            'lat': 123.456,
            'lon': 23.456,
            'content': u"コンテンツ2",
            'image': u"http://www.i-nono.jp/pc/image/nc_gpf01Photo0120071219075808.jpg"
        },
        ]
    return json.dumps(dummy_result)

if __name__ == '__main__':
    run_wsgi_app(app)
