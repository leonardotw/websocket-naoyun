# Websocket Stream Graph Application

* Be sure you have a Redis instance running (localy or remotely)
* Edit streamquery.yml and settings.py (to rename and adapt)
* Run `python twitter_streamer.py` This will start the streaming from twitter 
* Run `python ws_connector.py` This will start the websocket manager
* Open `index.html` and enjoy  (`vivagraph.html` is just a vivagraph version of the `index.html`) 

# Stream Bridge
The `streamplugin_bridge.html` is an example of how to create a local stream proxy to receive graph from a remote source to a local gephi.

Not working properly on 0.9.1 but ok on 0.8.2 