from google.appengine.api import urlfetch
import json
import logging

def shorten_url(long_url):
    payload={"longUrl": long_url}
    headers = {'Content-Type': 'application/json'}

    r = urlfetch.fetch('https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyB0xUMorwpM1SXEY7BvZcjLoxJ9lx_XTWY',
                     method=urlfetch.POST, headers=headers, payload= json.dumps(payload))
    logging.info("response : {}".format(r.content))
    response = json.loads(r.content)
    return response.get('id', '')


