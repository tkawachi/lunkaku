#!/usr/bin/env python
# encoding: utf-8
from google.appengine.ext import db
from geo.geomodel import GeoModel
import logging

class LunchTweet(GeoModel) :
    """ランチのつぶやき情報を格納するモデルですよ。
    """
    twitter_name = db.StringProperty()
    twitter_disp_name = db.StringProperty()
    # URL of image profile
    twitter_profile_image = db.LinkProperty()
    tweet_id = db.IntegerProperty()
    tweet_content = db.TextProperty()
    tweet_date = db.DateTimeProperty(auto_now_add=True)
    
    @staticmethod
    def get_nearby(center, max_distance=100000, max_results=100):
        query = LunchTweet.all()
        return LunchTweet.proximity_fetch(query, center, max_distance=max_distance, max_results=max_results)
        
