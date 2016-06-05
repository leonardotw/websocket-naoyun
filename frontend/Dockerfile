FROM nginx
COPY ./index.html /usr/share/nginx/html/index.html
COPY ./streamplugin_bridge.html /usr/share/nginx/html/streamplugin_bridge.html
COPY ./js/ /usr/share/nginx/html/js/
COPY init.sh /srv/init.sh
ENTRYPOINT /srv/init.sh
