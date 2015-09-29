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

    def test_simple_geocode(self,query):

        results = self.client.geocode(query)
        print json.dumps(results, indent=1)

    def test_reverse_geocode(self,lat,lon):

        results = self.client.reverse_geocode((lat, lon))
        print json.dumps(results,indent=1)

    def test_geocode_with_bounds(self):

        results = self.client.geocode('Winnetka',
                                  bounds={'southwest': (34.172684, -118.604794),
                                          'northeast':(34.236144, -118.500938)})
        print json.dumps(results,indent=1)

    def test_geocode_with_region_biasing(self):

        results = self.client.geocode('Toledo', region='es')
        print json.dumps(results,indent=1)

    def test_geocode_with_component_filter(self):

        results = self.client.geocode('santa cruz',
            components={'country': 'ES'})
        print json.dumps(results,indent=1)

    def test_reverse_geocode_restricted_by_type(self):

        results = self.client.reverse_geocode((40.714224, -73.961452),
                                          location_type='ROOFTOP',
                                          result_type='street_address')
        print json.dumps(results,indent=1)

    def test_direction(self): #though not working as of now

        now = datetime.now()
        results = self.client.directions("Sydney Town Hall",
                                         "Parramatta, NSW",
                                         mode="transit",
                                         departure_time=now)

        print json.dumps(results,indent=1)


query1 = GeocodingTest()
#Examples :
query1.test_simple_geocode('1600 Amphitheatre Parkway, Mountain View, CA')
