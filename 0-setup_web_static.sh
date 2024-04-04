#!/usr/bin/env bash
# Script that prepares a webserver for deployment of website static files
if ! dpkg -l | grep -q "nginx"; then
	apt-get update
	apt-get -y install nginx
fi
mkdir -p /data/web_static/{releases,shared}
mkdir /data/web_static/releases/test
echo "<html><head></head><body>This is a test page</body></html>" > /data/web_static/releases/test/index.html
if [ -L /data/web_static/current ]; then
	rm -f /data/web_static/current
fi
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
sed -i '/server_name _;/a \\n    location \/hbnb_static\/ {\n        alias \/data\/web_static\/current\/;\n    }' /etc/nginx/sites-available/default
nginx -t
service nginx restart
exit 0
