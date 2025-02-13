import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

import json

from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import quote_plus


def nominatimQuery(
    query,
    base_url = 'https://nominatim.openstreetmap.org/',
    referer = None,
    user_agent = None,
    format = 'json',
    limit = 10):

    url = base_url + 'search?'
    url += 'format=' + format
    url += '&q=' + quote_plus(query)
    url += '&limit=' + str(limit)

    req = Request(url)
    if referer:
        req.add_header('Referer', referer)
    if user_agent:
        req.add_header('User-Agent', user_agent)

    response = urlopen(req)

    r = json.loads(response.read().decode('utf-8'))

    return r
