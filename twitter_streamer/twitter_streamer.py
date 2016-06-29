#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Simple Twitter to Redis Streamer
# Implementing User to User network

from collections import Counter
import json
import logging

import redis
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

import settings

logger = logging.getLogger()
logger.setLevel(settings.LOG_LEVEL)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

if settings.LOG_FILE:
    file_handler = RotatingFileHandler('twitter_streamer.log', 'a', 1000000, 1)
    file_handler.setLevel(settings.LOG_LEVEL)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(settings.LOG_LEVEL)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

stream = None

class UserGraph(StreamListener):
    def __init__(self,redis_connection):
        self.score = Counter()
        self.redis_connection = redis_connection
    def on_data(self, data):
        try:  
            status = json.loads(data)
            graph_add = {'ae':{},'an':{}}
            graph_change = {'ce':{}}
            originUser = status['user']['screen_name'].lower()
 
            graph_add['an'][originUser]={"label":"@"+originUser,"image":status['user']['profile_image_url_https']}
            for mentions in json.loads(data)['entities']['user_mentions']:
                targetUser = mentions['screen_name'].lower()
                if targetUser != originUser:
                    self.score[(originUser,targetUser)]+=1
             
                    graph_add['an'][targetUser] = {"label":"@"+targetUser,'image':None}
                    graph_add['ae']['{}-->{}'.format(originUser,targetUser)] = {'directed':True,"source":originUser,"target":targetUser,'weight':self.score[(originUser,targetUser)]}
                    if self.score[(originUser,targetUser)] > 1:
                        graph_change['ce']['{}-->{}'.format(originUser,targetUser)] = {'weight':self.score[(originUser,targetUser)],'directed':True,"source":originUser,"target":targetUser}
       
            if graph_add['ae'] :
                redis_connection.publish('twitter', json.dumps(graph_add))

            if graph_change['ce']:
                redis_connection.publish('twitter', json.dumps(graph_change))
            if "retweeted_status" in status.keys():
                self.on_data(json.dumps(status['retweeted_status']))
        except Exception as e:
            logger.error(e)
            logger.error(data)
        return True

    def on_error(self, status):
        logger.info(status)

def sig_handler(sig, frame):
    stream.disconnect()

if __name__ == '__main__':
    with open("streamquery.yml",'rb') as f:
        data = load(f, Loader=Loader)
    f.closed
    redis_connection = redis.StrictRedis(host=settings.REDIS_HOSTNAME, port=settings.REDIS_PORT)

    l = UserGraph(redis_connection)

    auth = OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN,settings.TWITTER_ACCESS_TOKEN_SECRET)


    stream = Stream(auth, l)
    logger.info('Starting tracking : {track}'.format(track=','.join(data['words'])))
    stream.filter(track=data['words'],async=True)
