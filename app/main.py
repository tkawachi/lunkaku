# -*- coding: utf-8 -*-

import sys; sys.path.insert(0, './distlib.zip')
from google.appengine.ext.webapp.util import run_wsgi_app
import werkzeug
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    run_wsgi_app(app)
