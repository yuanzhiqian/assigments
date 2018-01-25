gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" -w 4 --bind 0:8000 chatserver

# For env
virtualenv -p /usr/bin/python3 py3env
source py3env/bin/activate
pip install -r requirements.txt
