__author__ = 'tanmoy'
#pip install nose-cov requests-oauthlib pytz
#https://travis-ci.org/geopy/geopy/jobs/53600832

from geopy import Bing #case 1
from geopy.location import Location
from geopy.geocoders import Nominatim #case 2
from geopy.geocoders.placefinder import YahooPlaceFinder #case 3 Not working
import oauth2 as oauth

try:
    print "Case 1: Bing"

    bing1 = Bing(api_key = "ArM0ZuNFTWU0KyEVIZwjPu2JmSMT5XQCmLNke6x6ODTL1jwp6cMd7gQffDz5tl8z")
    location =  bing1.geocode('Google hyderabad office')
    print location.address
    print((location.latitude, location.longitude))
    print location.raw
except Exception:
    print "Error..."

try:
    print "Case 2:Nominatim"

    geolocator1 = Nominatim()
    location =  geolocator1.geocode('Google Hyderabad, India')
    print location.address
    print((location.latitude, location.longitude))
except Exception:
    print "Error..."

try:
    print "Case 3:Yahoo"

    geolocator1 = YahooPlaceFinder(consumer_key='dj0yJmk9cDhXZ0lnVkt4NnRRJmQ9WVdrOVIwVXpka1prTkdjbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1iMw',consumer_secret='e74e281d5e9460693c72e58b0abe54599b8921e9')
    location =  geolocator1.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
    print location.address
    print((location.latitude, location.longitude))
except Exception:
    print "Error..."

