#!/usr/bin/env python
# encoding: utf-8
from google.appengine.ext import db
from geo.geomodel import GeoModel

class LunchTweet(GeoModel) :
    """ランチのつぶやき情報を格納するモデルですよ。
    """
    twitter_name = db.StringProperty()
    twitter_disp_name = db.StringProperty()
    tweet_id = db.IntegerProperty()
    tweet_content = db.TextProperty()
    
