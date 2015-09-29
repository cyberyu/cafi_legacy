

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line example for Custom Search.
Command-line application that does a search.
"""

__author__ = 'shyu'

import pprint

from googleapiclient.discovery import build
import json, sys

def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  #service = build("CustomSearchAPI", "v1", developerKey="AIzaSyDkxRofVDMMrci34b9yFCePgJz2YAoDmAA")
  service = build("customsearch", "v1", developerKey="AIzaSyC8viCWyzR_q2MBKLeRZGpc7BHA3NTNimA")


  #  https://developers.google.com/custom-search/json-api/v1/reference/cse/list


  collection = service.cse()

  num_requests = 2
  search_term='Olympics'
  search_engine_id = '012608441591405123751:clhx3wq8jxk'

  #sampletext = ''

  for i in range(0, num_requests):
        # This is the offset from the beginning to start getting the results from
        start_val = 1 + (i * 10)
        # Make an HTTP request object
        request = collection.list(q=search_term,
            num=10, #this is the maximum & default anyway
            start=start_val,
            cx=search_engine_id
        )
        response = request.execute()
        #user = json.loads(response)
        output = json.dumps(response, sort_keys=True, indent=2)
        data = json.loads(output)
        #jdict = json.load(output)

        for j in range(0,len(data['items'])):
            print(data['items'][j].get('title')+'\t'+data['items'][j].get('link')+'\t'+data['items'][j].get('htmlSnippet'))

        #print(len(response))
        #print(len(data))
        #print(output)
        #output_f.write(output)
        print('Wrote 10 search results...')


  #print('Output file "{}" written.'.format(output_fname))

  # res = service.cse().list(
  #     q='Olympics',
  #     cx='012608441591405123751:clhx3wq8jxk',
  #     num=11,
  #     start=20,
  #     dateRestrict='y1',
  #     lr='lang_ar',
  #     #searchType='image',
  #   ).execute()
  # pprint.pprint(res)

if __name__ == '__main__':
  main()