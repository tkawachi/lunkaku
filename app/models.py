#!/usr/bin/env python
# encoding: utf-8
from google.appengine.ext import db
from geo.geomodel import GeoModel

class LunchTweet(GeoModel) :
    """$B%i%s%A$N$D$V$d$->pJs$r3JG<$9$k%b%G%k$G$9$h!#(B
    """
    twitter_name = db.StringProperty()
    twitter_disp_name = db.StringProperty()
    tweet_id = db.IntegerProperty()
    tweet_content = db.TextProperty()
    
