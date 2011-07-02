# -*- coding: utf-8 -*-

import sys; sys.path.insert(0, './distlib.zip')
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import werkzeug
from flask import Flask, json, request
app = Flask(__name__)

import models

@app.route('/')
def index():
    return 'hello world'

def list_dummy():
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

@app.route('/list')
def list_endpoint():
    """nearby の LunchTweet 一覧を json で返します。
    """
    lat = float(request.values['lat'])
    lon = float(request.values['lon'])
    nearby_tweets = models.LunchTweet.get_nearby(db.GeoPt(lat, lon))
    result = []
    for tweet in nearby_tweets:
        result.append({
            'twitter_name': tweet.twitter_name,
            'twitter_profile_image': tweet.twitter_profile_image,
            'lat': tweet.location.lat,
            'lon': tweet.location.lon,
            'content': tweet.tweet_content,
            })
    return json.dumps(result)

if __name__ == '__main__':
    run_wsgi_app(app)
