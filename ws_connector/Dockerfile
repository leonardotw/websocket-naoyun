FROM python:3.5
MAINTAINER Matthieu Totet <@totetmatt>

# Setup
WORKDIR /app/
COPY ./ /app/
RUN mv /app/settings.py.default /app/settings.py
 
# Python req
RUN pip install -r req.txt

# Start
EXPOSE 8888
ENTRYPOINT python /app/ws_connector.py
