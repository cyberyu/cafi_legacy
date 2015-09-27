__author__ = 'tanmoy'

"""
<a href="/wiki/Geographic_coordinate_system" title="Geographic coordinate system">Coordinates</a>
<!-- The multiple class approach -->
<span style="display: none" class="geo">
<span class="latitude">37.33182</span>
<span class="longitude">-122.03118</span>
</span>
<!-- When used as one class, the separator must be a semicolon -->
<span style="display: none" class="geo">37.33182 ; -122.03118</span>
"""

import requests # pip install requests
from BeautifulSoup import BeautifulSoup # pip install BeautifulSoup
import json
# XXX: Any URL containing a geo microformat...

URL = 'https://en.wikipedia.org/wiki/Apple_Inc.'

# In the case of extracting content from Wikipedia, be sure to
# review its "Bot Policy," which is defined at
# http://meta.wikimedia.org/wiki/Bot_policy#Unacceptable_usage

req = requests.get(URL, headers={'User-Agent' : "AutoCafi", 'From': 'deloittecafi@gmail.com'})
#print req.text
soup = BeautifulSoup(req.text)


geoTag = soup.find(True, 'geo')

if geoTag and len(geoTag) > 1:
    lat = geoTag.find(True, 'latitude').string
    lon = geoTag.find(True, 'longitude').string
    print 'Location is at', lat, lon
elif geoTag and len(geoTag) == 1:
    (lat, lon) = geoTag.string.split(';')
    (lat, lon) = (lat.strip(), lon.strip())
    print 'Location is at', lat, lon
else:
    print 'No location found'