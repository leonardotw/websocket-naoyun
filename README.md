# Websocket Stream Graph Application

## Run with docker-compose

* Create and edit `twitter-auth.env` and `app.env`
* Run `docker-compose up`
* Go to http://localhost:29090/

## Run without docker

* Be sure you have a Redis instance running (localy or remotely)
* Edit streamquery.yml and settings.py (to rename and adapt)
* Run `python twitter_streamer.py` This will start the streaming from twitter 
* Run `python ws_connector.py` This will start the websocket manager
* Open `index.html` and enjoy  (`vivagraph.html` is just a vivagraph version of the `index.html`) 

# Web Graph
`index.html` is a quick implementation of Graph Stream visualisation with Linkurious.js / Sigma.js 

Still not perfect (Getting slow at 200nodes & 200 edges)

# Stream Bridge
The `streamplugin_bridge.html` is an example of how to create a local stream proxy to receive graph from a remote source to a local gephi.

Not working properly on 0.9.1 but ok on 0.8.2 