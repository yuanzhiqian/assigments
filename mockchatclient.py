import json
import time
import gevent
from gevent import monkey
monkey.patch_all()

import websocket

def sender(lable, ws):
    while True:
        gevent.sleep(3)
        ts_in_milli = int(round(time.time() * 100))
        msg = {'message': '{\"msg\": \"' + lable + ': I have a dream\", \"ts\":' + str(ts_in_milli) +'}'}
        ws.send(json.dumps(msg))

def receiver(lable, ws):
    while True:
        result = ws.recv()
        message = json.loads(result)['message']
        snt_milli = json.loads(message)['ts']
        rcv_milli = int(round(time.time() * 100))

        print(lable + ': ' + message)
        print(lable + ': old milli: ' + str(snt_milli))
        print(lable + ': new milli: ' + str(rcv_milli))
        print(lable + ": msg received within " + str(rcv_milli - snt_milli) + 'ms')

def client(lable):
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:8000/chat")

    gevent.joinall([gevent.spawn(sender, lable, ws), gevent.spawn(receiver, lable, ws)])

    #ws.close()

if __name__ == '__main__':
    gevent.joinall([gevent.spawn(client, 'client' + str(i)) for i in range(1000)])
    #client('single client')

