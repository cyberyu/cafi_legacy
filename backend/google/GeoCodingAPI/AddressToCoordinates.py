__author__ = 'tanmoy'

#https://developers.google.com/maps/documentation/geocoding/usage-limits 2500 requests/days 10 per sec
#pip install -U googlemaps

import googlemaps
import datetime
import json


class GeocodingTest():
    def __init__(self):
        self.key = 'AIzaSyC8viCWyzR_q2MBKLeRZGpc7BHA3NTNimA' #Autocafi Developer Key
        self.client = googlemaps.Client(self.key)

    def simple_geocode(self,query):
        results = self.client.geocode(query)
        return results
        #print json.dumps(results, indent=1)


query1 = GeocodingTest()
#Input Address :
# address = raw_input("Enter Address: ")
address = '1600 Amphitheatre Parkway, Mountain View, CA'  #Example
results = query1.simple_geocode(address)
print dict(results[0]["geometry"]["location"])
