import json
import pickle
import redis

from multiprocessing import Manager

import logging
import uuid

import gevent
from gevent import monkey; monkey.patch_socket()
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.resource import Resource, WebSocketApplication


class MemoryBroker():
    def __init__(self):
        self.sockets = {}

    def subscribe(self, key, socket):
        if key not in self.sockets:
            self.sockets[key] = set()

        if socket in self.sockets[key]:
            return

        self.sockets[key].add(socket)

    def publish(self, key, data):
        for socket in self.sockets[key]:
            socket.on_broadcast(data)

    def unsubscribe(self, key, socket):
        if key not in self.sockets: return

        self.sockets[key].remove(socket)


#broker = MemoryBroker()

#class RedisBroker():
#    def __init__(self):
#        self.r = redis.Redis(host='localhost',port=6379,db=0)
#        self.prefix = 'chtsrv_sk:'
#
#    def subscribe(self, key, socket):
#        self.r.sadd(self.prefix + key, chat2info(socket))
#
#    def publish(self, key, data):
#        for member in self.r.smembers(self.prefix + key):
#            socket = info2chat(member)
#            socket.on_broadcast(data)
#
#    def unsubscribe(self, key, socket):
#        self.r.srem(self.prefix + key, chat2info(socket))
#
#
#broker = RedisBroker()
#
#
#def chat2info(obj):
#    return pickle.dumps(obj.userid)
#
#def info2chat(info):
#    print(info)
#    chat = Chat()
#    chat.userid = pickle.loads(info)
#    return chat


class MemoryBrokerWithRedis():
    def __init__(self):
        self.subscribers = {}
        self.r = redis.Redis(host='localhost',port=6379,db=0)

    def courier(self, key, socket, ps):
        ps.subscribe([key])
        for item in ps.listen():
            #print(item)
            if item['type'] == 'message':
                socket.on_broadcast(json.loads(item['data'].decode('utf-8')))

        #print('bye!')

    def subscribe(self, key, socket):
        if key not in self.subscribers:
            self.subscribers[key] = dict()

        if socket.userid.hex in self.subscribers[key]:
            return

        ps = self.r.pubsub()
        self.subscribers[key][socket.userid.hex] = ps

        gevent.spawn(self.courier, key, socket, ps)

    def publish(self, key, data):
        self.r.publish(key, json.dumps(data))

    def unsubscribe(self, key, socket):
        if key not in self.subscribers: return

        ps = self.subscribers[key][socket.userid.hex]
        ps.unsubscribe()
        del self.subscribers[key][socket.userid.hex]

        #if socket.userid.hex not in self.subscribers[key]: print('unsubscribed')


broker = MemoryBrokerWithRedis()


class Chat(WebSocketApplication):

    def on_open(self, *args, **kwargs):
        self.userid = uuid.uuid4()
        broker.subscribe('room1', self)

    def on_close(self, *args, **kwargs):
        broker.unsubscribe('room1', self)

    def on_message(self, message, *args, **kwargs):
        if not message: return

        data = json.loads(message)
        data['user'] = self.userid.hex
        broker.publish('room1', data)

    def on_broadcast(self, data):
        self.ws.send(json.dumps(data))


def index(environ, start_response):
    start_response('200 OK', [('Content-type','text/html')])
    html = open('index.html', 'rb').read()
    return [html]


application = Resource([
    ('^/chat', Chat),
    ('^/', index)
])


if __name__ == '__main__':
    #print("script mode")
    WSGIServer('{}:{}'.format('0.0.0.0', 8000), application, handler_class=WebSocketHandler).serve_forever()
