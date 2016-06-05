FROM python:3.5

WORKDIR /app/
COPY ./ /app/
RUN mv /app/settings.py.default /app/settings.py

RUN pip install -r req.txt

ENTRYPOINT python /app/twitter_streamer.py
