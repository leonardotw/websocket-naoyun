sed -i "s/WS_HOST/$WS_HOST/g" /usr/share/nginx/html/index.html
sed -i "s/WS_HOST/$WS_HOST/g" /usr/share/nginx/html/streamplugin_bridge.html
nginx -g 'daemon off;'
