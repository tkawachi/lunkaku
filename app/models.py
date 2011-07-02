#!/usr/bin/env python
from google.appengine.ext import db
from geo.geomodel import GeoModel
from datetime import datetime,timedelta
import math
from lib import util
#import logging

from google.appengine.api import memcache

class Quake(GeoModel) :
    
    @staticmethod
    def _getSeparatedCache(_cacheKey,roop=0) :
        
        results = memcache.get(_cacheKey + ('__'+str(roop) if roop > 0 else ''))
        ##logging.info('LoadCache : '+_cacheKey + ('__'+str(roop) if roop > 0 else ''))
        
        if results != None :
            
            _end = results[-1]
            #logging.info('Cahe_end : '+str(_end))
            
            if _end == '--end--' :
                del(results[-1])
                return results
            
            else :
                roop += 1
                next = Quake._getSeparatedCache(_cacheKey,roop)
                
                if next != None :
                    #logging.info('return : '+str(next))
                    results = results + next
                    return results
                
                else :
                    #logging.info('return : '+str('None'))
                    return None
            
        else :
            #logging.info('return : '+str('None'))
            return None
        
    @staticmethod
    def _setSeparatedCache(_cacheKey,results,time) :
        
        split = 500
        
        _splitedResult = util.splitList(results,split)
        if len(_splitedResult) == 0 :
            _splitedResult = [[]]
        _splitedResult[-1].append('--end--')
            
        for roop in range(0,len(_splitedResult)) :
            memcache.add(_cacheKey + ('__'+str(roop) if roop > 0 else ''),_splitedResult[roop],time)
            #logging.info('SaveCache : '+_cacheKey + ('__'+str(roop) if roop > 0 else ''))
        
        
        
    
    @staticmethod
    def getDatas(targetYmd,span,lowermag=0,box=None,center=None,max_distance=100000,max_results=1000,cache=True) :
        
        _cacheKey = ''
        if cache :
            _pKey = ''
            if box != None :
                _pKey += str(box.north)+':'+str(box.south)+':'+str(box.west)+':'+str(box.east)
            elif center != None :
                _pKey += str(center.lat)+':'+str(center.lon)+':'+str(max_distance)
            
            _cacheKey = targetYmd+'/'+str(span)+'/'+str(lowermag)+'/'+_pKey+'/'+str(max_results)
            
            results = Quake._getSeparatedCache(_cacheKey)
            
            if results != None :
                #logging.info('use cached Data')
                return results
        
        #logging.info('Loading new Data ')
        query = Quake.all()
        
        date_fieldname = 's_date1'
        if span == 14 :
            date_fieldname = 's_date14'
        elif span == 31 :
            date_fieldname = 's_date31'
        
        query.filter(date_fieldname+' =', targetYmd)
        
        if lowermag > 0:
            query.filter('s_magnitude =', lowermag)
        
        if box != None :
            results = Quake.bounding_box_fetch(query, box, max_results=max_results)
        
        elif center != None :
            results = Quake.proximity_fetch(query, center, max_distance=max_distance, max_results=max_results)
        
        else :
            results = query.fetch(max_results)
        
        if cache :
            Quake._setSeparatedCache(_cacheKey,results,600)
        
        return results
    
    
    date = db.DateTimeProperty()
    mag = db.FloatProperty()
    depth = db.StringProperty()
    areaname = db.StringProperty()
    datasource = db.StringProperty()
    s_date1 = db.StringProperty()
    s_date14 = db.StringListProperty()
    s_date31 = db.StringListProperty()
    s_magnitude = db.ListProperty(long)
    
    def _get_latitude(self):
        return self.location.lat if self.location else None

    def _set_latitude(self, lat):
        if not self.location:
            self.location = db.GeoPt(0,0)

        self.location.lat = lat

    lat = property(_get_latitude, _set_latitude)

    def _get_longitude(self):
        return self.location.lon if self.location else None

    def _set_longitude(self, lon):
        if not self.location:
            self.location = db.GeoPt(0,0)

        self.location.lon = lon

    long = property(_get_longitude, _set_longitude)

    def _get_occur_date(self):
        return self.date if self.date else None
    
    def _set_occur_date(self,occur_date):
        if not self.s_date14:
            self.s_date14 = []
            
        if not self.s_date31:
            self.s_date31 = []
            
        self.date = occur_date
        
        self.s_date1 = occur_date.strftime('%Y%m%d')
        
        for i in range(0,14):
            n_day = occur_date + timedelta(days=+i)
            self.s_date14.append(n_day.strftime('%Y%m%d'))
            self.s_date31.append(n_day.strftime('%Y%m%d'))
        
        for i in range(14,31):
            n_day = occur_date + timedelta(days=+i)
            self.s_date31.append(n_day.strftime('%Y%m%d'))
            
    occur_date = property(_get_occur_date, _set_occur_date)
            
    
    def _get_magnitude(self):
        return self.mag if self.mag else None
    
    def _set_magnitude(self,magnitude):
            
        self.mag = magnitude
        
        _mlevel = int(math.floor(magnitude));
        
        self.s_magnitude = []
        for i in range(1,_mlevel+1):
            self.s_magnitude.append(i)
            
    magnitude = property(_get_magnitude, _set_magnitude)
            