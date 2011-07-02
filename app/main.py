# -*- coding: utf-8 -*-

import sys; sys.path.insert(0, './distlib.zip')
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import werkzeug
import logging
from flask import Flask, json, request, make_response
app = Flask(__name__)

import tweepy
import models

@app.route('/')
def index():
    return 'hello world'

@app.route('/list_dummy')
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
    response = make_response(json.dumps(dummy_result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    return response

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

"""
@app.route('/create_dummy')
def create_dummy_data():
    l = models.LunchTweet(
    twitter_name = u'kawachi',
    twitter_disp_name = u'Takashi Kawachi',
    twitter_profile_image = u'http://example.com/hoge.jpg',
    tweet_id = 12345657,
    tweet_content = u'content', location=db.GeoPt(12.3, 45.6))
    l.update_location()
    l.put()
    return ''
"""

def get_tweets(hash_tag, tweet_id):
    api = tweepy.API()
    return api.search(q=hash_tag, since_id=tweet_id)


@app.route('/admin/fetch_tweet')
def fetch_tweet():
    latest_tweet = models.LunchTweet.all().order("-tweet_date").get()
    if latest_tweet:
        since_id = latest_tweet.tweet_id
    else:
        since_id = 0
    logging.info(since_id)
    api = tweepy.API()
    tweets = api.search(q='#lunkaku', since_id=since_id, show_user=True)
    n = 0
    for t in tweets:
        # TODO type=Point 以外も使えるようにする
        if not t.geo or t.geo[u'type'] != u'Point':
            continue
        coord = t.geo[u'coordinates']

        user = api.get_user(screen_name=t.from_user)
        # TODO user の位置情報を利用する

        l = models.LunchTweet(twitter_name=t.from_user,
                twitter_disp_name = user.name,
                twitter_profile_image = t.profile_image_url,
                tweet_id = t.id,
                tweet_content = t.text,
                tweet_date = t.created_at,
                location = db.GeoPt(coord[0], coord[1]))
        l.update_location()
        l.put()
        n += 1
    return "%d fetched" % n


if __name__ == '__main__':
    run_wsgi_app(app)
