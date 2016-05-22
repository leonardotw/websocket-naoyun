#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Gateway Redis Pubsub to Websocket

import logging
from logging.handlers import RotatingFileHandler

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import signal
import socket
import redis
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
"""
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
"""
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

class Binder:
    def __init__(self,websocket,params):
        self.websocket = websocket
        redis_connection = redis.Redis(connection_pool=redis_pool) 
        redis_pubsub = redis_connection.pubsub(ignore_subscribe_messages=True)
        redis_pubsub.subscribe(**{'twitter': self.redis_handler})
        self.pubsub_thread = redis_pubsub.run_in_thread(sleep_time=0.001)

    def redis_handler(self,handler):
        logger.debug(handler)
        self.websocket.write_message(handler['data'])
    def close(self):
        self.pubsub_thread.stop()

class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def open(self):
        logger.info('new connection')
        self.application.clients[self]=Binder(self,{})
      
    def on_message(self, message):
        logger.info('message received %s' , message )
 
    def on_close(self):
        logger.info('connection closed' )
        self.application.clients[self].close()
        del self.application.clients[self]
        

application = tornado.web.Application([
                                        (r'/ws', WSHandler),
                                      ], 
                                      debug=True)
application.clients = {}

def sig_handler(sig, frame):
    tornado.ioloop.IOLoop.instance().stop()
    for websocket,binder in application.clients.items():
        binder.close()

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8765)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    myIP = socket.gethostbyname(socket.gethostname())
    logger.info('*** Websocket Server Started at %s***', myIP )

    tornado.ioloop.IOLoop.instance().start()